from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WikipediaPage:
    """Page Object for the main Wikipedia homepage."""

    # Define all element locators
    SEARCH_INPUT = (By.CSS_SELECTOR, "#searchInput")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ENGLISH_LINK = (By.CSS_SELECTOR, "#js-link-box-en")
    JAPAN_LINK = (By.CSS_SELECTOR, "#js-link-box-ja")
    FOOTER = (By.CSS_SELECTOR, ".footer")
    LOGO = (By.CSS_SELECTOR, ".central-featured-logo")
    LANGUAGE_LINKS = (By.CSS_SELECTOR, ".central-featured-lang")
    LANGUAGE_DROPDOWN = (By.CSS_SELECTOR, "#searchLanguage")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def navigate(self, url):
        self.driver.get(url)

    def search_for(self, text):
        self.wait.until(EC.visibility_of_element_located(self.SEARCH_INPUT)).send_keys(text)
        self.wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON)).click()

    def click_element(self, locator):
        # Helper to click an element given its (By, selector) tuple
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    # --- Verification Methods ---
    
    def wait_for_title_to_be(self, expected_title):
        self.wait.until(EC.title_is(expected_title))

    def wait_for_title_to_contain(self, text):
        self.wait.until(EC.title_contains(text))

    def is_element_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def is_element_present(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_for_url_to_contain(self, text):
        self.wait.until(EC.url_contains(text))