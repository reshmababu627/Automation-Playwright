import pytest
import os
import allure
from pages.login_page import LoginPage
from utils.config import BASE_URL, USERNAME, PASSWORD

def pytest_collection_modifyitems(config, items):
    """Enforce test execution priority: Login -> Job Actions -> Job Category"""
    # Priority order for test files
    order = ["test_login.py", "test_user_management.py", "test_job_actions.py", "test_employment_status.py", "test_job_categories.py", "test_work_shifts.py", "test_general_info.py", "test_locations.py" , "test_organization_structure.py"]
    
    def get_order_priority(item):
        filename = os.path.basename(item.fspath)
        try:
            return order.index(filename)
        except ValueError:
            return len(order)

    # Sort items based on the priority list
    items.sort(key=get_order_priority)

@pytest.fixture(scope="module")
def session_context(browser):
    """Use standard session-scoped 'browser' fixture to create a module-scoped context."""
    context = browser.new_context()
    yield context
    context.close()

@pytest.fixture(scope="module")
def session_page(session_context):
    """Create a single page for the entire module/file."""
    page = session_context.new_page()
    yield page
    page.close()

@pytest.fixture(scope="module")
def authenticated_page(session_page):
    """Sign in once for the entire module/file."""
    if "dashboard/index" not in session_page.url:
        login_page = LoginPage(session_page)
        # Ensure we start from the login page
        login_page.navigate(BASE_URL)
        
        # Wait for fields to be interactable
        session_page.wait_for_load_state("networkidle")
        session_page.wait_for_selector(login_page.username_input, state="visible",  timeout=60000)
        login_page.login(USERNAME, PASSWORD)
        
        # Wait for dashboard to load
        session_page.wait_for_url("**/dashboard/index", timeout=60000)
        session_page.wait_for_load_state("load")
    
    yield session_page
