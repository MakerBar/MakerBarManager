from unittest import TestCase
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display

class UserProfileTest(TestCase):
    def setUp(self):
        self.live_server_path = 'http://localhost:8000'
        self.dummy_user='DUMMY_TEST'
        self.dummy_pass='password'
        self.display = Display(visible=0,size=(800,600))
        self.display.start()
        self.browser = webdriver.Firefox()
        #create a dummy test user
        self.browser.get(self.live_server_path+'/admin/auth/user/add/')
        self.browser.find_element_by_id('id_username').send_keys(self.dummy_user)
        self.browser.find_element_by_id('id_password1').send_keys(self.dummy_pass)
        self.browser.find_element_by_id('id_password2').send_keys(self.dummy_pass)
        self.browser.find_element_by_id('id_username').submit()

    def tearDown(self):
        #self.browser.get(self.live_server_url + '/admin/auth/user/')
        #userElement = self.browser.find_element_by_id('id_username')
        #userElement.send_keys(self.dummy_user)
        #passElement = self.browser.find_element_by_id('id_password1')
        #passElement.send_keys(self.dummy_pass)
        #passElement.submit()
        self.browser.quit()

    def test_create_new_profile_via_admin(self):
        self.browser.get(self.live_server_path + '/admin/presence/userprofilepresence/add/')
        userElement=self.browser.find_element_by_id('id_user')
        userElement.send_keys(self.dummy_user)
        deviceNameElement=self.browser.find_element_by_id('id_device_set-0-name')
        deviceNameElement.send_keys("DUMMY_DEVICE")
        deviceMACElement=self.browser.find_element_by_id('id_device_set-0-mac')
        deviceMACElement.send_keys("00:00:00:00:00:00")
        deviceMACElement.submit()
        try:
            WebDriverWait(self.browser,10)
            successElement=self.browser.find_element_by_class('info')
            self.assertIn('The user profile presence "%s" was added successfully.' % self.dummy_user,successElement.text)
        except TimeoutException as e:
            self.fail(e)