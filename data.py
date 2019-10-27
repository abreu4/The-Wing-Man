# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# A library for image data treatment
#
# 1. convert: converts all images to .jpg
# 2. normalize: normalizes all images to AxA size
# 3. check: assert data quality: file number, label, dimensions, format
# 4. label: start labelling routine, ideally from a checkpoint (last labelled image)
# 5. rename: given folder, rename all files in order (1,2,...,n)
# 6. remove_duplicates: md5 hash python for removing duplicates
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import os
import cv2
import time
import shutil
import subprocess
import tkinter as tk
from PIL import ImageTk, Image

from utilities import *
from detector import DetectorAPI


def rename(folder):

    """ Renames files in folder to exact numeric ascending order """

    assert os.path.isdir(folder), "Invalid data folder"

    # get all the files that are not folder in the data folder (images)
    imagefiles = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and f.endswith('.jpg')]
    imagefiles.sort(key=filenumber)

    # rename according to index
    for i in range(len(imagefiles)):
        source = os.path.join(folder, imagefiles[i])
        extension = os.path.splitext(imagefiles[i])[1]
        destination = os.path.join(folder, str(i)+extension)
        os.rename(source, destination)

        print("Renamed "+str(imagefiles[i])+" -> "+str(i)+extension)

    return 1


def convert(folder):

    """ Converts every picture inside folder to JPEG """

    assert os.path.isdir(folder), "Invalid data folder"

    for filename in os.listdir(folder):
        if filename.endswith('.webp') or filename.endswith('.png'):

            # creating jpg
            imgpath = os.path.join(folder, filename)
            im = Image.open(imgpath).convert("RGB")
            im.save(os.path.join(folder, os.path.splitext(filename)[0] + '.jpg'), "jpeg")

            # deleting duplicate in webp
            os.remove(imgpath)

            print('Converted '+str(filename))

    return 1


def remove_duplicates(folder):

    """ Removes duplicate file entries inside folder """

    assert os.path.isdir(folder), "Invalid data folder"
    duplicates = []
    hash_keys = []

    for filename in os.listdir(folder):
        imgpath = os.path.join(folder, filename)
        if os.path.isfile(imgpath):
            hax = file_hash(imgpath)
            if hax not in hash_keys:
                hash_keys.append(hax)
            else:
                duplicates.append(imgpath)

    # Remove all the duplicates
    [os.remove(copycat) for copycat in duplicates]

    print('Removed '+str(len(duplicates))+' duplicates')
    return 1


def keep_only_pics_with_people(folder):

    # TODO not really removing anything yet, still under testing

    print("Trimming dataset...")

    model_path = r"C:\Users\Tiago\PycharmProjects\thewingman\support\faster_rcnn_inception_v2_coco_2018_01_28/frozen_inference_graph.pb"
    odapi = DetectorAPI(path_to_ckpt=model_path)
    threshold = 0.7

    # List all pictures in folder
    images = [os.path.join(folder, i) for i in os.listdir(folder)
              if os.path.isfile(os.path.join(folder, i))
              and i.endswith(".jpg")
              or i.endswith(".webp")]

    counter = 0
    found = False
    for img in images:

        img = cv2.imread(img)
        img = cv2.resize(img, (1280, 720))
        boxes, scores, classes, num = odapi.processFrame(img)

        # Visualization of the results of a detection.

        for i in range(len(boxes)):
            # Class 1 represents human
            if classes[i] == 1 and scores[i] > threshold:
                found=True
                box = boxes[i]
                cv2.rectangle(img, (box[1], box[0]), (box[3], box[2]), (255, 0, 0), 2)

        if not found:
            cv2.imshow("preview", img)
            cv2.waitKey()
        else:
            found = False

    print("Kept %d images" % counter)

def resize(src_folder, des_folder, width=640, height=800):

    """ Normalizes src folder images into des folder """
    # Assumes src folder's images of interest have already been converted to '.jpg' format

    print('\nInitializing resizing subroutine')

    assert os.path.isdir(src_folder), "Invalid source data folder"
    if not os.path.isdir(des_folder):
        os.mkdir(des_folder)
        print("New destination directory created")
    print(os.listdir(des_folder))
    assert not os.listdir(des_folder), "Destination folder is not empty"

    image_list = os.listdir(src_folder)
    assert image_list is not None, "There's nothing to resize in that folder"

    dim = (width, height)
    print('Goal dimensions {:}'.format(dim))
    for image in image_list:
        src_img = os.path.join(src_folder, image)

        if os.path.isfile(src_img) and src_img.endswith('.jpg'):

            des_img = os.path.join(des_folder, image)
            img_array = cv2.imread(src_img, cv2.IMREAD_UNCHANGED)

            if img_array.shape[0] == dim[1] and img_array.shape[1] == dim[0]:
                shutil.copy(src_img, des_img)

            else:
                rs_img = cv2.resize(img_array, dim, interpolation=cv2.INTER_CUBIC)
                cv2.imwrite(des_img, rs_img)
                print('Resized image '+image+' {:}'.format(img_array.shape))

        else:
            continue
    return 1
