from django.urls import reverse

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorsBaseTest


class AuthorsRegisterTest(AuthorsBaseTest):
    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

        form.find_element(By.NAME, 'email').send_keys('a@a.com')

    def test_the_test(self):
        url = self.live_server_url + reverse('authors:register')
        self.browser.get(url)

        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div[2]/form'
        )

        self.fill_form_dummy_data(form)

        first_name_field = form.find_element(By.NAME, 'first_name')
        first_name_field.send_keys(Keys.ENTER)

        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div[2]/form'
        )

        self.assertIn('Write your first name', form.text)
