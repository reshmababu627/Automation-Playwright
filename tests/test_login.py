import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.config import BASE_URL, USERNAME, PASSWORD

class TestLogin:
    @pytest.fixture(autouse=True)
    def setup(self, authenticated_page: Page):
        self.login_page = LoginPage(authenticated_page)
        self.dashboard_page = DashboardPage(authenticated_page)

    def test_login_invalid_credentials(self, authenticated_page: Page):
        # Already logged in via fixture, so logout first to test login UI
        self.login_page.logout()
        
        self.login_page.navigate(BASE_URL)
        self.login_page.login("Admin", "InvalidPassword")
        assert self.login_page.get_invalid_credential_message() == "Invalid credentials"

    def test_login_empty_username(self, authenticated_page: Page):
        self.login_page.navigate(BASE_URL)
        self.login_page.login("", PASSWORD)
        assert self.login_page.is_input_error_displayed()
        assert self.login_page.get_input_error_message() == "Required"

    def test_login_empty_password(self, authenticated_page: Page):
        self.login_page.navigate(BASE_URL)
        self.login_page.login(USERNAME, "")
        assert self.login_page.is_input_error_displayed()
        assert self.login_page.get_input_error_message() == "Required"

    def test_orangehrm_login(self, authenticated_page: Page):
        self.login_page.navigate(BASE_URL)
        self.login_page.login(USERNAME, PASSWORD)
        assert self.dashboard_page.is_dashboard_visible()