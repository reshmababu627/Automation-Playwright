from playwright.sync_api import Page

class EmploymentStatusPage:
    def __init__(self, page: Page):
        self.page = page

        # Navigation
        self.admin_menu = "//span[normalize-space()='Admin']"
        self.job_menu = "//span[normalize-space()='Job']"
        self.employment_status_menu = "//a[normalize-space()='Employment Status']"
        self.page_header = "//h6[normalize-space()='Employment Status']"

        # Add / Edit Form
        self.add_button = "//button[normalize-space()='Add']"
        self.save_button = "//button[@type='submit']"
        self.cancel_button = "//button[normalize-space()='Cancel']"
        self.edit_button = "i.bi-pencil-fill"   
        
        # Form Fields
        self.name_input = "//label[text()='Name']/../following-sibling::div/input"

        # Table / Action
        self.delete_confirm_button = "//button[normalize-space()='Yes, Delete']"
        self.delete_selected_button = "//button[normalize-space()='Delete Selected']"
        self.error_message = "//span[contains(@class,'oxd-input-group__message')]"

    def navigate_to_employment_status(self):
        self.page.click(self.admin_menu)
        self.page.click(self.job_menu)
        self.page.click(self.employment_status_menu)
        self.page.wait_for_url("**/employmentStatus")
        self.page.wait_for_selector(self.page_header)

    def add_employment_status(self, name):
        self.page.click(self.add_button)
        self.page.wait_for_url("**/saveEmploymentStatus")
        
        self.page.fill(self.name_input, name)
        
        self.page.click(self.save_button)
        self.page.wait_for_url("**/employmentStatus")
        self.page.wait_for_load_state("networkidle")

    def is_employment_status_present(self, name):
        self.page.wait_for_selector("div.oxd-table-body")
        rows = self.page.locator("div.oxd-table-row")
        return rows.filter(has_text=name).count() > 0

    def edit_employment_status(self, current_name, new_name):
        # Find Row
        self.page.wait_for_selector("div.oxd-table-body")        
        # Click Edit (pencil)
        row = self.page.locator("div.oxd-table-row").filter(has_text=current_name)
        row.locator(self.edit_button).click()
        
        # wait for edit page
        self.page.wait_for_url("**/saveEmploymentStatus/**")
        self.page.wait_for_load_state("networkidle")

        # clear and update name
        self.page.fill(self.name_input, new_name)

        # save updated title
        self.page.click(self.save_button)   
        
        # Wait until we return to list page
        self.page.wait_for_url("**/employmentStatus")
        self.page.wait_for_selector("div.oxd-table-body")
        self.page.wait_for_load_state("networkidle")

    def delete_employment_status(self, name):
        # Find Row
        row_xpath = f"//div[contains(@class, 'oxd-table-row') and .//div[text()='{name}']]";
        
        # Click Delete (trash)
        self.page.locator(row_xpath).locator("i.bi-trash").click()
        
        self.page.wait_for_timeout(2000)
        self.page.click(self.delete_confirm_button)
        self.page.wait_for_load_state("networkidle")

    def click_cancel(self):
        self.page.click(self.cancel_button)
        self.page.wait_for_url("**/employmentStatus")

    def is_required_error_visible(self):
        try:
            self.page.wait_for_selector(f"{self.error_message}[text()='Required']", timeout=5000)
            return True
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

    def select_employment_statuses(self, names: list):
        for name in names:
            row_checkbox = f"//div[contains(@class, 'oxd-table-row') and .//div[text()='{name}']]//i[contains(@class, 'oxd-checkbox-input-icon')]"
            self.page.click(row_checkbox)

    def delete_selected(self):
        self.page.click(self.delete_selected_button)
        self.page.wait_for_timeout(1000)
        self.page.click(self.delete_confirm_button)
        self.page.wait_for_load_state("networkidle")
