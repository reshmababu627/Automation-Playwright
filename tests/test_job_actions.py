import random
import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.job_page import JobPage
from utils.config import BASE_URL, USERNAME, PASSWORD


class TestJob:
    job_title = None

    @pytest.fixture(autouse=True)
    def setup(self, authenticated_page: Page):
        self.login_page = LoginPage(authenticated_page)
        self.job_page = JobPage(authenticated_page)

    def test_add_job_title(self, authenticated_page: Page):
        self.job_page.navigate_to_job_titles()
        TestJob.job_title = f"QA Engineer {random.randint(1000, 9999)}"
        print(f"Testing Add Job Title: {TestJob.job_title}")
        
        # Add Job Title
        self.job_page.add_job(TestJob.job_title, "Automation Testing Role")
        
        # Verify
        assert self.job_page.is_job_present(TestJob.job_title), f"Job Title {TestJob.job_title} not found!"

    def test_edit_job_title(self, authenticated_page: Page):
        authenticated_page.wait_for_timeout(2000)
        assert TestJob.job_title is not None, "Setup failed: No job title to edit!"
        
        old_title = TestJob.job_title
        new_title = f"Edited_{old_title}"
        print(f"Editing Job Title: {old_title} -> {new_title}")
        
        # Edit Job Title
        self.job_page.edit_job(old_title, new_title)
        
        # Update class variable
        TestJob.job_title = new_title
        
        # Verify
        assert self.job_page.is_job_present(new_title), f"New Job Title {new_title} not found!"

    def test_delete_job_title(self, authenticated_page: Page):
        authenticated_page.wait_for_timeout(2000)
        assert TestJob.job_title is not None, "Setup failed: No job title to delete!"
        
        title_to_delete = TestJob.job_title
        print(f"Deleting Job Title: {title_to_delete}")

        # Delete Job Title
        self.job_page.delete_job(title_to_delete)
        
        # Reset state
        TestJob.job_title = None
        
        # Verify
        assert not self.job_page.is_job_present(title_to_delete), f"Job Title {title_to_delete} still exists after deletion!"

    def test_add_job_title_duplicate(self, authenticated_page: Page):
       #self.job_page.navigate_to_job_titles()
        authenticated_page.wait_for_timeout(2000)
        existing_title = f"Duplicate Job {random.randint(1000, 9999)}"
        
        # Add a job first
        self.job_page.add_job(existing_title, "Original")
        
        # Try to add the same title again
        self.job_page.page.click(self.job_page.add_button)
        self.job_page.page.fill(self.job_page.job_title_input, existing_title)
        self.job_page.page.click(self.job_page.save_button)
        
        # Verify duplicate error
        assert self.job_page.is_duplicate_error_visible(), "Duplicate error message not visible!"
        
        # Cleanup
        self.job_page.click_cancel()
        #self.job_page.delete_job(existing_title)

    def test_add_job_title_empty(self, authenticated_page: Page):
        #self.job_page.navigate_to_job_titles()
        authenticated_page.wait_for_timeout(2000)
        self.job_page.page.click(self.job_page.add_button)
        
        # Click save without filling title
        self.job_page.page.click(self.job_page.save_button)
        
        # Verify required field error
        assert self.job_page.is_required_error_visible(), "Required field error message not visible!"
        
        # Cleanup
        self.job_page.click_cancel()

    def test_cancel_add_job(self, authenticated_page: Page):
        #self.job_page.navigate_to_job_titles()
        authenticated_page.wait_for_timeout(2000)
        self.job_page.page.click(self.job_page.add_button)
        
        temp_title = "Cancel Test Job"
        self.job_page.page.fill(self.job_page.job_title_input, temp_title)
        
        # Click Cancel
        self.job_page.click_cancel()
        
        # Verify job is not added
        assert not self.job_page.is_job_present(temp_title), f"Job Title {temp_title} was added despite clicking cancel!"

    def test_bulk_delete_job_titles(self, authenticated_page: Page):
        #self.job_page.navigate_to_job_titles()
        authenticated_page.wait_for_timeout(2000)
        
        # Create some random job titles to delete
        titles_to_create = [f"BulkDelete_{random.randint(1000, 9999)}" for _ in range(3)]
        for title in titles_to_create:
            self.job_page.add_job(title)
            
        print(f"Testing Bulk Delete for: {titles_to_create}")
        
        # Refresh and navigate back to list (though add_job should do it)
        #self.job_page.navigate_to_job_titles()
        authenticated_page.wait_for_timeout(2000)
        
        # Select and Delete
        self.job_page.select_job_titles(titles_to_create)
        self.job_page.delete_selected()
        
        # Verify all are deleted
        for title in titles_to_create:
            assert not self.job_page.is_job_present(title), f"Job Title {title} still exists after bulk deletion!"

    def test_upload_job_specification(self, authenticated_page: Page):
        import os
       # self.job_page.navigate_to_job_titles()
        authenticated_page.wait_for_timeout(2000)
        self.job_page.page.click(self.job_page.add_button)
        
        job_title = f"UploadTest_{random.randint(1000, 9999)}"
        self.job_page.page.fill(self.job_page.job_title_input, job_title)
        
        # Upload valid file
        file_path = os.path.abspath("test_spec.pdf")
        self.job_page.upload_job_specification(file_path)
        
        # Save
        self.job_page.page.click(self.job_page.save_button)
        self.job_page.page.wait_for_url("**/viewJobTitleList")
        
        # Verify job is present
        assert self.job_page.is_job_present(job_title), f"Job Title {job_title} not found after upload!"
        
        # Cleanup
        #self.job_page.delete_job(job_title)

    def test_upload_invalid_file_format(self, authenticated_page: Page):
        import os
        #self.job_page.navigate_to_job_titles()
        authenticated_page.wait_for_timeout(2000)
        self.job_page.page.click(self.job_page.add_button)
        
        job_title = f"InvalidUpload_{random.randint(1000, 9999)}"
        self.job_page.page.fill(self.job_page.job_title_input, job_title)
        
        # Upload invalid file (.exe)
        file_path = os.path.abspath("dummy.exe")
        self.job_page.upload_job_specification(file_path)
        
        # Click Save
        self.job_page.page.click(self.job_page.save_button)
        
        # Verify invalid file error message
        assert self.job_page.is_file_type_error_visible(), "Invalid file type error message not visible after clicking save!"
        
        # Cleanup
        self.job_page.click_cancel()