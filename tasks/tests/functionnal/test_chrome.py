from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class MeliusChromeTest(StaticLiveServerTestCase):
    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        self.browser = webdriver.Chrome('tasks/tests/functionnal/'
                                        'chromedriver',
                                        chrome_options=chrome_options)

    def tearDown(self):
        self.browser.close()

    def test_number_one(self):
        self.assertEqual(12, 12)
