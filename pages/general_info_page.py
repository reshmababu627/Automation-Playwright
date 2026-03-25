from playwright.sync_api import Page

class GeneralInfoPage:
    def __init__(self, page: Page):
        self.page = page

        # Navigation
        self.admin_menu = "//span[normalize-space()='Admin']"
        self.organization_menu = "//span[normalize-space()='Organization']"
        self.general_info_menu = "//a[normalize-space()='General Information']"
        self.page_header = "//h6[normalize-space()='General Information']"

        # Form Fields
        self.edit_toggle = "//input[@type='checkbox']/following-sibling::span"
        self.organization_name_input = "//label[contains(normalize-space(),'Organization Name')]/following::input[1]"
        self.tax_id_input = "//label[contains(normalize-space(),'Tax ID')]/following::input[1]"
        self.registration_number_input = "//label[contains(normalize-space(),'Registration Number')]/following::input[1]"
        self.phone_input = "//label[contains(normalize-space(),'Phone')]/following::input[1]"
        self.fax_input = "//label[contains(normalize-space(),'Fax')]/following::input[1]"
        self.email_input = "//label[contains(normalize-space(),'Email')]/following::input[1]"
        self.address_street1_input = "//label[contains(normalize-space(),'Address Street 1')]/following::input[1]"
        self.address_street2_input = "//label[contains(normalize-space(),'Address Street 2')]/following::input[1]"
        self.city_input = "//label[contains(normalize-space(),'City')]/following::input[1]"
        self.state_province_input = "//label[contains(normalize-space(),'State/Province')]/following::input[1]"
        self.zip_postal_code_input = "//label[contains(normalize-space(),'Zip/Postal Code')]/following::input[1]"
        self.country_dropdown = "//label[contains(normalize-space(),'Country')]/following::div[contains(@class, 'oxd-select-text')]"
        self.save_button = "//button[@type='submit']"
        self.success_toast = "//div[contains(@class,'oxd-toast--success')]"

    def navigate_to_general_info(self):
        if "/viewOrganizationGeneralInformation" not in self.page.url:
            self.page.click(self.admin_menu, no_wait_after=True)
            # Wait for any Top Nav element to ensure page transition
            self.page.wait_for_selector(self.organization_menu, state="visible", timeout=20000)
            
            # Check if Organization menu needs to be clicked
            if not self.page.is_visible(self.general_info_menu):
                self.page.click(self.organization_menu, no_wait_after=True)
            
            # Wait for dropdown item with explicit visibility
            self.page.wait_for_selector(self.general_info_menu, state="visible", timeout=20000)
            self.page.click(self.general_info_menu, no_wait_after=True)
            self.page.wait_for_url("**/viewOrganizationGeneralInformation")
        
        self.page.wait_for_selector(self.page_header, state="visible", timeout=30000)

    def is_edit_enabled(self):
        # We can check if name input is disabled
        self.page.wait_for_timeout(2000)
        return not self.page.is_disabled(self.organization_name_input)

    def enable_edit(self):
        if not self.is_edit_enabled():
            self.page.click(self.edit_toggle)
            self.page.wait_for_timeout(1000) # Buffer for UI enablement

    def clear_organization_name(self):
        self.page.wait_for_timeout(2000)
        self.enable_edit()
       
        name_field = self.page.locator(self.organization_name_input)
        name_field.click(click_count=3)
        self.page.keyboard.press("Backspace")
        self.page.wait_for_timeout(500)

    def click_save(self):
        self.page.wait_for_timeout(2000)
        self.page.click(self.save_button)

    def is_required_error_visible(self, field_name):
        # Handle labels with or without asterisk
        locator = f"//label[contains(normalize-space(),'{field_name}')]/ancestor::div[contains(@class, 'oxd-input-group')]//span[contains(@class,'oxd-input-group__message') and text()='Required']"
        try:
            self.page.wait_for_selector(locator, timeout=3000)
            return True
        except:
            return False

    def update_general_info(self, **kwargs):
        self.page.wait_for_timeout(2000)
        self.enable_edit()
        self.page.wait_for_timeout(2000)
        field_mapping = {
        
            "name": self.organization_name_input,
            "tax_id": self.tax_id_input,
            "reg_num": self.registration_number_input,
            "phone": self.phone_input,
            "fax": self.fax_input,
            "email": self.email_input,
            "street1": self.address_street1_input,
            "street2": self.address_street2_input,
            "city": self.city_input,
            "state": self.state_province_input,
            "zip_code": self.zip_postal_code_input
        }

        for key, value in kwargs.items():
            if key in field_mapping and value is not None:
                self.page.wait_for_timeout(500)
                self.page.fill(field_mapping[key], value)
            elif key == "country" and value is not None:
                self.page.click(self.country_dropdown)
                self.page.click(f"div[role='listbox'] div[role='option'] span:has-text('{value}')")

        self.page.click(self.save_button)
        # Handle toast or just wait for load state if toast is unreliable
        try:
            self.page.wait_for_selector(self.success_toast, timeout=10000)
        except:
            print("Warning: Success toast not seen, waiting for load state instead.")
            self.page.wait_for_load_state("networkidle")

    def get_info_values(self):
        return {
            "name": self.page.input_value(self.organization_name_input),
            "tax_id": self.page.input_value(self.tax_id_input),
            "reg_num": self.page.input_value(self.registration_number_input),
            "phone": self.page.input_value(self.phone_input),
            "fax": self.page.input_value(self.fax_input),
            "email": self.page.input_value(self.email_input),
            "street1": self.page.input_value(self.address_street1_input),
            "street2": self.page.input_value(self.address_street2_input),
            "city": self.page.input_value(self.city_input),
            "state": self.page.input_value(self.state_province_input),
            "zip_code": self.page.input_value(self.zip_postal_code_input),
            "country": self.page.text_content(self.country_dropdown).strip()
        }

