import pytest
import random
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.user_management_page import UserManagementPage

class TestUserManagement:
    username_to_test = None
    employee_to_assign = "a" # We'll just type 'a' to get the first available employee

    @pytest.fixture(autouse=True)
    def setup(self, authenticated_page: Page):
        self.login_page = LoginPage(authenticated_page)
        self.user_mgt_page = UserManagementPage(authenticated_page)

    def generate_random_username(self):
        return f"TestUser_{random.randint(10000, 99999)}"

    def test_add_user(self, authenticated_page: Page):
        self.user_mgt_page.navigate_to_users()
        TestUserManagement.username_to_test = self.generate_random_username()
        print(f"Testing Add User: {TestUserManagement.username_to_test}")
        
        # Add User
        self.user_mgt_page.add_user(
            user_role="Admin",
            employee_name=self.employee_to_assign,
            status="Enabled",
            username=TestUserManagement.username_to_test,
            password="TestPassword123!"
        )
        
        # Verify
        assert self.user_mgt_page.is_user_present(TestUserManagement.username_to_test), f"User {TestUserManagement.username_to_test} not found after adding!"

    def test_add_user_empty(self, authenticated_page: Page):
        # self.user_mgt_page.navigate_to_users() # Uncomment if running isolated
        authenticated_page.wait_for_timeout(2000)
        
        # Click Add
        self.user_mgt_page.page.click(self.user_mgt_page.add_button)
        self.user_mgt_page.page.wait_for_url("**/saveSystemUser*")
        
        # Click Save without filling anything
        self.user_mgt_page.page.click(self.user_mgt_page.save_button)
        
        # Verify required errors
        assert self.user_mgt_page.is_required_error_visible("User Role"), "Required error not visible for User Role"
        assert self.user_mgt_page.is_required_error_visible("Employee Name"), "Required error not visible for Employee Name"
        assert self.user_mgt_page.is_required_error_visible("Status"), "Required error not visible for Status"
        assert self.user_mgt_page.is_required_error_visible("Username"), "Required error not visible for Username"
        assert self.user_mgt_page.is_required_error_visible("Password"), "Required error not visible for Password"
        
        # Cleanup
        self.user_mgt_page.page.click(self.user_mgt_page.cancel_button)
        self.user_mgt_page.page.wait_for_url("**/viewSystemUsers")

    def test_add_user_duplicate(self, authenticated_page: Page):
        authenticated_page.wait_for_timeout(2000)
        assert TestUserManagement.username_to_test is not None, "Setup failed: No existing user to duplicate!"
        
        # Click Add
        self.user_mgt_page.page.click(self.user_mgt_page.add_button)
        self.user_mgt_page.page.wait_for_url("**/saveSystemUser*")
        
        # Fill existing username and other mandatory fields
        self.user_mgt_page.select_dropdown(self.user_mgt_page.user_role_dropdown, "Admin")
        
        self.user_mgt_page.page.fill(self.user_mgt_page.employee_name_autocomplete, self.employee_to_assign)
        self.user_mgt_page.page.wait_for_selector("div[role='listbox']", timeout=5000)
        self.user_mgt_page.page.click(f"div[role='option'] span:has-text('{self.employee_to_assign}')")
        
        self.user_mgt_page.select_dropdown(self.user_mgt_page.status_dropdown, "Enabled")
        
        # This is the existing username
        self.user_mgt_page.page.fill(self.user_mgt_page.username_input, TestUserManagement.username_to_test)
        self.user_mgt_page.page.fill(self.user_mgt_page.password_input, "TestPassword123!")
        self.user_mgt_page.page.fill(self.user_mgt_page.confirm_password_input, "TestPassword123!")
        
        # Blur
        self.user_mgt_page.page.click("//h6")
        self.user_mgt_page.page.wait_for_timeout(500)
        
        # Click Save
        self.user_mgt_page.page.click(self.user_mgt_page.save_button)
        
        # Verify already exists error
        assert self.user_mgt_page.is_already_exists_error_visible(), f"Already exists error not visible for duplicate user '{TestUserManagement.username_to_test}'!"
        
        # Cleanup
        self.user_mgt_page.page.click(self.user_mgt_page.cancel_button)
        self.user_mgt_page.page.wait_for_url("**/viewSystemUsers")

    def test_add_user_password_mismatch(self, authenticated_page: Page):
        authenticated_page.wait_for_timeout(2000)
        
        # Click Add
        self.user_mgt_page.page.click(self.user_mgt_page.add_button)
        self.user_mgt_page.page.wait_for_url("**/saveSystemUser*")
        
        # Fill mandatory fields
        self.user_mgt_page.select_dropdown(self.user_mgt_page.user_role_dropdown, "Admin")
        
        self.user_mgt_page.page.fill(self.user_mgt_page.employee_name_autocomplete, self.employee_to_assign)
        self.user_mgt_page.page.wait_for_selector("div[role='listbox']", timeout=5000)
        self.user_mgt_page.page.click(f"div[role='option'] span:has-text('{self.employee_to_assign}')")
        
        self.user_mgt_page.select_dropdown(self.user_mgt_page.status_dropdown, "Enabled")
        
        # Fill randomly generated username
        random_username = self.generate_random_username()
        self.user_mgt_page.page.fill(self.user_mgt_page.username_input, random_username)
        
        # Fill mismatched passwords
        self.user_mgt_page.page.fill(self.user_mgt_page.password_input, "Password123!")
        self.user_mgt_page.page.fill(self.user_mgt_page.confirm_password_input, "DifferentPass123!")
        
        # Blur
        self.user_mgt_page.page.click("//h6")
        self.user_mgt_page.page.wait_for_timeout(500)
        
        # Click Save
        self.user_mgt_page.page.click(self.user_mgt_page.save_button)
        
        # Verify mismatch error
        assert self.user_mgt_page.is_password_mismatch_error_visible(), "Password mismatch error not visible!"
        
        # Cleanup
        self.user_mgt_page.page.click(self.user_mgt_page.cancel_button)
        self.user_mgt_page.page.wait_for_url("**/viewSystemUsers")

    def test_add_user_password_policy(self, authenticated_page: Page):
        authenticated_page.wait_for_timeout(2000)
        
        # Click Add
        self.user_mgt_page.page.click(self.user_mgt_page.add_button)
        self.user_mgt_page.page.wait_for_url("**/saveSystemUser*")
        
        # Fill mandatory fields
        self.user_mgt_page.select_dropdown(self.user_mgt_page.user_role_dropdown, "Admin")
        
        self.user_mgt_page.page.fill(self.user_mgt_page.employee_name_autocomplete, self.employee_to_assign)
        self.user_mgt_page.page.wait_for_selector("div[role='listbox']", timeout=5000)
        self.user_mgt_page.page.click(f"div[role='option'] span:has-text('{self.employee_to_assign}')")
        
        self.user_mgt_page.select_dropdown(self.user_mgt_page.status_dropdown, "Enabled")
        
        # Fill randomly generated username
        random_username = self.generate_random_username()
        self.user_mgt_page.page.fill(self.user_mgt_page.username_input, random_username)
        
        # Fill weak password
        self.user_mgt_page.page.fill(self.user_mgt_page.password_input, "weak")
        self.user_mgt_page.page.fill(self.user_mgt_page.confirm_password_input, "weak")
        
        # Blur
        self.user_mgt_page.page.click("//h6")
        self.user_mgt_page.page.wait_for_timeout(500)
        
        # Click Save (often required to trigger the policy check fully)
        self.user_mgt_page.page.click(self.user_mgt_page.save_button)
        
        # Verify policy error
        assert self.user_mgt_page.is_password_policy_error_visible(), "Password policy error not visible for weak password!"
        
        # Cleanup
        self.user_mgt_page.page.click(self.user_mgt_page.cancel_button)
        self.user_mgt_page.page.wait_for_url("**/viewSystemUsers")

    def test_edit_user(self, authenticated_page: Page):
        authenticated_page.wait_for_timeout(2000)
        assert TestUserManagement.username_to_test is not None, "Setup failed: No user to edit!"
        
        current_username = TestUserManagement.username_to_test
        print(f"Editing User Role for: {current_username}")
        
        # Edit User (change role to ESS)
        self.user_mgt_page.edit_user(
            current_username=current_username,
            new_role="ESS"
        )
        
        # Verify user still exists (save completed successfully)
        assert self.user_mgt_page.is_user_present(current_username), f"User {current_username} not found after edit!"

    def test_disable_user(self, authenticated_page: Page):
        authenticated_page.wait_for_timeout(2000)
        
        # Ensure we have a user to disable
        if TestUserManagement.username_to_test is None:
            self.test_add_user(authenticated_page)
            
        user_to_disable = TestUserManagement.username_to_test
        print(f"Disabling User: {user_to_disable}")
        
        # Disable User
        self.user_mgt_page.edit_user(
            current_username=user_to_disable,
            new_status="Disabled"
        )
        
        # Verify status - this is tricky without a specific method, 
        # but if save was successful and we are back on the view page, 
        # we can assume the flow worked. For deeper verification, we'd need to check the row text.
        assert self.user_mgt_page.is_user_present(user_to_disable), f"User {user_to_disable} not found after disabling!"
        
        # Additional verification: Check if "Disabled" text is present in the row
        row = self.user_mgt_page.page.locator("div.oxd-table-row").filter(has_text=user_to_disable)
        expect(row).to_contain_text("Disabled")

    def test_bulk_delete_users(self, authenticated_page: Page):
        self.user_mgt_page.navigate_to_users()
        authenticated_page.wait_for_timeout(2000)
        
        # Create two test users
        user1 = self.generate_random_username()
        user2 = self.generate_random_username()
        
        print(f"Creating users for bulk delete: {user1}, {user2}")
        
        for u in [user1, user2]:
            self.user_mgt_page.add_user(
                user_role="Admin",
                employee_name=self.employee_to_assign,
                status="Enabled",
                username=u,
                password="TestPassword123!"
            )
            authenticated_page.wait_for_timeout(1000)
            
        # Bulk Delete
        self.user_mgt_page.bulk_delete_users([user1, user2])
        
        # Verify
        assert not self.user_mgt_page.is_user_present(user1), f"User {user1} still exists after bulk deletion!"
        assert not self.user_mgt_page.is_user_present(user2), f"User {user2} still exists after bulk deletion!"

    def test_search_user_by_username(self, authenticated_page: Page):
        self.user_mgt_page.navigate_to_users()
        authenticated_page.wait_for_timeout(2000)
        
        # Create a unique user to search for
        test_username = self.generate_random_username()
        print(f"Creating user for search test: {test_username}")
        
        self.user_mgt_page.add_user(
            user_role="Admin",
            employee_name=self.employee_to_assign,
            status="Enabled",
            username=test_username,
            password="TestPassword123!"
        )
        
        # Search for the user
        print(f"Searching for user: {test_username}")
        self.user_mgt_page.search_by_username(test_username)
        
        # Verify result
        assert self.user_mgt_page.is_user_present(test_username), f"User {test_username} not found after search!"
        
        # Optionally verify that only 1 record is shown or that the table size is reduced
        rows = self.user_mgt_page.page.locator("div.oxd-table-row")
        row_count = rows.count()
        print(f"Rows found after search: {row_count}")
        # Note: sometimes there might be multiple rows if the username is a substring of others, 
        # but here we generate unique ones. Check for at least 1 and maybe exact match if possible.
        
        # Cleanup (Delete the user so we don't clutter)
        self.user_mgt_page.reset_search()
        self.user_mgt_page.delete_user(test_username)

    def test_search_user_by_role(self, authenticated_page: Page):
        self.user_mgt_page.navigate_to_users()
        authenticated_page.wait_for_timeout(2000)
        
        role_to_search = "Admin"
        print(f"Searching for users with role: {role_to_search}")
        
        # Perform search
        self.user_mgt_page.search_by_role(role_to_search)
        
        # Verify results
        # We check the 'User Role' column in the table rows
        rows = self.user_mgt_page.page.locator("div.oxd-table-body div.oxd-table-row")
        count = rows.count()
        print(f"Found {count} users with role {role_to_search}")
        
        # If there are results, verify at least the first one has the correct role
        if count > 0:
            # The 'User Role' column is typically the 3rd column (index 2)
            # But let's check for text containment in the row
            for i in range(min(count, 5)): # Check first 5 results
                expect(rows.nth(i)).to_contain_text(role_to_search)
        else:
            print("No users found with the specified role, but search completed.")

        # Cleanup
        self.user_mgt_page.reset_search()

    def test_search_user_by_status(self, authenticated_page: Page):
        self.user_mgt_page.navigate_to_users()
        authenticated_page.wait_for_timeout(2000)
        
        status_to_search = "Enabled"
        print(f"Searching for users with status: {status_to_search}")
        
        # Perform search
        self.user_mgt_page.search_by_status(status_to_search)
        
        # Verify results
        rows = self.user_mgt_page.page.locator("div.oxd-table-body div.oxd-table-row")
        count = rows.count()
        print(f"Found {count} users with status {status_to_search}")
        
        if count > 0:
            for i in range(min(count, 5)):
                expect(rows.nth(i)).to_contain_text(status_to_search)
        else:
            print("No users found with the specified status.")

    def test_search_non_existing_user(self, authenticated_page: Page):
        self.user_mgt_page.navigate_to_users()
        authenticated_page.wait_for_timeout(2000)
        
        non_existing_username = f"NonExistent_{random.randint(1000000, 9999999)}"
        print(f"Searching for non-existing user: {non_existing_username}")
        
        # Perform search
        self.user_mgt_page.search_by_username(non_existing_username)
        
        # Verify result
        assert self.user_mgt_page.is_no_records_found_visible(), " 'No Records Found' message not visible for non-existing user!"
        
        # Reset search for next tests
        self.user_mgt_page.reset_search()

    def test_delete_user(self, authenticated_page: Page):
        authenticated_page.wait_for_timeout(2000)
        assert TestUserManagement.username_to_test is not None, "Setup failed: No user to delete!"
        
        user_to_delete = TestUserManagement.username_to_test
        print(f"Deleting User: {user_to_delete}")
        
        # Delete User
        self.user_mgt_page.delete_user(user_to_delete)
        
        # Reset state
        TestUserManagement.username_to_test = None
        
        # Verify
        assert not self.user_mgt_page.is_user_present(user_to_delete), f"User {user_to_delete} still exists after deletion!"
