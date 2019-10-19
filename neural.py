# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Added NIMA on PyTorch for aesthetic evaluation of pictures
# Code courtesy of:
#   - https://github.com/kentsyx/Neural-IMage-Assessment/
#   - https://github.com/kentsyx/Neural-IMage-Assessment/issues/12
#
# Learn more about NIMA in https://arxiv.org/pdf/1709.05424.pdf
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import argparse
import os

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import torch
from torch import no_grad
import torch.autograd as autograd
import torch.optim as optim

import torchvision.transforms as transforms
import torchvision.datasets as dsets
import torchvision.models as models

import torch.nn.functional as F

from nima.model import *

import cv2

# file_name = 'me'
path_to_data = r"C:\Users\Tiago\PycharmProjects/thewingman\data/testing2"
image_names = os.listdir(path_to_data)
image_names = [os.path.join(path_to_data, f) for f in image_names if f.endswith(".jpg")]

img_tensors = []
for filename in image_names:
    image = cv2.imread(filename)
    image = cv2.resize(image, (224, 224))

    img_arr = image.transpose(2, 0, 1)  # C x H x W
    img_arr = np.expand_dims(img_arr, axis=0)
    print(img_arr.shape)

    img_tensor = torch.from_numpy(img_arr)
    img_tensor = img_tensor.type('torch.FloatTensor')
    print(img_tensor.shape, img_tensor.size)

    img_tensors.append(img_tensor)
# show_handler = plt.imshow(image)
# plt.show()

cuda = torch.cuda.is_available()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
if cuda:
    print("Device: GPU")
else:
    print("Device: CPU")

base_model = models.vgg16(pretrained=True)
model = NIMA(base_model)

model.load_state_dict(torch.load("./nima/epoch-57.pkl", map_location=lambda storage, loc: storage))
print("Successfully loaded model")

with torch.no_grad():
    model.eval()

for filename, image in zip(image_names, img_tensors):

    output = model(image)
    output = output.view(10, 1)

    predicted_mean, predicted_std = 0.0, 0.0
    for i, elem in enumerate(output, 1):
        predicted_mean += i * elem
    for j, elem in enumerate(output, 1):
        predicted_std += elem * (j - predicted_mean) ** 2
    print("________________")
    print("Picture {}: ".format(filename))
    print(u"({}) \u00B1{}".format(round(float(predicted_mean), 2), round(float(predicted_std), 2)))