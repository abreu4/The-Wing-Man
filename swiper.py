import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from getpass import getpass
import urllib as u


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
        try:  # Check whether login was successful by finding the home button
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

    def manual_swipe(self):

        actions = ActionChains(self.driver)
        print("Manual swiping mode activated")
        time.sleep(2)

        try:
            while True:
                if self.driver.find_element_by_class_name("react-swipeable-view-container"):
                    image_links = self.driver.find_elements_by_class_name("recCard")
                    print('len(image_links): {:}'.format(len(image_links)))
                    input()
                    for i in range(len(image_links)):
                        href = image_links[i].get_attribute('href')
                        u.urlretrieve(href, "nome da gaja_"+str(i)+".png")
                    input()

                # get data from current profile, wait for user input (left or right)
                # when the user clicks, associate this input with data obtained
                # expect a token when user closes tinder
                # discard data if user closes tinder before labelling
                #
#                href = link.get_attribute('href')
 #               download = self.browser.get(href)
        except:
            return -1


        return 1