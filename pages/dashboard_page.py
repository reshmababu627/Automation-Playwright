from playwright.sync_api import Page

class DashboardPage:

    def __init__(self, page: Page):
        self.page = page
        self.dashboard_header = "//h6[text()='Dashboard']"

    def is_dashboard_visible(self):
        self.page.wait_for_selector(self.dashboard_header, timeout=40000)
        return self.page.locator(self.dashboard_header).is_visible()
