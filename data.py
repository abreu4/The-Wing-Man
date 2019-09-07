# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# A library for image data treatment
#
# 1. convert: converts all images to .jpg
# 2. normalize: normalizes all images to AxA size
# 3. check: assert data quality: file number, label, dimensions, format
# 4. label: start labelling routine, ideally from a checkpoint (last labelled image)
# 5. rename: given folder, rename all files in order (1,2,...,n)
# 6. remove_duplicates: md5 hash python for removing duplicates
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import os
import subprocess
from PIL import ImageTk, Image
import tkinter as tk

from utilities import *


def rename(folder):

    """ Renames files in folder to exact numeric ascending order """

    assert os.path.isdir(folder), "Invalid data folder"

    # get all the files that are not folder in the data folder (images)
    imagefiles = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
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

    """ Converts every picture inside <folder> to JPEG """

    assert os.path.isdir(folder), "Invalid data folder"

    for filename in os.listdir(folder):
        if filename.endswith('.webp'):

            # creating jpg
            imgpath = os.path.join(folder, filename)
            im = Image.open(imgpath).convert("RGB")
            im.save(os.path.join(folder, os.path.splitext(filename)[0] + '.jpg'), "jpeg")

            # deleting duplicate in webp
            os.remove(imgpath)

            print('done converting '+str(filename)+'…')

    return 1


def remove_duplicates(folder):

    """ Removes duplicate file entries inside <folder> """

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