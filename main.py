# the wingman

import os
import requests
import subprocess
import tkinter as tk


from swiper import Swiper
import data
import ranker

DATA_TEST = 'data/testing'
DATA_RESIZE = 'data/testing2'
DATA = 'data/raw'


def main():

    # DE = data extraction
    # DT = data treatment
    # DL = data labelling

    # SS = swipe smart
    # SD = swipe dumb
    mode = "DL"

    # testing the ranker
    if mode is "DL":
        ranker.run()
        return

    # testing the data library
    if mode is "DT":
        data.rename(DATA_TEST)
        return

    # testing the swiper library
    swiper = Swiper()
    if swiper.fb_login():
        if swiper.tinder_login:
            if mode is 'DE':
                swiper.data_extraction()

            else:
                while True:
                    swiper.dumb_swipe()

    else:
        print('Login failed')
        return -1

    return 1


if __name__ == '__main__':
    main()