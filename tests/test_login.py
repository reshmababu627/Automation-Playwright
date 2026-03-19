import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.config import BASE_URL, USERNAME, PASSWORD

class TestLogin:
    @pytest.fixture(autouse=True)
    def setup(self, session_page: Page):
        self.login_page = LoginPage(session_page)
        self.dashboard_page = DashboardPage(session_page)

    def test_login_invalid_credentials(self, session_page: Page):
        """Verify that an error message is displayed when attempting to log in with invalid credentials."""
        # Clean login check
        self.login_page.navigate(BASE_URL)
        self.login_page.login("Admin", "InvalidPassword")
        assert self.login_page.get_invalid_credential_message() == "Invalid credentials"

    def test_login_empty_username(self, session_page: Page):
        """Verify that an error message is displayed when attempting to log in with an empty username."""
        self.login_page.navigate(BASE_URL)
        self.login_page.login("", PASSWORD)
        assert self.login_page.is_input_error_displayed()
        assert self.login_page.get_input_error_message() == "Required"

    def test_login_empty_password(self, session_page: Page):
        """Verify that an error message is displayed when attempting to log in with an empty password."""
        self.login_page.navigate(BASE_URL)
        self.login_page.login(USERNAME, "")
        assert self.login_page.is_input_error_displayed()
        assert self.login_page.get_input_error_message() == "Required"

    def test_orangehrm_login(self, session_page: Page):
        """Verify that the user can successfully log in with valid credentials."""
        self.login_page.navigate(BASE_URL)
        self.login_page.login(USERNAME, PASSWORD)
        assert self.dashboard_page.is_dashboard_visible()