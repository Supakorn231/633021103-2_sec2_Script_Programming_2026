"""Manages Selenium WebDriver setup and teardown."""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


class DriverManager:
    """
    Creates a Chrome or Firefox WebDriver.
    Driver lookup order: explicit `driver_path` -> webdriver-manager download ->
    Selenium Manager (built into selenium >= 4.6).
    """

    def __init__(self, browser_type: str = "chrome", headless: bool = True,
                 user_agent: str = DEFAULT_USER_AGENT, driver_path: str = None,
                 binary_path: str = None):
        self.browser_type = browser_type.lower()
        self.headless = headless
        self.user_agent = user_agent
        self.driver_path = driver_path
        self.binary_path = binary_path
        self.driver = None

    def _chrome_service(self):
        if self.driver_path:
            return ChromeService(self.driver_path)
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            return ChromeService(ChromeDriverManager().install())
        except Exception as e:  # noqa: BLE001
            print(f"  [Info] webdriver-manager unavailable ({type(e).__name__}); using Selenium Manager.")
            return ChromeService()

    def _firefox_service(self):
        if self.driver_path:
            return FirefoxService(self.driver_path)
        try:
            from webdriver_manager.firefox import GeckoDriverManager
            return FirefoxService(GeckoDriverManager().install())
        except Exception as e:  # noqa: BLE001
            print(f"  [Info] webdriver-manager unavailable ({type(e).__name__}); using Selenium Manager.")
            return FirefoxService()

    def get_driver(self):
        """Initialise (once) and return the WebDriver."""
        if self.driver:
            return self.driver

        if self.browser_type == "chrome":
            options = webdriver.ChromeOptions()
            if self.headless:
                options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--log-level=3")
            options.add_argument(f"user-agent={self.user_agent}")
            if self.binary_path:
                options.binary_location = self.binary_path
            self.driver = webdriver.Chrome(service=self._chrome_service(), options=options)

        elif self.browser_type == "firefox":
            options = webdriver.FirefoxOptions()
            if self.headless:
                options.add_argument("--headless")
            options.set_preference("general.useragent.override", self.user_agent)
            self.driver = webdriver.Firefox(service=self._firefox_service(), options=options)

        else:
            raise ValueError(f"Unsupported browser type: {self.browser_type}")

        # Explicit waits are used for page content; keep the implicit wait short so
        # "element not found" checks (e.g. no next button) return quickly.
        self.driver.implicitly_wait(2)
        return self.driver

    def close_driver(self):
        """Quit the browser if it is running."""
        if self.driver:
            self.driver.quit()
            self.driver = None
