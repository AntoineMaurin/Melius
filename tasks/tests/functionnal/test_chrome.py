from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from tasks.models import SimpleTask, TaskList
import time
from selenium.webdriver.common.keys import Keys



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

    def create_user(self):
        self.user = User.objects.create_user(username='seleniumtest@test.com',
                                             email='seleniumtest@test.com',
                                             password='password')
        TaskList.objects.create(user=self.user)
    def test_simple_task_creation(self):
        self.create_user()
        self.browser.get(self.live_server_url + '/login')

        username = self.browser.find_element_by_name("username")
        password = self.browser.find_element_by_name("password")

        username.send_keys("seleniumtest@test.com")
        password.send_keys("password")

        self.browser.find_element_by_class_name("register-submit").click()

        self.browser.get(self.live_server_url + '/tasks')

        task_name_field = self.browser.find_element_by_id(
            "empty-task-form-name")

        task_name_field.send_keys("test task")

        self.browser.find_element_by_id(
            'empty-task-form-submit-add-button').click()

        self.assertTrue(SimpleTask.objects.filter(tasklist__user=self.user,
                                                  name='test task').exists())
