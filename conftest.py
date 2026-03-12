import pytest
import os
import sys
from datetime import datetime
from playwright.sync_api import sync_playwright
import allure
from pages.login_page import LoginPage
from utils.config import BASE_URL, USERNAME, PASSWORD

def pytest_collection_modifyitems(config, items):
    """Enforce test execution priority: Login -> Job Actions -> Job Category"""
    # Priority order for test files
    order = ["test_login.py", "test_employment_status.py", "test_job_actions.py", "test_job_categories.py", "test_user_management.py"]
    
    def get_order_priority(item):
        filename = os.path.basename(item.fspath)
        try:
            return order.index(filename)
        except ValueError:
            return len(order)

    # Sort items based on the priority list
    items.sort(key=get_order_priority)

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(headless=False)
    yield browser
    browser.close()

@pytest.fixture(scope="session")
def authenticated_page(page):
    """Use the shared session page and sign in once."""
    if "dashboard/index" not in page.url:
        login_page = LoginPage(page)
        # Only navigate if not already on login page
        if "/login" not in page.url:
            login_page.navigate(BASE_URL)
        
        login_page.login(USERNAME, PASSWORD)
        
        # Wait for dashboard to load
        page.wait_for_url("**/dashboard/index", timeout=60000)
    
    yield page

@pytest.fixture(scope="session")
def context(browser):
    context = browser.new_context()
    yield context
    context.close()

@pytest.fixture(scope="session")
def page(context):
    page = context.new_page()
    yield page
    page.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Try to get page from authenticated_page or page fixture
        page = item.funcargs.get("authenticated_page") or item.funcargs.get("page")
        if page:
            try:
                screenshot = page.screenshot()
                allure.attach(
                    screenshot,
                    name=f"{item.name}_failure",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"Failed to take screenshot: {e}")
