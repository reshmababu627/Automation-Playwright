import pytest
import random
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.job_category_page import JobCategoryPage
from utils.config import BASE_URL, USERNAME, PASSWORD

class TestJobCategories:
    category_name = None

    @pytest.fixture(autouse=True)
    def setup(self, authenticated_page: Page):
        self.login_page = LoginPage(authenticated_page)
        self.job_category_page = JobCategoryPage(authenticated_page)

    def generate_random_name(self):
        return f"JobCategory_{random.randint(1000, 9999)}"

    def test_add_job_category(self, authenticated_page: Page):
        self.job_category_page.navigate_to_job_categories()
        TestJobCategories.category_name = self.generate_random_name()
        print(f"Testing Add Job Category: {TestJobCategories.category_name}")
        
        # Add Job Category
        self.job_category_page.add_job_category(TestJobCategories.category_name)
        
        # Verify
        assert self.job_category_page.is_job_category_present(TestJobCategories.category_name), f"Job Category {TestJobCategories.category_name} not found after adding!"

    def test_edit_job_category(self, authenticated_page: Page):
        authenticated_page.wait_for_timeout(2000)
        assert TestJobCategories.category_name is not None, "Setup failed: No category to edit!"
        
        old_name = TestJobCategories.category_name
        new_name = f"Edited_{old_name}"
        print(f"Editing Job Category: {old_name} -> {new_name}")
        
        # Edit Job Category
        self.job_category_page.edit_job_category(old_name, new_name)
        
        # Update class variable for next test
        TestJobCategories.category_name = new_name
        
        # Verify
        assert self.job_category_page.is_job_category_present(new_name), f"New Job Category {new_name} not found!"

    def test_add_job_category_empty(self, authenticated_page: Page):
        #self.job_category_page.navigate_to_job_categories()
        authenticated_page.wait_for_timeout(2000)
        
        # Click Add and then Save without filling name
        self.job_category_page.page.click(self.job_category_page.add_button)
        self.job_category_page.page.click(self.job_category_page.save_button)
        
        # Verify error
        assert self.job_category_page.is_required_error_visible(), "Required error message not visible for empty name!"
        
        # Cleanup
        self.job_category_page.click_cancel()

    def test_add_duplicate_job_category(self, authenticated_page: Page):
        authenticated_page.wait_for_timeout(2000)
        existing_name = self.generate_random_name()
        
        # Add a category first
        self.job_category_page.add_job_category(existing_name)
        
        # Try to add the same name again
        self.job_category_page.page.click(self.job_category_page.add_button)
        self.job_category_page.page.fill(self.job_category_page.name_input, existing_name)
        self.job_category_page.page.click(self.job_category_page.save_button)
        
        # Verify duplicate error
        assert self.job_category_page.is_already_exists_error_visible(), "Duplicate error message 'Already exists' not visible!"
        
        # Cleanup
        self.job_category_page.click_cancel()
        # Optionally delete the created category if needed, 
        # but usually we leave it for the delete test or handle it via class level cleanup if necessary.
        # For now, let's keep it simple.

    def test_delete_job_category(self, authenticated_page: Page):
        authenticated_page.wait_for_timeout(2000)
        assert TestJobCategories.category_name is not None, "Setup failed: No category to delete!"
        
        name_to_delete = TestJobCategories.category_name
        print(f"Deleting Job Category: {name_to_delete}")
        
        # Delete Job Category
       
        self.job_category_page.delete_job_category(name_to_delete)
        
        # Reset state
        TestJobCategories.category_name = None
        
        # Verify
        assert not self.job_category_page.is_job_category_present(name_to_delete), f"Job Category {name_to_delete} still exists after deletion!"

    def test_bulk_delete_job_categories(self, authenticated_page: Page):
        authenticated_page.wait_for_timeout(2000)
        
        # Create some random categories to delete
        names_to_create = [f"BulkCat_{random.randint(1000, 9999)}" for _ in range(3)]
        for name in names_to_create:
            self.job_category_page.add_job_category(name)
            
        print(f"Testing Bulk Delete for: {names_to_create}")
        
        authenticated_page.wait_for_timeout(2000)
        
        # Select and Delete
        self.job_category_page.select_job_categories(names_to_create)
        self.job_category_page.delete_selected()
        
        # Verify all are deleted
        for name in names_to_create:
            assert not self.job_category_page.is_job_category_present(name), f"Job Category {name} still exists after bulk deletion!"
