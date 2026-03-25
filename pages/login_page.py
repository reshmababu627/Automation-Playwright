from playwright.sync_api import Page
class LoginPage:
    def __init__(self, page: Page):
        self.page = page

        #locators
        self.username_input = "//input[@name='username']"
        self.password_input = "//input[@name='password']"
        self.login_button = "//button[@type='submit']"
        self.invalid_credential_msg = "//p[text()='Invalid credentials']"
        self.input_error_msg = "//span[text()='Required']"
        
        # User Dropdown / Logout
        self.user_dropdown = "//span[@class='oxd-userdropdown-tab']"
        self.logout_link = "//a[text()='Logout']"

    def navigate(self, BASE_URL):
        self.page.goto(BASE_URL)
    def login(self, username, password):
        self.page.fill(self.username_input, username)
        self.page.fill(self.password_input, password)
        # Use no_wait_after=True to avoid timing out if navigation is slow/complex
        # We handle waiting for the target URL in authenticated_page fixture
        self.page.click(self.login_button, no_wait_after=True)
    
    def logout(self):
        self.page.click(self.user_dropdown)
        self.page.click(self.logout_link)
        self.page.wait_for_url("**/login")

    def get_invalid_credential_message(self):
        self.page.wait_for_selector(self.invalid_credential_msg)
        return self.page.inner_text(self.invalid_credential_msg)

    def get_input_error_message(self):
        # This might return multiple if both are empty, for now let's just get the first visible one or all
        self.page.wait_for_selector(self.input_error_msg)
        return self.page.inner_text(self.input_error_msg)
    
    def is_input_error_displayed(self):
        try:
            self.page.wait_for_selector(self.input_error_msg, state="visible", timeout=5000)
            return True
        except:
            return False 
      