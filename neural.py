# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Finetuning torchvision models for the purpose of predicting
# the swipes, left or right
#
# Based on https://pytorch.org/tutorials/beginner/finetuning_torchvision_models_tutorial.html
#
# Lots of things could be tweaked here:
#   - Model learning rate
#   - Whether to train or to load an existing model
#   - Which architecture to use
#   - Different models for different people!
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from __future__ import print_function, division
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import time
import os
import copy
import uuid


class Libido:

    def __init__(self):
        self.savepath = "trained_models/"
        self.current_model_name = str(uuid.uuid1()) + ".pth"
        self.data_dir = "data/sorted"
        self.pretrained = True
        self.num_epochs = 12

        # Data augmentation and normalization for training
        # Just normalization for validation
        self.data_transforms = {
            'train': transforms.Compose([
                transforms.Resize(224),  # RandomResizedCrop(224), - currently assumes input images are square
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ]),
            'test': transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ]),
        }

        self.image_datasets = {x: datasets.ImageFolder(os.path.join(self.data_dir, x), self.data_transforms[x]) for x in ['train', 'test']}
        self.dataloaders = {x: torch.utils.data.DataLoader(self.image_datasets[x], batch_size=4, shuffle=True, num_workers=4) for x in
                       ['train', 'test']}
        self.dataset_sizes = {x: len(self.image_datasets[x]) for x in ['train', 'test']}
        self.class_names = self.image_datasets['train'].classes
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        print("Class_names: {}".format(self.class_names))
        print("Using CUDA: {} - {}".format(torch.cuda.is_available(), self.device))

    def train_model(self, pretrained):

        model_ft = models.resnet18(pretrained=self.pretrained)
        num_ftrs = model_ft.fc.in_features
        model_ft.fc = nn.Linear(num_ftrs, len(self.class_names))
        model_ft = model_ft.to(self.device)

        criterion = nn.CrossEntropyLoss()

        # Observe that all parameters are being optimized - finetuning
        optimizer_ft = optim.SGD(model_ft.parameters(), lr=0.001, momentum=0.9)

        # Decay LR by a factor of 0.001 every epoch
        exp_lr_scheduler = lr_scheduler.StepLR(optimizer_ft, step_size=1, gamma=0.001)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        model_ft = self._train_model(model_ft, criterion, optimizer_ft, exp_lr_scheduler, num_epochs=self.num_epochs)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def _train_model(self, model, criterion, optimizer, scheduler, num_epochs=25):
        since = time.time()

        best_model_wts = copy.deepcopy(model.state_dict())
        best_acc = 0.0

        for epoch in range(num_epochs):
            print('Epoch {}/{}'.format(epoch, num_epochs - 1))
            print('-' * 10)

            # Each epoch has a training and validation phase
            for phase in ['train', 'test']:
                if phase == 'train':
                    model.train()  # Set model to training mode
                else:
                    model.eval()  # Set model to evaluate mode

                running_loss = 0.0
                running_corrects = 0

                # Iterate over data.
                for inputs, labels in self.dataloaders[phase]:
                    inputs = inputs.to(self.device)
                    labels = labels.to(self.device)

                    # zero the parameter gradients
                    optimizer.zero_grad()

                    # forward
                    # track history if only in train
                    with torch.set_grad_enabled(phase == 'train'):
                        outputs = model(inputs)
                        _, preds = torch.max(outputs, 1)
                        loss = criterion(outputs, labels)

                        # backward + optimize only if in training phase
                        if phase == 'train':
                            loss.backward()
                            optimizer.step()

                    # statistics
                    running_loss += loss.item() * inputs.size(0)
                    running_corrects += torch.sum(preds == labels.data)
                if phase == 'train':
                    scheduler.step()

                epoch_loss = running_loss / self.dataset_sizes[phase]
                epoch_acc = running_corrects.double() / self.dataset_sizes[phase]

                print('{} Loss: {:.4f} Acc: {:.4f}'.format(
                    phase, epoch_loss, epoch_acc))

                # deep copy the model
                if phase == 'test' and epoch_acc > best_acc:
                    best_acc = epoch_acc
                    best_model_wts = copy.deepcopy(model.state_dict())

            print()

        time_elapsed = time.time() - since
        print('Training complete in {:.0f}m {:.0f}s'.format(
            time_elapsed // 60, time_elapsed % 60))
        print('Best val Acc: {:4f}'.format(best_acc))

        # Save after training
        torch.save(best_model_wts, os.path.join(self.savepath, self.current_model_path))

        # Load model
        model.load_state_dict(best_model_wts)

        # Visualize best model
        # TODO: - For debug, remove once done
        self.visualize_model(model)
        plt.show()

        # return model
        return model

    def imshow(self, inp, title=None):
        """Imshow for Tensor."""
        inp = inp.numpy().transpose((1, 2, 0))
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        inp = std * inp + mean
        inp = np.clip(inp, 0, 1)
        plt.imshow(inp)
        if title is not None:
            plt.title(title)
        plt.pause(0.001) # pause a bit so that plots are updated

    def visualize_model(self, model, num_images=6):

        was_training = model.training
        model.eval()
        images_so_far = 0
        fig = plt.figure()

        with torch.no_grad():
            for i, (inputs, labels) in enumerate(self.dataloaders['test']):
                inputs = inputs.to(self.device)
                labels = labels.to(self.device)

                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)

                for j in range(inputs.size()[0]):
                    images_so_far += 1
                    ax = plt.subplot(num_images // 2, 2, images_so_far)
                    ax.axis('off')
                    ax.set_title('predicted: {}'.format(self.class_names[preds[j]]))
                    self.imshow(inputs.cpu().data[j])

                    if images_so_far == num_images:
                        model.train(mode=was_training)
                        return
            model.train(mode=was_training)