from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

class UserProfileTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        #create a dummy test user
        self.dummy_user='DUMMY_TEST'
        self.dummy_pass='password'
        self.browser.get(self.live_server_url + '/admin/auth/user/add/')
        userElement = self.browser.find_element_by_id('id_username')
        userElement.send_keys(self.dummy_user)
        passElement = self.browser.find_element_by_id('id_password1')
        passElement.send_keys(self.dummy_pass)
        passElement.submit()

    def tearDown(self):
        #self.browser.get(self.live_server_url + '/admin/auth/user/')
        #userElement = self.browser.find_element_by_id('id_username')
        #userElement.send_keys(self.dummy_user)
        #passElement = self.browser.find_element_by_id('id_password1')
        #passElement.send_keys(self.dummy_pass)
        #passElement.submit()
        self.browser.quit()

    def test_create_new_profile_via_admin(self):
        self.browser.get(self.live_server_url + '/admin/presence/userprofilepresence/add/')
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