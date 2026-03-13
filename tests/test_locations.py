import pytest
import random
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.locations_page import LocationsPage

class TestLocations:
    location_name = None

    @pytest.fixture(autouse=True)
    def setup(self, authenticated_page: Page):
        self.login_page = LoginPage(authenticated_page)
        self.locations_page = LocationsPage(authenticated_page)
        self.locations_page.navigate_to_locations()

    def generate_random_name(self):
        return f"Loc_{random.randint(1000, 9999)}"

    def test_add_location(self, authenticated_page: Page):
        """Verify that a new location can be successfully added with all fields filled."""
        TestLocations.location_name = self.generate_random_name()
        print(f"Testing Add Location: {TestLocations.location_name}")
        
        self.locations_page.add_location(
            name=TestLocations.location_name,
            city="New York",
            province="New York",
            zip_code="10001",
            country="United States",
            phone="1234567890",
            fax="1234567890",
            address="123 Test St",
            notes="Test Notes"
        )
        
        # Verify
        assert self.locations_page.is_location_present(TestLocations.location_name), f"Location {TestLocations.location_name} not found!"

    def test_add_location_mandatory_name(self, authenticated_page: Page):
        """Verify that the 'Name' field is mandatory when adding a location."""
        authenticated_page.wait_for_timeout(2000)
        self.locations_page.page.click(self.locations_page.add_button)
        
        # Fill everything except Name
        self.locations_page.page.click(self.locations_page.country_dropdown)
        self.locations_page.page.click("div[role='listbox'] div[role='option'] span:has-text('India')")
        
        self.locations_page.page.click(self.locations_page.save_button)
        
        # Verify Name required error
        assert self.locations_page.is_required_error_visible("Name"), "Required error message not visible for Name!"
        
        # Cleanup
        self.locations_page.click_cancel()

    def test_add_location_mandatory_country(self, authenticated_page: Page):
        """Verify that the 'Country' field is mandatory when adding a location."""
        authenticated_page.wait_for_timeout(2000)
        self.locations_page.page.click(self.locations_page.add_button)
        
        # Fill only Name
        self.locations_page.page.fill(self.locations_page.name_input, "Missing Country Loc")
        
        self.locations_page.page.click(self.locations_page.save_button)
        
        # Verify Country required error
        assert self.locations_page.is_required_error_visible("Country"), "Required error message not visible for Country!"
        
        # Cleanup
        self.locations_page.click_cancel()

    def test_edit_location(self, authenticated_page: Page):
        """Verify that an existing location's name can be successfully updated."""
        authenticated_page.wait_for_timeout(2000)
        assert TestLocations.location_name is not None, "Setup failed: No location to edit!"
        
        old_name = TestLocations.location_name
        new_name = f"Edited_{old_name}"
        print(f"Editing Location: {old_name} -> {new_name}")
        
        self.locations_page.edit_location(old_name, new_name)
        
        # Update class variable
        TestLocations.location_name = new_name
        
        # Verify
        assert self.locations_page.is_location_present(new_name), f"New Location {new_name} not found!"

    def test_delete_location(self, authenticated_page: Page):
        """Verify that a location can be successfully deleted."""
        authenticated_page.wait_for_timeout(2000)
        assert TestLocations.location_name is not None, "Setup failed: No location to delete!"
        
        name_to_delete = TestLocations.location_name
        print(f"Deleting Location: {name_to_delete}")
        
        self.locations_page.delete_location(name_to_delete)
        
        # Reset state
        TestLocations.location_name = None
        
        # Verify
        assert not self.locations_page.is_location_present(name_to_delete), f"Location {name_to_delete} still exists after deletion!"

    def test_bulk_delete_locations(self, authenticated_page: Page):
        """Verify that multiple locations can be selected and deleted in bulk."""
        authenticated_page.wait_for_timeout(2000)
        
        # Create some random locations to delete
        names_to_create = [f"BulkLoc_{random.randint(1000, 9999)}" for _ in range(3)]
        for name in names_to_create:
            self.locations_page.add_location(name, country="Singapore")
            
        print(f"Testing Bulk Delete for: {names_to_create}")
        authenticated_page.wait_for_timeout(2000)
        
        # Select and Delete
        self.locations_page.select_locations(names_to_create)
        self.locations_page.delete_selected()
        
        # Verify all are deleted
        for name in names_to_create:
            assert not self.locations_page.is_location_present(name), f"Location {name} still exists after bulk deletion!"

    