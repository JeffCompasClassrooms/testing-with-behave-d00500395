"""
This environment file sets up and tears down the Selenium WebDriver (ChromeDriver)
for all feature files, using the webdriver-manager for automatic driver executable handling.
"""
import os
import time
from behave.runner import Context
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# --- Setup and Teardown Functions ---

def before_all(context: Context):
    """Setup function run before all features/scenarios."""
    print("Initializing WebDriver...")

    try:
        # 1. Install/get the driver path and set up the Service
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
        print(f"Using chromedriver at: {driver_path}")
        
        options = Options()
        # Configure browser options
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        
        # 2. Initialize the browser using the modern Selenium 4+ syntax
        print("Starting Chrome browser...")
        context.webdriver = webdriver.Chrome(service=service, options=options)
        context.webdriver.set_page_load_timeout(30)
        context.webdriver.implicitly_wait(5) # Set a default implicit wait time
        print("Chrome started successfully.")

    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        raise Exception("Failed to initialize Chrome WebDriver. Check your Chrome installation.")


def after_all(context: Context):
    """Teardown function run after all features/scenarios."""
    if 'webdriver' in context and context.webdriver:
        print("Closing WebDriver.")
        context.webdriver.quit()

def before_scenario(context: Context, scenario):
    """Setup function run before each scenario."""
    if hasattr(context, 'webdriver') and context.webdriver:
        try:
            context.webdriver.delete_all_cookies()
            context.webdriver.maximize_window()
        except Exception as e:
            print(f"[WARNING] Failed to reset browser state: {e}")

# The after_scenario hook is typically empty unless you need screenshot logic
# def after_scenario(context: Context, scenario):
#     pass