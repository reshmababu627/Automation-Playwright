import pytest
import random
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.work_shifts_page import WorkShiftsPage

class TestWorkShifts:
    shift_name = None

    @pytest.fixture(autouse=True)
    def setup(self, authenticated_page: Page):
        self.login_page = LoginPage(authenticated_page)
        self.work_shifts_page = WorkShiftsPage(authenticated_page)
        # Handle navigation centrally; POM handles conditional check
        self.work_shifts_page.navigate_to_work_shifts()

    def generate_random_name(self):
        return f"WorkShift_{random.randint(1000, 9999)}"

    def test_add_work_shift(self, authenticated_page: Page):
        TestWorkShifts.shift_name = self.generate_random_name()
        print(f"Testing Add Work Shift: {TestWorkShifts.shift_name}")
        self.work_shifts_page.add_work_shift(TestWorkShifts.shift_name)
        # Verify
        assert self.work_shifts_page.is_work_shift_present(TestWorkShifts.shift_name), f"Work Shift {TestWorkShifts.shift_name} not found after adding!"

    def test_add_work_shift_with_employee(self, authenticated_page: Page):
        # Buffer wait for Jenkins stability if needed, though POM handles most
        authenticated_page.wait_for_timeout(1000)
        TestWorkShifts.shift_name = self.generate_random_name()
        employee_to_assign = "a" # Typing 'a' to get any record
        
        # Add Work Shift with Employee
        self.work_shifts_page.add_work_shift(TestWorkShifts.shift_name, employees=employee_to_assign)
        
        # Verify
        assert self.work_shifts_page.is_work_shift_present(TestWorkShifts.shift_name), f"Work Shift {TestWorkShifts.shift_name} not found!"

    def test_add_work_shift_empty(self, authenticated_page: Page):
        authenticated_page.wait_for_timeout(1000)
        
        # Click Add
        self.work_shifts_page.page.click(self.work_shifts_page.add_button)
        self.work_shifts_page.page.wait_for_url("**/saveWorkShift*", timeout=30000)
        
        # Click Save without filling anything
        self.work_shifts_page.page.click(self.work_shifts_page.save_button)
        
        # Verify required error
        assert self.work_shifts_page.is_required_error_visible("Shift Name"), "Required error message not visible!"
        
        # Cleanup
        self.work_shifts_page.page.click(self.work_shifts_page.cancel_button)
        self.work_shifts_page.page.wait_for_url("**/workShift")

    def test_add_work_shift_without_time(self, authenticated_page: Page):
        authenticated_page.wait_for_timeout(1000)
        
        # Click Add
        self.work_shifts_page.page.click(self.work_shifts_page.add_button)
        self.work_shifts_page.page.wait_for_url("**/saveWorkShift*", timeout=30000)
        
        # Fill only name
        random_name = self.generate_random_name()
        self.work_shifts_page.page.fill(self.work_shifts_page.name_input, random_name)
        
        # Clear times
        from_input = self.work_shifts_page.page.locator(self.work_shifts_page.from_time_input)
        from_input.clear()
        to_input = self.work_shifts_page.page.locator(self.work_shifts_page.to_time_input)
        to_input.clear()
        
        # Blur
        self.work_shifts_page.page.click("//h6")
        
        # Click Save
        self.work_shifts_page.page.click(self.work_shifts_page.save_button)
        
        # Verify required error
        assert not self.work_shifts_page.is_required_error_visible("Shift Name"), "Shift Name should not have an error!"
        assert self.work_shifts_page.is_required_error_visible("From"), "From time required error missing!"
        assert self.work_shifts_page.is_required_error_visible("To"), "To time required error missing!"
        
        # Cleanup
        self.work_shifts_page.page.click(self.work_shifts_page.cancel_button)
        self.work_shifts_page.page.wait_for_url("**/workShift")

    def test_add_work_shift_invalid_time_range(self, authenticated_page: Page):
        authenticated_page.wait_for_timeout(1000)
        
        # Click Add
        self.work_shifts_page.page.click(self.work_shifts_page.add_button)
        self.work_shifts_page.page.wait_for_url("**/saveWorkShift*", timeout=30000)
        
        # Fill name
        random_name = self.generate_random_name()
        self.work_shifts_page.page.fill(self.work_shifts_page.name_input, random_name)
        
        # Fill times where From > To
        from_input = self.work_shifts_page.page.locator(self.work_shifts_page.from_time_input)
        from_input.clear()
        from_input.type("05:00 PM", delay=100)
        from_input.press("Escape")
        
        to_input = self.work_shifts_page.page.locator(self.work_shifts_page.to_time_input)
        to_input.clear()
        to_input.type("09:00 AM", delay=100)
        to_input.press("Escape")
        
        # Blur
        self.work_shifts_page.page.click("//h6")
        
        # Click Save
        self.work_shifts_page.page.click(self.work_shifts_page.save_button)
        
        # Verify range error
        assert self.work_shifts_page.is_time_range_error_visible(), "Time range error message missing!"
        
        # Cleanup
        self.work_shifts_page.page.click(self.work_shifts_page.cancel_button)
        self.work_shifts_page.page.wait_for_url("**/workShift")

    def test_add_duplicate_work_shift(self, authenticated_page: Page):
        authenticated_page.wait_for_timeout(1000)
        assert TestWorkShifts.shift_name is not None, "Setup failed: No existing shift to duplicate!"
        
        # Click Add
        self.work_shifts_page.page.click(self.work_shifts_page.add_button)
        self.work_shifts_page.page.wait_for_url("**/saveWorkShift*", timeout=60000)
        
        # Fill existing name
        self.work_shifts_page.page.fill(self.work_shifts_page.name_input, TestWorkShifts.shift_name)
        
        # Blur
        self.work_shifts_page.page.click("//h6")
        
        # Click Save
        self.work_shifts_page.page.click(self.work_shifts_page.save_button)
        
        # Verify already exists error
        assert self.work_shifts_page.is_already_exists_error_visible(), f"Already exists error not visible!"
        
        # Cleanup
        self.work_shifts_page.page.click(self.work_shifts_page.cancel_button)
        self.work_shifts_page.page.wait_for_url("**/workShift")

    def test_edit_work_shift(self, authenticated_page: Page):
        authenticated_page.wait_for_timeout(1000)
        assert TestWorkShifts.shift_name is not None, "Setup failed: No shift to edit!"
        
        old_name = TestWorkShifts.shift_name
        new_name = f"Edited_{old_name}"
        print(f"Editing: {old_name} -> {new_name}")
        
        # Edit Work Shift
        self.work_shifts_page.edit_work_shift(old_name, new_name)
        
        # Update class variable for next test
        TestWorkShifts.shift_name = new_name
        
        # Verify
        assert self.work_shifts_page.is_work_shift_present(new_name), "New Work Shift not found!"

    def test_delete_work_shift(self, authenticated_page: Page):
        authenticated_page.wait_for_timeout(1000)
        assert TestWorkShifts.shift_name is not None, "No shift to delete!"
        
        name_to_delete = TestWorkShifts.shift_name
        print(f"Deleting: {name_to_delete}")
        
        # Delete Work Shift
        self.work_shifts_page.delete_work_shift(name_to_delete)
        
        # Reset state
        TestWorkShifts.shift_name = None
        
        # Verify
        assert not self.work_shifts_page.is_work_shift_present(name_to_delete), "Work Shift still exists after deletion!"

    def test_bulk_delete_work_shifts(self, authenticated_page: Page):
        authenticated_page.wait_for_timeout(1000)
        
        # Add 2 shifts to delete
        shift1 = self.generate_random_name()
        shift2 = self.generate_random_name()
        
        # Add shifts via POM
        self.work_shifts_page.add_work_shift(shift1)
        self.work_shifts_page.add_work_shift(shift2)
        
        # Bulk Delete
        self.work_shifts_page.bulk_delete_work_shifts([shift1, shift2])
        
        # Verify deleted
        assert not self.work_shifts_page.is_work_shift_present(shift1), f"Work Shift {shift1} still exists!"
        assert not self.work_shifts_page.is_work_shift_present(shift2), f"Work Shift {shift2} still exists!"
