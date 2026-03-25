from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from authentication.models import CustomUser

WAIT_TIMEOUT = 10


class LoginE2ETest(StaticLiveServerTestCase):
    """End-to-end tests for login and logout functionality."""

    valid_email = "test@test.com"
    valid_password = "testpassword123"

    def setUp(self):
        CustomUser.objects.create_user(
            email=self.valid_email,
            password=self.valid_password,
            first_name="Test",
            last_name="User",
            is_active=True,
        )
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def wait_clickable(self, by, selector):
        return WebDriverWait(self.driver, WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((by, selector))
        )

    def wait_visible(self, by, selector):
        return WebDriverWait(self.driver, WAIT_TIMEOUT).until(
            EC.visibility_of_element_located((by, selector))
        )

    def login(self, email, password):
        self.driver.get(self.live_server_url)

        self.wait_clickable(By.CSS_SELECTOR, "[data-id='login-link']").click()
        self.wait_visible(By.NAME, "email").send_keys(email)
        self.wait_visible(By.NAME, "password").send_keys(password)
        self.wait_clickable(By.CSS_SELECTOR, "[data-id='login-button']").click()

    def test_valid_login_and_logout(self):
        self.login(self.valid_email, self.valid_password)

        logout_button = self.wait_visible(By.CSS_SELECTOR, "[data-id='logout-button']")
        self.assertTrue(logout_button.is_displayed(), "Logout button should be visible after login")

        logout_button.click()

        login_link = self.wait_visible(By.CSS_SELECTOR, "[data-id='login-link']")
        self.assertTrue(login_link.is_displayed(), "Login link should be visible after logout")
        logout_buttons = self.driver.find_elements(By.CSS_SELECTOR, "[data-id='logout-button']")
        self.assertEqual(len(logout_buttons), 0, "Logout button should not be present after logout")

    def test_invalid_login(self):
        self.login("wrong@wrong.com", "wrongpassword")

        error = self.wait_visible(By.CSS_SELECTOR, "[data-id='alert-message']")
        self.assertTrue(error.is_displayed(), "Error message should be displayed for invalid credentials")
        self.assertIn("Invalid", error.text)

        logout_buttons = self.driver.find_elements(By.CSS_SELECTOR, "[data-id='logout-button']")
        self.assertEqual(len(logout_buttons), 0, "Logout button should not be present after failed login")
