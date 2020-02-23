# The Wing Man

import os
import requests
import subprocess
import tkinter as tk
import ranker
import utilities
from swiper import Swiper
from neural import Libido
from data import convert, split, crop_to_squares

# TODO: - Test routine to extract only pictures with people
# TODO: - Needs additional crop_to_square routine - add to data.py - in order to train model


DATA_TEST = 'data/testing'
DATA_RESIZE = 'data/testing2'
DATA = 'data/raw'
DATA_LABELLING = 'data/labelling'
DATA_SORTED = 'data/sorted'


def main():

    mode = "SD"

    """ DATA TREATMENT 1
    neural_paths = {x : os.path.join(DATA_SORTED, x) for x in ["train", "test"]}
    for phase in ["train", "test"]:
        crop_to_squares(os.path.join(neural_paths[phase], "left"))
        crop_to_squares(os.path.join(neural_paths[phase], "right"))
    exit()
    """

    """ DATA TREATMENT 2
    convert(os.path.join(DATA_SORTED, "left"))
    convert(os.path.join(DATA_SORTED, "right"))

    split(DATA_SORTED, 0.85)
    """

    # TRAINING
    predictor = Libido()
    predictor.train_model(pretrained=True)
    exit()


    # testing the 'swiper.py'
    swiper = Swiper()
    if swiper.fb_login():
        if swiper.tinder_login:
            if mode is 'DE':
                swiper.data_extraction()
                return

        elif mode is 'SD':
            while True:
                swiper.dumb_swipe()
                return

        elif mode is 'SS':
            while True:
                print("TODO")
                # swiper.smart_swipe()
                return

    else:
        print('Login failed')
        return -1

    return 1


if __name__ == '__main__':
    main()