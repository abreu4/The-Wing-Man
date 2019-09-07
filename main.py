# the wingman

import os
import requests
import subprocess
import tkinter

from swiper import Swiper

"""
def requests():
    url = 'http://tinder.com'
    r = requests.get(url)  # requests.get to make a get call to google server.
    with open("tinder.html", "w+") as file:
        file.write(str(r.content))

    print(r.content)
    print(r.status_code)
    print(len(r.content))
"""

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

    swiper = Swiper()
    mode = "DC"
    # DE = data extraction
    # DC = data conversion

    # SS = swipe smart
    # S = swipe dumb

    if mode is "DC":
        return

    if swiper.fb_login():
        if swiper.tinder_login:
            if mode is 'DE':
                swiper.data_extraction()

            else:
                while True:
                    swiper.dumb_swipe()

    else:
        print('Login failed')


    return


if __name__ == '__main__':
    main()