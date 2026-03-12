import os
from playwright.sync_api import sync_playwright

def inspect():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        # Login
        page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        page.wait_for_selector("input[name='username']")
        page.fill("input[name='username']", "Admin")
        page.fill("input[name='password']", "admin123")
        page.click("button[type='submit']")
        
        page.wait_for_url("**/dashboard/index")
        
        # Go to Admin -> User Management -> Users -> Add
        page.click("//span[normalize-space()='Admin']")
        page.wait_for_selector("//h5[normalize-space()='System Users']")
        page.click("//button[normalize-space()='Add']")
        page.wait_for_url("**/saveSystemUser")
        page.wait_for_timeout(2000)
        
        # Fill a weak password
        page.fill("//label[text()='Password']/../following-sibling::div//input", "weak")
        page.fill("//label[text()='Confirm Password']/../following-sibling::div//input", "weak")
        
        # Blur & try to get validation
        page.click("//h6")
        page.wait_for_timeout(1000)
        
        # Click save
        page.click("//button[@type='submit']")
        page.wait_for_timeout(1000)
        
        out = []
        try:
            # specifically under Password
            msg = page.locator("//label[text()='Password']/ancestor::div[contains(@class, 'oxd-input-group')]//span[contains(@class,'oxd-input-group__message')]").inner_text()
            out.append(f"Password error text: '{msg}'")
        except Exception as e:
            out.append(f"Error checking validation: {e}")
        
        with open("tests/inspect_out.txt", "w") as f:
            f.write("\n".join(out))

        browser.close()

if __name__ == "__main__":
    inspect()
