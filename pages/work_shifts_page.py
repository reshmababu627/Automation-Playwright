from playwright.sync_api import Page

class WorkShiftsPage:
    def __init__(self, page: Page):
        self.page = page

        # Navigation
        self.admin_menu = "//span[normalize-space()='Admin']"
        self.job_menu = "//span[normalize-space()='Job']"
        self.work_shifts_menu = "//a[normalize-space()='Work Shifts']"
        self.page_header = "//h6[normalize-space()='Work Shifts']"

        # Add / Edit Form
        self.add_button = "//button[normalize-space()='Add']"
        self.save_button = "//button[@type='submit']"
        self.cancel_button = "//button[normalize-space()='Cancel']"
        self.edit_button = "i.bi-pencil-fill"   
        
        # Form Fields
        self.name_input = "//label[text()='Shift Name']/../following-sibling::div/input"
        self.from_time_input = "//label[text()='From']/../following-sibling::div//input"
        self.to_time_input = "//label[text()='To']/../following-sibling::div//input"
        self.assigned_employees_input = "//label[text()='Assigned Employees']/../following-sibling::div//input"
      
        # Table / Action
        self.delete_confirm_button = "//button[normalize-space()='Yes, Delete']"
        self.delete_selected_button = "//button[normalize-space()='Delete Selected']"
        self.error_message = "//span[contains(@class,'oxd-input-group__message')]"

    def navigate_to_work_shifts(self):
        self.page.click(self.admin_menu)
        self.page.click(self.job_menu)
        self.page.click(self.work_shifts_menu)
        self.page.wait_for_url("**/workShift")
        self.page.wait_for_selector(self.page_header)

    def add_work_shift(self, name, from_time="09:00 AM", to_time="05:00 PM", employees=None):
        self.page.click(self.add_button)
        self.page.wait_for_url("**/saveWorkShift*")
        
        self.page.fill(self.name_input, name)
        
        # Set From and To time
        from_input = self.page.locator(self.from_time_input)
        from_input.clear()
        if from_time:
            from_input.type(from_time, delay=100)
        from_input.press("Escape")
        
        to_input = self.page.locator(self.to_time_input)
        to_input.clear()
        if to_time:
            to_input.type(to_time, delay=100)
        to_input.press("Escape")
        # fill assigned employees
        if employees:
            self.page.fill(self.assigned_employees_input, employees)
            # Wait for autocomplete dropdown listbox
            self.page.wait_for_selector("div[role='listbox']", timeout=5000)
            # Click the option that contains the typed name
            self.page.click(f"div[role='option'] span:has-text('{employees}')")
        self.page.wait_for_timeout(500)
        
        self.page.click(self.save_button)
        self.page.wait_for_url("**/workShift")
        self.page.wait_for_load_state("networkidle")

    def is_work_shift_present(self, name):
        self.page.wait_for_selector("div.oxd-table-body")
        rows = self.page.locator("div.oxd-table-row")
        return rows.filter(has_text=name).count() > 0

    def edit_work_shift(self, current_name, new_name):
        # Find Row
        self.page.wait_for_selector("div.oxd-table-body")        
        # Click Edit (pencil)
        row = self.page.locator("div.oxd-table-row").filter(has_text=current_name)
        row.locator(self.edit_button).click()
        
        # Wait for edit page
        import re
        self.page.wait_for_url(re.compile(r".*saveWorkShift.*"))
        self.page.wait_for_load_state("networkidle")

        # Clear and fill updated name
        self.page.fill(self.name_input, new_name)

        # Save updated shift
        self.page.click(self.save_button)   
        
        # Wait until we return to list page
        self.page.wait_for_url("**/workShift")
        self.page.wait_for_selector("div.oxd-table-body")
        self.page.wait_for_load_state("networkidle")

    def delete_work_shift(self, name):
        # Find Row
        row_xpath = f"//div[contains(@class, 'oxd-table-row') and .//div[text()='{name}']]"
        
        # Click Delete (trash)
        self.page.locator(row_xpath).locator("i.bi-trash").click()
        
        self.page.wait_for_timeout(2000)
        self.page.click(self.delete_confirm_button)
        self.page.wait_for_load_state("networkidle")

    def bulk_delete_work_shifts(self, names):
        # Select checkboxes for all given work shifts
        for name in names:
            row_xpath = f"//div[contains(@class, 'oxd-table-row') and .//div[text()='{name}']]"
            self.page.locator(row_xpath).locator(".oxd-checkbox-wrapper span").click()
            self.page.wait_for_timeout(500)
            
        # Click Delete Selected
        self.page.click(self.delete_selected_button)
        
        self.page.wait_for_timeout(2000)
        self.page.click(self.delete_confirm_button)
        self.page.wait_for_load_state("networkidle")

    def is_required_error_visible(self, field_name):
        locator = f"//label[text()='{field_name}']/ancestor::div[contains(@class, 'oxd-input-group')]//span[contains(@class,'oxd-input-group__message') and text()='Required']"
        try:
            self.page.wait_for_selector(locator, timeout=5000)
            return True
        except:
            return False

    def is_time_range_error_visible(self):
        try:
            self.page.wait_for_selector(self.error_message, timeout=5000)
            errors = self.page.locator(self.error_message).all_text_contents()
            for error in errors:
                if "To time should be after from time" in error:
                    return True
            return False
        except:
            return False

    def is_already_exists_error_visible(self):
        try:
            self.page.wait_for_selector(self.error_message, timeout=5000)
            errors = self.page.locator(self.error_message).all_text_contents()
            for error in errors:
                if "already exists" in error.lower():
                    return True
            return False
        except:
            return False
