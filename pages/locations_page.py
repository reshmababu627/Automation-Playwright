from playwright.sync_api import Page, TimeoutError
import re

class LocationsPage:
    def __init__(self, page: Page):
        self.page = page

        # Navigation
        self.admin_menu = "//span[normalize-space()='Admin']"
        self.organization_menu = "//span[normalize-space()='Organization']"
        self.locations_menu = "//a[normalize-space()='Locations']"
        self.locations_page_header = "//h5[normalize-space()='Locations']"

        # Add / Edit Form
        self.add_button = "//button[normalize-space()='Add']"
        self.save_button = "//button[@type='submit']"
        self.cancel_button = "//button[normalize-space()='Cancel']"
        self.edit_button = "//i[@class='oxd-icon bi-pencil-fill']"
        
        # Form Fields
        self.name_input = "//label[text()='Name']/../following-sibling::div/input"
        self.city_input = "//label[text()='City']/../following-sibling::div/input"
        self.country_dropdown = "//label[text()='Country']/../following-sibling::div//div[@class='oxd-select-text-input']"
        self.province_input = "//label[text()='State/Province']/../following-sibling::div/input"
        self.zip_input = "//label[text()='Zip/Postal Code']/../following-sibling::div/input"
        self.phone_input = "//label[text()='Phone']/../following-sibling::div/input"
        self.fax_input = "//label[text()='Fax']/../following-sibling::div/input"
        self.address_input = "//label[text()='Address']/../following-sibling::div/textarea"
        self.notes_input = "//label[text()='Notes']/../following-sibling::div/textarea"
        self.state_input = "//label[text()='State/Province']/../following-sibling::div/input"

        self.success_saved = "//div[contains(@class,'oxd-toast--success')]"
        self.delete_confirm_button = "//button[normalize-space()='Yes, Delete']"
        self.delete_selected_button = "//button[normalize-space()='Delete Selected']"
        self.error_message = "//span[contains(@class,'oxd-input-group__message')]"

    # ---------------- Navigation ----------------
    def navigate_to_locations(self):
        if "/viewLocations" not in self.page.url:
            self.page.click(self.admin_menu)
            self.page.click(self.organization_menu)
            self.page.click(self.locations_menu)
            self.page.wait_for_url("**/viewLocations")
        
        self.page.wait_for_selector(self.locations_page_header)
        self.page.wait_for_selector(self.add_button, state="visible", timeout=20000)

    # ---------------- ADD LOCATION ---------------- #
    def add_location(self, name, city=None, province=None, zip_code=None, country=None, phone=None, fax=None, address=None, notes=None):
        self.page.click(self.add_button)
        self.page.wait_for_url("**/saveLocation*")

        self.page.fill(self.name_input, name)
        self.page.wait_for_timeout(500)
        
        if city:

            self.page.fill(self.city_input, city)
            self.page.wait_for_timeout(500)
        
        
        
        if province:
            self.page.wait_for_timeout(500)
            self.page.fill(self.province_input, province)
        if zip_code:
            self.page.wait_for_timeout(500)
            self.page.fill(self.zip_input, zip_code)
    # Select Country
        self.page.click(self.country_dropdown)
        self.page.click(f"div[role='listbox'] div[role='option'] span:has-text('{country}')")
        self.page.wait_for_timeout(500)
        
        if phone:
            self.page.wait_for_timeout(500)
            self.page.fill(self.phone_input, phone)

        if fax:
            self.page.wait_for_timeout(500)
            self.page.fill(self.fax_input, fax)
       
        if address:
            self.page.wait_for_timeout(500)
            self.page.fill(self.address_input, address)
       
        if notes:
            self.page.wait_for_timeout(500)
            self.page.fill(self.notes_input, notes)
        

            
        self.page.click(self.save_button)
        #wait for success message
        self.page.wait_for_url("**/viewLocations", timeout=60000)
        self.page.wait_for_load_state("networkidle")


    def is_locations_page_loaded(self):
        self.page.wait_for_selector(self.locations_page_header, timeout=10000)
        return True

    def is_location_present(self, name):
        self.page.wait_for_selector("div.oxd-table-body")
        rows = self.page.locator("div.oxd-table-row")
        return rows.filter(has_text=name).count() > 0

    def is_required_error_visible(self, field_name):
        locator = f"//label[text()='{field_name}']/ancestor::div[contains(@class, 'oxd-input-group')]//span[contains(@class,'oxd-input-group__message') and text()='Required']"
        try:
            self.page.wait_for_selector(locator, timeout=5000)
            return True
        except:
            return False

    def click_cancel(self):
        self.page.click(self.cancel_button)
        self.page.wait_for_url("**/viewLocations")

    def is_duplicate_error_visible(self):
        try:
            self.page.wait_for_selector(self.error_message, timeout=5000)
            errors = self.page.locator(self.error_message).all_text_contents()
            for error in errors:
                if "already exists" in error.lower():
                    return True
            return False
        except:
            return False

    def select_locations(self, names: list):
        for name in names:
            row_checkbox = f"//div[contains(@class, 'oxd-table-row') and .//div[text()='{name}']]//i[contains(@class, 'oxd-checkbox-input-icon')]"
            self.page.click(row_checkbox)

    def delete_selected(self):
        self.page.click(self.delete_selected_button)
        self.page.wait_for_timeout(1000)
        self.page.click(self.delete_confirm_button)
        self.page.wait_for_load_state("networkidle")

    def delete_location(self, name):
        row_xpath = f"//div[contains(@class, 'oxd-table-row') and .//div[text()='{name}']]"
        self.page.locator(row_xpath).locator("i.bi-trash").click()
        self.page.wait_for_timeout(2000)
        self.page.click(self.delete_confirm_button)
        self.page.wait_for_load_state("networkidle")

    def edit_location(self, old_name, new_name):
        self.page.wait_for_selector("div.oxd-table-body")
        row = self.page.locator("div.oxd-table-row").filter(has_text=old_name)
        row.locator(self.edit_button).click()
        self.page.wait_for_url("**/saveLocation/**")
        self.page.wait_for_load_state("networkidle")
        self.page.fill(self.name_input, new_name)
        self.page.click(self.save_button)
        self.page.wait_for_url("**/viewLocations")
        self.page.wait_for_selector("div.oxd-table-body")
        self.page.wait_for_load_state("networkidle")

   