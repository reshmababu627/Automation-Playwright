from playwright.sync_api import Page, TimeoutError

class JobPage:
    def __init__(self, page: Page):
        self.page = page

        # LEFT SIDE MENU (NEW ORANGEHRM UI)
        self.admin_menu = "//span[normalize-space()='Admin']"
        self.job_menu = "//span[normalize-space()='Job']"
        self.job_titles_option = "//a[normalize-space()='Job Titles']"

        # 
        self.job_page_header = "//h6[text()='Job Titles']"
        self.add_button = "//button[normalize-space()='Add']"
        self.save_button = "//button[@type='submit']"
        self.job_title_input = "//label[text()='Job Title']/../following-sibling::div/input"
        self.job_description_input = "//label[text()='Job Description']/../following-sibling::div/textarea"

        self.success_saved= "//div[contains(@class,'oxd-toast--success')]"
        self.job_table = "//div[@class='orangehrm-container']"
        self.delete_confirm_button = "//button[normalize-space()='Yes, Delete']"
        self.cancel_button = "//button[normalize-space()='Cancel']"
        self.error_message = "//span[contains(@class,'oxd-input-group__message')]"
        self.delete_selected_button = "//button[normalize-space()='Delete Selected']"
        self.job_specification_input = "input[type='file']"

    #edit locators
        self.edit_button = "//i[@class='oxd-icon bi-pencil-fill']"
        self.edit_job_title_input = "//label[text()='Job Title']/../following-sibling::div/input"
        self.edit_save_button = "//button[@type='submit']"  

    # ---------------- Navigation ----------------
    def navigate_to_job_titles(self):   
        self.page.click(self.admin_menu, no_wait_after=True)    
        self.page.click(self.job_menu, no_wait_after=True) 
        self.page.click(self.job_titles_option, no_wait_after=True) 
        self.page.wait_for_url("**/viewJobTitleList")
        self.page.wait_for_selector(self.job_page_header)

     # ---------------- ADD JOB ---------------- #

    # Add Job
    # -------------------------------

    def add_job(self, title: str, description: str = ""):
        self.page.click(self.add_button)
        self.page.wait_for_url("**/saveJobTitle")
        self.page.fill(self.job_title_input, title)

        if description:
            self.page.fill(self.job_description_input, description)

        self.page.click(self.save_button)

        # Wait for success message
        self.page.wait_for_url("**/viewJobTitleList")
        self.page.wait_for_load_state("networkidle")

    def is_job_page_loaded(self):
        self.page.wait_for_selector(self.job_page_header, timeout=10000)
        return True
    

    
    def is_job_present(self, title: str):
        self.page.wait_for_selector("div.oxd-table-body")
        rows = self.page.locator("div.oxd-table-row")
        return rows.filter(has_text=title).count() > 0

  

    def is_file_type_error_visible(self):
        try:
            # Wait for any potential error message to appear (span or toast)
            any_message_selector = "//span[contains(@class,'oxd-input-group__message')] | //div[contains(@class,'oxd-toast')]"
            self.page.wait_for_selector(any_message_selector, timeout=5000)
            
            error_spans = self.page.locator("//span[contains(@class,'oxd-input-group__message')]").all_text_contents()
            toasts = self.page.locator("//div[contains(@class,'oxd-toast')]").all_text_contents()
            
            for msg in error_spans + toasts:
                msg_lower = msg.lower()
                if "not supported" in msg_lower or "not allowed" in msg_lower or "invalid" in msg_lower:
                    return True
            return False
        except:
            return False

    def edit_job(self, original_title: str, new_title: str):
          # Wait for table
        self.page.wait_for_selector("div.oxd-table-body")
        # Click edit icon of matching row
        row = self.page.locator("div.oxd-table-row").filter(has_text=original_title)

        row.locator(self.edit_button).click()
        # Wait for edit page
        self.page.wait_for_url("**/saveJobTitle/**")
        self.page.wait_for_load_state("networkidle")
        # Clear and fill updated title
        self.page.fill(self.job_title_input, new_title)
        #save updated title
        self.page.click(self.save_button) 
        # Wait until we return to list page
        self.page.wait_for_url("**/viewJobTitleList")
        # wait for table reload
        self.page.wait_for_selector("div.oxd-table-body")
        self.page.wait_for_load_state("networkidle")


    def delete_job(self, title: str):
         # Find Row
        row_xpath = f"//div[contains(@class, 'oxd-table-row') and .//div[text()='{title}']]";
        
        # Click Delete (trash)
        self.page.locator(row_xpath).locator("i.bi-trash").click()
        
        self.page.wait_for_timeout(2000)
        self.page.click(self.delete_confirm_button)
        self.page.wait_for_load_state("networkidle")

    def click_cancel(self):
        self.page.click(self.cancel_button)
        self.page.wait_for_url("**/viewJobTitleList")

    def is_required_error_visible(self):
        try:
            self.page.wait_for_selector(f"{self.error_message}[text()='Required']", timeout=5000)
            return True
        except:
            return False

    def is_duplicate_error_visible(self):
        try:
            # Wait for either field error span OR toast message
            error_selector = f"{self.error_message} | //div[contains(@class,'oxd-toast-content')]"
            self.page.wait_for_selector(error_selector, timeout=5000)
            
            # Check field errors
            errors = self.page.locator(self.error_message).all_text_contents()
            # Check toasts
            toasts = self.page.locator("//div[contains(@class,'oxd-toast-content')]").all_text_contents()
            
            for msg in errors + toasts:
                if "already exists" in msg.lower():
                    return True
            return False
        except:
            return False

    def select_job_titles(self, titles: list):
        for title in titles:
            row_checkbox = f"//div[contains(@class, 'oxd-table-row') and .//div[text()='{title}']]//i[contains(@class, 'oxd-checkbox-input-icon')]"
            self.page.click(row_checkbox)

    def delete_selected(self):
        self.page.click(self.delete_selected_button)
        self.page.click(self.delete_confirm_button)
        self.page.wait_for_load_state("networkidle")

    def upload_job_specification(self, file_path: str):
        self.page.set_input_files(self.job_specification_input, file_path)

    