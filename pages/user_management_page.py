from playwright.sync_api import Page
import re

class UserManagementPage:
    def __init__(self, page: Page):
        self.page = page

        # Navigation
        self.admin_menu = "//span[normalize-space()='Admin']"
        self.user_management_menu = "//span[normalize-space()='User Management ']"
        self.users_menu = "//a[normalize-space()='Users']"
        self.page_header = "//h5[normalize-space()='System Users']"

        # Buttons
        self.add_button = "//button[normalize-space()='Add']"
        self.save_button = "//button[@type='submit']"
        self.cancel_button = "//button[normalize-space()='Cancel']"
        self.edit_button = "i.bi-pencil-fill"
        self.delete_confirm_button = "//button[normalize-space()='Yes, Delete']"
        self.delete_selected_button = "//button[normalize-space()='Delete Selected']"

        # Form Fields
        self.user_role_dropdown = "//label[contains(normalize-space(),'User Role')]/../following-sibling::div//div[contains(@class, 'oxd-select-text')]"
        self.employee_name_autocomplete = "//label[contains(normalize-space(),'Employee Name')]/../following-sibling::div//input"
        self.status_dropdown = "//label[contains(normalize-space(),'Status')]/../following-sibling::div//div[contains(@class, 'oxd-select-text')]"
        self.username_input = "//label[contains(normalize-space(),'Username')]/../following-sibling::div//input"
        self.password_input = "//label[contains(normalize-space(),'Password')]/../following-sibling::div//input"
        self.confirm_password_input = "//label[contains(normalize-space(),'Confirm Password')]/../following-sibling::div//input"
 
        # Search / Filter
        self.search_username_input = "//label[text()='Username']/ancestor::div[contains(@class, 'oxd-input-group')]//input"
        self.search_button = "//button[@type='submit' and normalize-space()='Search']"
        self.reset_button = "//button[contains(@class, 'oxd-button--ghost') and normalize-space()='Reset']"

    def navigate_to_users(self):
        self.page.click(self.admin_menu)
        # We might already be on the Admin -> User Management -> Users page
        # but just in case, we can ensure we are there.
        # Actually clicking "Admin" often goes straight to Users by default
        self.page.wait_for_url("**/viewSystemUsers")
        self.page.wait_for_selector(self.page_header)

    def select_dropdown(self, dropdown_locator, option_text):
        self.page.click(dropdown_locator)
        self.page.wait_for_selector("div[role='listbox']")
        self.page.click(f"div[role='option'] span:has-text('{option_text}')")

    def add_user(self, user_role, employee_name, status, username, password):
        self.page.click(self.add_button)
        self.page.wait_for_url("**/saveSystemUser")
        
        # Select Role
        self.select_dropdown(self.user_role_dropdown, user_role)
        
        # Type Employee Autocomplete
        self.page.fill(self.employee_name_autocomplete, employee_name)
        self.page.wait_for_selector("div[role='listbox']", timeout=5000)
        self.page.click(f"div[role='option'] span:has-text('{employee_name}')")
        
        # Select Status
        self.select_dropdown(self.status_dropdown, status)
        
        # Fill texts
        self.page.fill(self.username_input, username)
        self.page.fill(self.password_input, password)
        self.page.fill(self.confirm_password_input, password)
        
        # Blur just in case
        self.page.click("//h6")
        self.page.wait_for_timeout(500)
        
        self.page.click(self.save_button)
        self.page.wait_for_url("**/viewSystemUsers")
        self.page.wait_for_load_state("networkidle")

    def edit_user(self, current_username, new_username=None, new_role=None, new_status=None):
        self.page.wait_for_selector("div.oxd-table-body")
        
        # Find row by username text
        row = self.page.locator("div.oxd-table-row").filter(has_text=current_username)
        row.locator(self.edit_button).click()
        
        # Wait for edit page
        self.page.wait_for_url(re.compile(r".*saveSystemUser.*"))
        self.page.wait_for_load_state("networkidle")
        
        if new_role:
            self.select_dropdown(self.user_role_dropdown, new_role)
            
        if new_status:
            self.select_dropdown(self.status_dropdown, new_status)

        if new_username:
            username_field = self.page.locator(self.username_input)
            username_field.click(click_count=3)
            self.page.keyboard.press("Backspace")
            username_field.type(new_username, delay=100)
            
        self.page.click(self.save_button)
        self.page.wait_for_url("**/viewSystemUsers")
        self.page.wait_for_load_state("networkidle")

    def delete_user(self, username):
        row_xpath = f"//div[contains(@class, 'oxd-table-row') and .//div[text()='{username}']]"
        self.page.locator(row_xpath).locator("i.bi-trash").click()
        
        self.page.wait_for_timeout(2000)
        self.page.click(self.delete_confirm_button)
        self.page.wait_for_load_state("networkidle")

    def bulk_delete_users(self, usernames):
        # Select checkboxes for all given usernames
        for username in usernames:
            row_xpath = f"//div[contains(@class, 'oxd-table-row') and .//div[text()='{username}']]"
            # Using the established pattern from work_shifts_page.py
            self.page.locator(row_xpath).locator(".oxd-checkbox-wrapper span").click()
            self.page.wait_for_timeout(500)
            
        # Click Delete Selected
        self.page.click(self.delete_selected_button)
        
        self.page.wait_for_timeout(2000)
        self.page.click(self.delete_confirm_button)
        self.page.wait_for_load_state("networkidle")

    def search_by_username(self, username):
        self.page.fill(self.search_username_input, username)
        self.page.click(self.search_button)
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1000) # Give it a moment to filter

    def search_by_status(self, status):
        self.select_dropdown(self.status_dropdown, status)
        self.page.click(self.search_button)
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1000)

    def search_by_role(self, role_name):
        self.select_dropdown(self.user_role_dropdown, role_name)
        self.page.click(self.search_button)
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1000)

    def reset_search(self):
        self.page.click(self.reset_button)
        self.page.wait_for_load_state("networkidle")

    def is_no_records_found_visible(self):
        try:
            # Common OrangeHRM locator for empty table message
            self.page.wait_for_selector("//span[normalize-space()='No Records Found']", timeout=3000)
            return True
        except:
            return False

    def is_required_error_visible(self, field_name):
        locator = f"//label[contains(normalize-space(),'{field_name}')]/ancestor::div[contains(@class, 'oxd-input-group')]//span[contains(@class,'oxd-input-group__message') and text()='Required']"
        try:
            self.page.wait_for_selector(locator, timeout=3000)
            return True
        except:
            return False

    def is_already_exists_error_visible(self):
        locator = "//span[contains(@class,'oxd-input-group__message') and text()='Already exists']"
        try:
            self.page.wait_for_selector(locator, timeout=3000)
            return True
        except:
            return False

    def is_password_mismatch_error_visible(self):
        locator = "//span[contains(@class,'oxd-input-group__message') and text()='Passwords do not match']"
        try:
            self.page.wait_for_selector(locator, timeout=3000)
            return True
        except:
            return False

    def is_password_policy_error_visible(self):
        locator = "//span[contains(@class,'oxd-input-group__message') and text()='Should have at least 7 characters']"
        try:
            self.page.wait_for_selector(locator, timeout=3000)
            return True
        except:
            return False

    def is_user_present(self, username):
        self.page.wait_for_selector("div.oxd-table-body")
        rows = self.page.locator("div.oxd-table-body div.oxd-table-row")
        return rows.filter(has_text=username).count() > 0
