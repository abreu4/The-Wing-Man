import os
import re
import time
import shutil
import urllib
import tkinter
from utilities import wait_4_key, random_string
from getpass import getpass
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


class Swiper():

    def __init__(self):

        option = Options()
        option.add_argument("--disable-infobars")
        option.add_argument("start-maximized")
        option.add_argument("--disable-extensions")

        # Pass the argument 1 to allow and 2 to block
        option.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})
        self.driver = webdriver.Chrome(chrome_options=option, executable_path='chromedriver.exe')

    def fb_login(self):
        self.driver.get('https://www.facebook.com/')
        a = self.driver.find_element_by_id('email')
        a.send_keys('tiagoabreu7197@gmail.com')
        b = self.driver.find_element_by_id('pass')
        b.send_keys(getpass(prompt='Username entered. Please enter password: '))
        print("Password entered. Logging in.")
        c = self.driver.find_element_by_id('loginbutton')
        c.click()

        # Check whether login was successful by finding the home button
        try:
            self.driver.find_element_by_id('u_0_c')
        except:
            return False
        return True

    @property
    def tinder_login(self):
        self.driver.get('http://tinder.com')
        time.sleep(5)
        print("Clicking on sign in with Facebook.")
        self.driver.find_element_by_xpath("//*[@aria-label='Log in with Facebook']").click()
        time.sleep(5)

        """ Some exceptions that need reviewing - supposedly being ignored by the bypass all command for Chrome
        try:  # Selenium scripts open a testing environment in chrome. Every login acts like a brand new login. Must click through tutorial
            print("Dismissing tutorial prompts")
            self.driver.find_element_by_xpath(
                "//*[@id=\"content\"]/div/span/div/div[2]/div/div[1]/div[1]/div/button/span/span").click()
            print("Prompt 1")
            time.sleep(2)
            self.driver.find_element_by_xpath(
                "//*[@id=\"content\"]/div/span/div/div[2]/div/div/main/div/button/span/span").click()
            print("Prompt 2")
            time.sleep(2)
            self.driver.find_element_by_xpath(
                "//*[@id=\"content\"]/div/span/div/div[2]/div/div/div[1]/div/div/div[4]/button[1]/span/span").click()
            print("Prompt 3")
            time.sleep(2)
            self.driver.find_element_by_xpath(
                "//*[@id=\"content\"]/div/span/div/div[2]/div/div/div[1]/div/div/div[4]/button[1]/span/span").click()
            print("Prompt 4")
        except:
            print('Something went wrong during login.')
            return False
        """
        print("Ready to start swiping.")
        return True

    def dumb_swipe(self):

        """
        The dumb swiping mode simply swipes right. Could be modified later
        to store info from profiles in order to educate the model later on
        """

        actions = ActionChains(self.driver)
        print("Dumb swiping mode activated")
        time.sleep(5)
        try:
            while self.driver.find_element_by_class_name("recsCardboard"):
                actions.send_keys(Keys.ARROW_RIGHT).perform()
                time.sleep(2)
        except:
            """
            Needs extra error handling for no profiles found, popup found,
            no more likes, free super like screen, etc.
            """
            print("Something came up. Quitting...")
            self.driver.quit()

    def data_extraction(self, just_data=False):

        """ Extracts and labels pictures from profiles """
        """ just_data flag swipes left even for right labels """
        """ in case you, you know, run out of likes """

        print("Data extraction mode activated")

        DIR = './data/sorted'
        LEFT = os.path.join(DIR, "left")
        RIGHT = os.path.join(DIR, "right")
        # TODO falta um try os is file com makedir na exception

        while True:
            # loops until it finds a profile
            found_profile = False
            done = False
            while not found_profile:
                try:
                    found_profile = self.driver.find_elements_by_class_name("react-swipeable-view-container")
                except NoSuchElementException:
                    pass

            # find the picture blocks
            image_blocks = self.driver.find_elements_by_xpath('//*[@class="recCard Ov(h) Cur(p) W(100%) Bgc($c-placeholder) StretchedBox Bdrs(8px) CenterAlign--ml Toa(n) active"]//*[@class="react-swipeable-view-container"]//*[@data-swipeable="true"]')

            # iterates through each of the image blocks
            for i in range(len(image_blocks)):
                # loops until it finds a picture link in current block
                current_picture = None
                while current_picture is None:
                    try:
                        current_picture = self.driver.find_element_by_xpath('//*[@class="recCard Ov(h) Cur(p) W(100%) Bgc($c-placeholder) StretchedBox Bdrs(8px) CenterAlign--ml Toa(n) active"]//*[@class="react-swipeable-view-container"]//*[@aria-hidden="false"]//*[@class="Bdrs(8px) Bgz(cv) Bgp(c) StretchedBox"]')
                    except NoSuchElementException:
                        pass

                # extracts the picture
                raw_link = current_picture.get_attribute('style')  # getting the full style block where link is embedded
                link = re.search("(?P<url>https?://[^\s'\"]+)", raw_link).group("url")  # extracting just the url string from said block
                path = urllib.parse.urlparse(link).path
                name = random_string()+os.path.splitext(path)[1]
                saved = urllib.request.urlretrieve(link, os.path.join(DIR, name))  # download and save image

                # jumps to the next picture
                ActionChains(self.driver).send_keys(' ').perform()  # moving toward the next picture

            # list all the pictures for the current profile
            imagefiles = [os.path.join(DIR, f) for f in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, f)) and (f.endswith('.jpg') or f.endswith('.webp'))]
            print("Saved %d pictures." % len(imagefiles))

            # TODO try/except in case user presses invalid key

            while not done:

                swiped = wait_4_key()

                # if you press 1, then pictures for current profile will be saved in 'left' folder
                if swiped == b'1':
                    [shutil.move(image, LEFT) for image in imagefiles]
                    print("Moved to 'left'")

                    # swipes left
                    ActionChains(self.driver).send_keys(Keys.ARROW_LEFT).perform()
                    time.sleep(0.5)
                    done = True

                # if you press 2, then pictures will go on the 'right'
                elif swiped == b'2':
                    [shutil.move(image, RIGHT) for image in imagefiles]
                    print("Moved to 'right'")

                    # if we're just gathering data, we save right swipes in the 'right' folder, but swipe left instead
                    if just_data:
                        # swipes left
                        ActionChains(self.driver).send_keys(Keys.ARROW_LEFT).perform()
                        time.sleep(0.5)
                    else:
                        # swipes right
                        ActionChains(self.driver).send_keys(Keys.ARROW_RIGHT).perform()
                        time.sleep(0.5)

                    done = True

                else:
                    for image in imagefiles:
                            os.remove(image)
                            print("Removed images")

                    ActionChains(self.driver).send_keys(Keys.ARROW_LEFT).perform()
                    time.sleep(0.5)

                    done = True



        return 1
