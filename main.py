# the wingman

import os
import requests
import subprocess
import tkinter as tk


import data
import ranker
from neural import Libido
from swiper import Swiper

DATA_TEST = 'data/testing'
DATA_RESIZE = 'data/testing2'
DATA = 'data/raw'
DATA_LABELLING = 'data/labelling'


def main():

    # E = extraction
    # T = treatment
    # L = labelling
    # P = predicting

    # SS = swipe smart
    # SD = swipe dumb

    mode = "P"

    if mode is "P":
        predictor = Libido()
        return

    # testing the ranker
    if mode is "L":
        ranker.run()
        return

    if mode is "T":
        data.rename(DATA_LABELLING)
        return

    # testing the swiper library
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