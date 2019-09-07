# the wingman

import os
import requests
import subprocess
import tkinter

from swiper import Swiper
import data

DATA_TEST = 'data/testing'
DATA = 'data'

def main():

    """
    def save_labelled():
        print('girl + misc = {}'.format(score_girl.get()+score_misc.get()))

    top = tkinter.Tk()
    top.geometry('300x115')

    score_girl = tkinter.Scale(top, from_=0, to=100, orient='horizontal', length=300)
    score_girl.grid(column=0, row=0)

    score_misc = tkinter.Scale(top, from_=0, to=100, orient='horizontal', length=300)
    score_misc.grid(column=0, row=1)

    send_button = tkinter.Button(top, text=("Classify"), command=save_labelled)
    send_button.grid(column=0, row=2)

    tkinter.mainloop()
    return
    """

    mode = "DT"
    # DE = data extraction
    # DT = data treatment

    # SS = swipe smart
    # SD = swipe dumb

    if mode is "DT":
        data.rename(DATA)
        return

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