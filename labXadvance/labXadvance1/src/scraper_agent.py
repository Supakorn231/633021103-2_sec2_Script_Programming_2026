"""
The config-driven "agent": reads a plan (JSON config), navigates, extracts items,
follows pagination and stops when there are no more pages or the page limit is reached.
"""
import time
from dataclasses import asdict

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By

from src.data_models import Product
from src.driver_manager import DEFAULT_USER_AGENT, DriverManager
from src.utils import is_allowed_by_robots, retry, safe_click, wait_for_element


class ScraperAgent:
    def __init__(self, config: dict, browser: str = "chrome", headless: bool = True,
                 driver_path: str = None, binary_path: str = None):
        self.config = config
        self.max_retries = int(config.get("max_retries", 3))
        self.wait_timeout = int(config.get("wait_timeout", 10))
        self.driver_manager = DriverManager(
            browser_type=browser,
            headless=headless,
            user_agent=config.get("user_agent", DEFAULT_USER_AGENT),
            driver_path=driver_path,
            binary_path=binary_path,
        )
        self.driver = None

    # ------------------------------------------------------------------ main loop
    def run(self) -> list:
        """Execute the scraping plan and return a list of product dicts."""
        start_url = self.config["start_url"]
        if self.config.get("respect_robots_txt", True) and not is_allowed_by_robots(start_url):
            print(f"[Stop] robots.txt disallows scraping {start_url}. Respecting the site owner.")
            return []

        results = []
        self.driver = self.driver_manager.get_driver()
        try:
            retry(lambda: self._open(start_url), self.max_retries, description="Loading start page")
            current_page = 1

            while current_page <= self.config["max_pages"]:
                print(f"Scraping page {current_page}...")
                page_items = retry(self._scrape_current_page, self.max_retries,
                                   description=f"Scraping page {current_page}")
                results.extend(page_items)
                print(f"  -> {len(page_items)} items")

                if current_page >= self.config["max_pages"]:
                    print(f"Reached max_pages ({self.config['max_pages']}). Stopping.")
                    break
                if not self._go_to_next_page():
                    print("No next page button found. Stopping.")
                    break
                current_page += 1
                time.sleep(self.config["delay_between_pages"])  # be polite between pages
        finally:
            self.driver_manager.close_driver()

        return results

    # ------------------------------------------------------------------ steps
    def _open(self, url: str):
        self.driver.get(url)
        wait_for_element(self.driver, self.config["item_container_selector"], self.wait_timeout)

    def _scrape_current_page(self) -> list:
        wait_for_element(self.driver, self.config["item_container_selector"], self.wait_timeout)
        items = self.driver.find_elements(By.CSS_SELECTOR, self.config["item_container_selector"])
        return [asdict(self._parse_item(item)) for item in items]

    def _go_to_next_page(self) -> bool:
        """Click the 'next' link. Returns False when there is no next page."""
        selector = self.config.get("pagination_selector")
        if not selector:
            return False
        buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
        if not buttons:
            return False
        old_url = self.driver.current_url

        def click_and_wait():
            button = self.driver.find_element(By.CSS_SELECTOR, selector)  # re-find: avoids stale refs
            safe_click(self.driver, button)
            wait_for_element(self.driver, self.config["item_container_selector"], self.wait_timeout)
            if self.driver.current_url == old_url:
                raise RuntimeError("Page did not change after clicking next")

        retry(click_and_wait, self.max_retries, description="Clicking next page")
        return True

    # ------------------------------------------------------------------ extraction
    def _extract(self, item, spec):
        """
        Extract one field. `spec` is a CSS selector, optionally ending in '@attr'
        to read an attribute instead of the text, e.g. "h3 a@title" or "img@src".
        """
        if not spec:
            return None
        selector, _, attr = spec.partition("@")
        try:
            element = item.find_element(By.CSS_SELECTOR, selector.strip())
            value = element.get_attribute(attr.strip()) if attr else element.text
            return value.strip() if value else None
        except (NoSuchElementException, StaleElementReferenceException):
            return None

    def _parse_item(self, item) -> Product:
        selectors = self.config["item_data_selectors"]
        return Product(
            name=self._extract(item, selectors.get("name")),
            price=self._extract(item, selectors.get("price")),
            description=self._extract(item, selectors.get("description")),
            url=self._extract(item, selectors.get("url")),
            image_url=self._extract(item, selectors.get("image_url")),
        )
