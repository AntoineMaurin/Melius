from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class MeliusChromeTest(StaticLiveServerTestCase):
    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        self.browser = webdriver.Chrome(ChromeDriverManager().install(),
                                        chrome_options=chrome_options)

    def tearDown(self):
        self.browser.close()

    def test_user_registration_and_login(self):
        self.browser.get(self.live_server_url + '/register')
        self.assertEquals(
            self.browser.current_url,
            self.live_server_url + '/register'
            )
        email = self.browser.find_element_by_name("email")
        pw1 = self.browser.find_element_by_name("pw1")
        pw2 = self.browser.find_element_by_name("pw2")
        email.send_keys("thetest@test.com")
        pw1.send_keys("testpassword")
        pw2.send_keys("testpassword")

        self.browser.find_element_by_class_name("register-submit").click()

        self.assertEquals(
            self.browser.current_url,
            self.live_server_url + '/login'
            )
        succes_message = self.browser.find_element_by_class_name(
            "alert-success")

        self.assertEquals(
            succes_message.text,
            'Compte créé ! Bienvenue thetest@test.com'
            )

        username = self.browser.find_element_by_name("username")
        password = self.browser.find_element_by_name("password")

        username.send_keys("thetest@test.com")
        password.send_keys("testpassword")

        self.browser.find_element_by_class_name("register-submit").click()

        self.assertEquals(
            self.browser.current_url,
            self.live_server_url + '/dashboard'
            )
