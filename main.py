# the chick finder bot

import requests
import subprocess

from swiper import Swiper


def requests():
    url = 'http://tinder.com'
    r = requests.get(url)  # requests.get to make a get call to google server.
    with open("tinder.html", "w+") as file:
        file.write(str(r.content))

    print(r.content)
    print(r.status_code)
    print(len(r.content))


def main():

    swiper = Swiper()
    mode = "M"
    # M = manual
    # S = smart
    # D = dumb

    if swiper.fb_login():
        if swiper.tinder_login:
            if mode is 'M':
                swiper.manual_swipe()
            else:
                while True:
                    swiper.dumb_swipe()

    else:
        print('Login failed')


    return


if __name__ == '__main__':
    main()