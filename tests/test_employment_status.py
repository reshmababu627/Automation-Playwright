import pytest
import random
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.employment_status_page import EmploymentStatusPage
from utils.config import BASE_URL, USERNAME, PASSWORD

class TestEmploymentStatus:
    status_name = None

    @pytest.fixture(autouse=True)
    def setup(self, authenticated_page: Page):
        self.login_page = LoginPage(authenticated_page)
        self.employment_status_page = EmploymentStatusPage(authenticated_page)

    def generate_random_name(self):
        return f"EmpStatus_{random.randint(1000, 9999)}"

    def test_add_employment_status(self, authenticated_page: Page):
        self.employment_status_page.navigate_to_employment_status()
        TestEmploymentStatus.status_name = self.generate_random_name()
        print(f"Testing Add Employment Status: {TestEmploymentStatus.status_name}")
        
        # Add Employment Status
        self.employment_status_page.add_employment_status(TestEmploymentStatus.status_name)
        
        # Verify
        assert self.employment_status_page.is_employment_status_present(TestEmploymentStatus.status_name), f"Employment Status {TestEmploymentStatus.status_name} not found after adding!"

    def test_edit_employment_status(self, authenticated_page: Page):
        authenticated_page.wait_for_timeout(2000)
        assert TestEmploymentStatus.status_name is not None, "Setup failed: No status to edit!"
        
        old_name = TestEmploymentStatus.status_name
        new_name = f"Edited_{old_name}"
        print(f"Editing Employment Status: {old_name} -> {new_name}")
        
        # Edit Employment Status
        self.employment_status_page.edit_employment_status(old_name, new_name)
        
        # Update class variable for next test
        TestEmploymentStatus.status_name = new_name
        
        # Verify
        assert self.employment_status_page.is_employment_status_present(new_name), f"New Employment Status {new_name} not found!"

    def test_add_employment_status_empty(self, authenticated_page: Page):
        authenticated_page.wait_for_timeout(2000)
        
        # Click Add and then Save without filling name
        self.employment_status_page.page.click(self.employment_status_page.add_button)
        self.employment_status_page.page.click(self.employment_status_page.save_button)
        
        # Verify error
        assert self.employment_status_page.is_required_error_visible(), "Required error message not visible for empty name!"
        
        # Cleanup
        self.employment_status_page.click_cancel()

    def test_add_duplicate_employment_status(self, authenticated_page: Page):
        authenticated_page.wait_for_timeout(2000)
        existing_name = self.generate_random_name()
        
        # Add an employment status first
        self.employment_status_page.add_employment_status(existing_name)
        
        # Try to add the same name again
        self.employment_status_page.page.click(self.employment_status_page.add_button)
        self.employment_status_page.page.fill(self.employment_status_page.name_input, existing_name)
        self.employment_status_page.page.click(self.employment_status_page.save_button)
        
        # Verify duplicate error
        assert self.employment_status_page.is_already_exists_error_visible(), "Duplicate error message 'Already exists' not visible!"
        
        # Cleanup
        self.employment_status_page.click_cancel()

    def test_delete_employment_status(self, authenticated_page: Page):
        authenticated_page.wait_for_timeout(2000)
        assert TestEmploymentStatus.status_name is not None, "Setup failed: No status to delete!"
        
        name_to_delete = TestEmploymentStatus.status_name
        print(f"Deleting Employment Status: {name_to_delete}")
        
        # Delete Employment Status
        self.employment_status_page.delete_employment_status(name_to_delete)
        
        # Reset state
        TestEmploymentStatus.status_name = None
        
        # Verify
        assert not self.employment_status_page.is_employment_status_present(name_to_delete), f"Employment Status {name_to_delete} still exists after deletion!"

    def test_bulk_delete_employment_status(self, authenticated_page: Page):
        authenticated_page.wait_for_timeout(2000)
        
        # Create some random statuses to delete
        names_to_create = [f"BulkStatus_{random.randint(1000, 9999)}" for _ in range(3)]
        for name in names_to_create:
            self.employment_status_page.add_employment_status(name)
            
        print(f"Testing Bulk Delete for: {names_to_create}")
        
        authenticated_page.wait_for_timeout(2000)
        
        # Select and Delete
        self.employment_status_page.select_employment_statuses(names_to_create)
        self.employment_status_page.delete_selected()
        
        # Verify all are deleted
        for name in names_to_create:
            assert not self.employment_status_page.is_employment_status_present(name), f"Employment Status {name} still exists after bulk deletion!"
