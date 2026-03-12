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
        TestLocations.location_name = self.generate_random_name()
        print(f"Testing Add Location: {TestLocations.location_name}")
        
        self.locations_page.add_location(
            name=TestLocations.location_name,
            country="United States",
            city="New York",
            address="123 Test St",
            zip_code="10001"
        )
        
        # Verify
        assert self.locations_page.is_location_present(TestLocations.location_name), f"Location {TestLocations.location_name} not found after adding!"

    def test_edit_location(self, authenticated_page: Page):
        assert TestLocations.location_name is not None, "Setup failed: No location to edit!"
        
        old_name = TestLocations.location_name
        new_name = f"Edited_{old_name}"
        print(f"Editing Location: {old_name} -> {new_name}")
        
        self.locations_page.edit_location(old_name, new_name)
        
        # Update class variable for next test
        TestLocations.location_name = new_name
        
        # Verify
        assert self.locations_page.is_location_present(new_name), f"New Location {new_name} not found!"

    def test_add_location_empty(self, authenticated_page: Page):
        # Click Add
        self.locations_page.page.click(self.locations_page.add_button)
        self.locations_page.page.wait_for_url("**/saveLocation*")
        
        # Click Save without filling anything
        self.locations_page.page.click(self.locations_page.save_button)
        
        # Verify required error
        assert self.locations_page.is_required_error_visible("Name"), "Required error message not visible for Name!"
        assert self.locations_page.is_required_error_visible("Country"), "Required error message not visible for Country!"
        
        # Cleanup
        self.locations_page.page.click(self.locations_page.cancel_button)
        self.locations_page.page.wait_for_url("**/viewLocations")

    def test_delete_location(self, authenticated_page: Page):
        assert TestLocations.location_name is not None, "Setup failed: No location to delete!"
        
        name_to_delete = TestLocations.location_name
        print(f"Deleting Location: {name_to_delete}")
        
        self.locations_page.delete_location(name_to_delete)
        
        # Reset state
        TestLocations.location_name = None
        
        # Verify
        assert not self.locations_page.is_location_present(name_to_delete), f"Location {name_to_delete} still exists after deletion!"

    def test_bulk_delete_locations(self, authenticated_page: Page):
        # Add 2 locations to delete
        loc1 = self.generate_random_name()
        loc2 = self.generate_random_name()
        
        self.locations_page.add_location(name=loc1, country="India", city="Bangalore")
        self.locations_page.add_location(name=loc2, country="India", city="Mumbai")
        
        # Bulk Delete
        self.locations_page.bulk_delete_locations([loc1, loc2])
        
        # Verify deleted
        assert not self.locations_page.is_location_present(loc1), f"Location {loc1} still exists after bulk deletion!"
        assert not self.locations_page.is_location_present(loc2), f"Location {loc2} still exists after bulk deletion!"
