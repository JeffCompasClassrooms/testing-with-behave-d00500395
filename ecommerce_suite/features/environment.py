"""
Environment setup for behave.
This file sets up and tears down the Selenium WebDriver (ChromeDriver)
for all feature files in the project, using a direct Selenium implementation
with the webdriver-manager for automatic driver executable handling.
"""
import os
from behave.runner import Context

# Try to import Selenium; if not available or if mock is requested use a lightweight Mock
USE_MOCK = os.getenv("MOCK_WEBDRIVER", "0") == "1"
if not USE_MOCK:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
else:
    webdriver = None
    Service = None
import time


class MockWebElement:
    def __init__(self, selector, text=""):
        self.selector = selector
        self._text = text or selector
        self._value = ""

    def click(self):
        print(f"[mock] click() on {self.selector}")

    def send_keys(self, keys):
        print(f"[mock] send_keys({keys}) on {self.selector}")
        self._value = keys

    def clear(self):
        self._value = ""

    def get_attribute(self, name):
        if name == "value":
            return self._value
        return ""

    @property
    def text(self):
        return self._text

    def is_displayed(self):
        return True


class MockWebDriver:
    """A minimal mock webdriver that supports the small surface used by the steps.
    This is not a full Selenium replacement — it's intended for dry-run/testing
    the behave flows without a live application.
    """
    is_mock = True

    def __init__(self):
        self.title = "Mock Home"
        self.current_url = "http://mock.local/"

    def get(self, url):
        print(f"[mock] get: {url}")
        self.current_url = url
        # Simple heuristics to set titles so assertions in steps pass
        if "/product/" in url:
            name = url.split('/product/')[-1].replace('-', ' ')
            self.title = name
        elif "/category/" in url:
            name = url.split('/category/')[-1].replace('-', ' ')
            self.title = name
        elif "/login" in url:
            self.title = "Login"
        elif "/checkout/shipping" in url:
            self.title = "Shipping Information"
        elif "/checkout/payment" in url:
            self.title = "Payment Review"
        elif "/checkout/confirm" in url:
            self.title = "Order Confirmation"
        else:
            self.title = "Mock Page"

    def find_element(self, by, value=None):
        # Return a MockWebElement — for important selectors provide sensible text
        text = ""
        if value:
            if "product-card:nth-child(1)" in value or "product-link-first" in value:
                text = "Deluxe Espresso Maker"
            elif "cart-count" in value:
                text = "0"
            elif "user-greeting" in value:
                text = "Test User"
            elif "total-price" in value:
                text = "$0.00"
            elif "mobile-menu" in value:
                text = ""
        return MockWebElement(value, text=text)

    def implicitly_wait(self, t):
        pass

    def delete_all_cookies(self):
        pass

    def maximize_window(self):
        pass

    def set_window_size(self, w, h):
        pass

    def execute_script(self, script, *args, **kwargs):
        print(f"[mock] execute_script: {script}")

    def quit(self):
        print("[mock] quit webdriver")

# --- Setup and Teardown Functions ---

def before_all(context: Context):
    """Setup function run before all features/scenarios."""
    print("Initializing WebDriver...")

    # ChromeDriverManager automatically downloads and manages the correct driver version.
    try:
        if USE_MOCK:
            # Use the lightweight mock webdriver for dry runs
            context.webdriver = MockWebDriver()
            context.webdriver.implicitly_wait(5)
            print("Running tests with MockWebDriver.")
        else:
            # 1. Install/get the driver path and set up the Service
            driver_path = ChromeDriverManager().install()
            # Write chromedriver logs for debugging if startup hangs
            logs_dir = os.path.join(os.getcwd(), 'features', 'logs')
            os.makedirs(logs_dir, exist_ok=True)
            chromedriver_log = os.path.join(logs_dir, 'chromedriver.log')
            service = Service(driver_path, log_path=chromedriver_log)
            print(f"Using chromedriver at: {driver_path}")
            print(f"Chromedriver log path: {chromedriver_log}")
            options = webdriver.ChromeOptions()

            # Configure browser options
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            
            # 2. Initialize the browser
            print("Starting Chrome browser...")
            context.webdriver = webdriver.Chrome(service=service, options=options)
            context.webdriver.set_page_load_timeout(30)
            context.webdriver.implicitly_wait(5) # Set a default implicit wait time
            print("Chrome started successfully.")

            print("Running tests with ChromeDriver (managed by webdriver-manager).")

    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        # Terminate gracefully if the driver cannot be initialized
        raise Exception("Failed to initialize Chrome WebDriver. Check your Chrome installation.")


def after_all(context: Context):
    """Teardown function run after all features/scenarios."""
    if 'webdriver' in context and context.webdriver:
        print("Closing WebDriver.")
        context.webdriver.quit()

#

def before_scenario(context: Context, scenario):
    """Setup function run before each scenario."""
    if not hasattr(context, 'webdriver') or not context.webdriver:
        print("[WARNING] WebDriver not found in before_scenario")
        return

    try:
        context.webdriver.delete_all_cookies()
        context.webdriver.maximize_window()
    except Exception as e:
        print(f"[WARNING] Failed to reset browser state: {e}")

def after_scenario(context: Context, scenario):
    """Teardown function run after each scenario."""
    # Custom teardown logic, if needed (e.g., taking screenshots on failure)
    pass