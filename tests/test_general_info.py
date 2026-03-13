import pytest
import random
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.general_info_page import GeneralInfoPage

class TestGeneralInfo:

    @pytest.fixture(autouse=True)
    def setup(self, authenticated_page: Page):
        self.login_page = LoginPage(authenticated_page)
        self.general_info_page = GeneralInfoPage(authenticated_page)
        self.general_info_page.navigate_to_general_info()


    def test_edit_general_info(self, authenticated_page: Page):
        """Verify that organization phone and fax numbers can be successfully updated."""
        info_before = self.general_info_page.get_info_values()
        
        test_phone = f"+1-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        test_fax = f"+1-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        
        print(f"Updating General Info - Phone: {test_phone}, Fax: {test_fax}")
        
        self.general_info_page.update_general_info(phone=test_phone, fax=test_fax)
        
        # Verify values updated
        info_after = self.general_info_page.get_info_values()
        assert info_after["phone"] == test_phone, f"Phone not updated! Expected {test_phone}, got {info_after['phone']}"
        assert info_after["fax"] == test_fax, f"Fax not updated! Expected {test_fax}, got {info_after['fax']}"

    

    def test_general_info_mandatory_field(self, authenticated_page: Page):
        """Verify that 'Organization Name' is a mandatory field and shows a 'Required' error when empty."""
        # Navigate and clear organization name
        self.general_info_page.clear_organization_name()
        
        # Click save
        self.general_info_page.click_save()
        
        # Verify required error
        assert self.general_info_page.is_required_error_visible("Organization Name"), "Required error not visible for Organization Name!"
