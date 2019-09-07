import os
import re
import time
import tkinter
import urllib
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

    def data_extraction(self):

        print("Data extraction mode activated")

        # initialize the image counter
        DIR = './data'
        counter = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

        while True:
            # loops until it finds a profile
            found_profile = False
            while not found_profile:
                try:
                    found_profile = self.driver.find_elements_by_class_name("react-swipeable-view-container")
                except NoSuchElementException:
                    pass

            # find the picture blocks
            image_blocks = self.driver.find_elements_by_xpath('//*[@class="recCard Ov(h) Cur(p) W(100%) Bgc($c-placeholder) StretchedBox Bdrs(8px) CenterAlign--ml Toa(n) active"]//*[@class="react-swipeable-view-container"]//*[@data-swipeable="true"]')
            print(len(image_blocks))

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
                pathx = urllib.parse.urlparse(link).path  # parsing the filename from the url string
                extension = os.path.splitext(pathx)[1]  # extracting extension from the filename
                saved = urllib.request.urlretrieve(link, "./data/"+str(counter)+extension)  # download and save image
                counter += 1  # increasing the file counter

                print('saved: {:}'.format(saved))
                #print('link: {:}'.format(link))

                # jumps to the next picture
                ActionChains(self.driver).send_keys(' ').perform()  # moving toward the next picture

            # jumps to the next profile
            ActionChains(self.driver).send_keys(Keys.ARROW_LEFT).perform()
            time.sleep(0.5)

        return 1