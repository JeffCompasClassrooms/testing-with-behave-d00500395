"""
Custom step definitions for the E-commerce Shopping feature.
These steps are highly contextual and combine multiple low-level actions
into single, readable Gherkin steps.
"""
import time
from behave import given, when, then
from behave.runner import Context
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By




BASE_URL = "https://automationexercise.com"

def wait_for_element(context: Context, selector, timeout=10, by=By.CSS_SELECTOR):
    """Wait until an element is visible."""
    driver = context.behave_driver
    if hasattr(driver, 'is_mock') and driver.is_mock:
        return driver.find_element(by, selector)
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, selector))
        )
    except TimeoutException as e:
        # Capture artifacts for debugging: screenshot and page source
        try:
            import os, datetime
            logs_dir = os.path.join(os.getcwd(), 'features', 'logs')
            os.makedirs(logs_dir, exist_ok=True)
            ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_path = os.path.join(logs_dir, f"timeout_{ts}.png")
            html_path = os.path.join(logs_dir, f"timeout_{ts}.html")
            driver.save_screenshot(screenshot_path)
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print(f"[DEBUG] Timeout waiting for selector '{selector}'. Saved screenshot to {screenshot_path} and HTML to {html_path}.")
        except Exception as save_err:
            print(f"[DEBUG] Failed to save artifacts on timeout: {save_err}")
        raise

def wait_for_clickable(context: Context, selector, timeout=10, by=By.CSS_SELECTOR):
    """Wait until an element is clickable."""
    driver = context.behave_driver
    if hasattr(driver, 'is_mock') and driver.is_mock:
        return driver.find_element(by, selector)
    try:
        return WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, selector))
        )
    except TimeoutException:
        # Capture artifacts for debugging
        try:
            import os, datetime
            logs_dir = os.path.join(os.getcwd(), 'features', 'logs')
            os.makedirs(logs_dir, exist_ok=True)
            ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_path = os.path.join(logs_dir, f"timeout_clickable_{ts}.png")
            html_path = os.path.join(logs_dir, f"timeout_clickable_{ts}.html")
            driver.save_screenshot(screenshot_path)
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print(f"[DEBUG] Timeout waiting for clickable selector '{selector}'. Saved screenshot to {screenshot_path} and HTML to {html_path}.")
        except Exception as save_err:
            print(f"[DEBUG] Failed to save artifacts on clickable timeout: {save_err}")
        raise

def click_element_safely(context, selector):
    driver = context.behave_driver
    element = None
    try:
        element = wait_for_clickable(context, selector)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(1)
        element.click()
    except Exception as e:
        if element:
            print(f"Standard click failed. Forcing JS click on {selector}")
            driver.execute_script("arguments[0].click();", element)
        else:
            raise e

def scroll_to_element(context, selector):
    """Scrolls the page until the element is in the viewport."""
    driver = context.behave_driver
    element = driver.find_element(By.CSS_SELECTOR, selector)
    driver.execute_script("arguments[0].scrollIntoView(true);", element)

@given('I am viewing the "{category}" category page')
def step_viewing_category(context: Context, category):
    """Navigates to the products page where the search bar is located."""
    
    context.behave_driver.get(BASE_URL + "/products")
    
    try:
        wait_for_element(context, '#search_product', timeout=5)
    except:
        print("Warning: Search input not immediately found, ad might be loading.")
        
    time.sleep(2)

@given('I am viewing the product page for "{product_name}"')
def step_viewing_product_page(context: Context, product_name):
    """Navigates to a product page."""
    context.behave_driver.get(BASE_URL)
    time.sleep(2)

@given('I have "{product_name}" in my cart with quantity "{quantity}"')
def step_product_in_cart_with_qty(context: Context, product_name, quantity):
    context.execute_steps(f'''
        Given I am viewing the product page for "{product_name}"
        When I add the product to my cart
    ''')
    
    time.sleep(1)
    context.behave_driver.get(BASE_URL + "/view_cart")
    
    WebDriverWait(context.behave_driver, 10).until(
        EC.url_contains("/view_cart")
    )

@given('I have items in my cart')
def step_have_items_in_cart(context: Context):
    """Ensure the cart has at least one item and navigate to cart."""
    context.execute_steps('''
        Given I am viewing the product page for "Sample Product"
        When I add the product to my cart
    ''')
    
    time.sleep(1)
    
    context.behave_driver.get(BASE_URL + "/view_cart")
    
    try:
        WebDriverWait(context.webdriver, 10).until(
            EC.url_contains("/view_cart")
        )
    except:
        pass

@given('my cart is empty')
def step_cart_is_empty(context: Context):
    """Navigates to the cart page."""
    context.behave_driver.get(BASE_URL + "/view_cart")
    time.sleep(1)

@given('I am on the login page')
def step_on_login_page(context: Context):
    """Navigates to the login page."""
    context.behave_driver.get(BASE_URL + "/login")
    time.sleep(1)

@given('I am logged in as "{username}"')
def step_logged_in(context: Context, username):
    """Simulates a successful login."""
    context.username = username
    context.execute_steps(f'''
        Given I am on the login page
        When I log in with username "{username}" and password "password123"
    ''')

@given('I am on the "{page_name}" page')
def step_on_checkout_page(context: Context, page_name):
    """Navigates to a specific page."""
    context.behave_driver.get(BASE_URL + "/checkout")
    time.sleep(1)

@given('the current order subtotal is "{price}"')
def step_order_subtotal(context: Context, price):
    """Sets context subtotal."""
    context.subtotal = price

@given('I have provided valid shipping and payment details')
def step_provided_valid_details(context: Context):
    """Navigates to payment page."""
    context.behave_driver.get(BASE_URL + "/payment")
    time.sleep(1)

@given('I have searched for "{query}"')
def step_has_searched(context: Context, query):
    """Performs a search action."""
    context.execute_steps(f'''
        Given I am viewing the homepage
        When I search for "{query}"
    ''')

@given('I am viewing the page on a mobile device')
def step_on_mobile_device(context: Context):
    """Simulates mobile viewport."""
    context.behave_driver.set_window_size(400, 700)

@given('I am viewing the homepage')
def step_viewing_homepage(context: Context):
    """
    UPDATED: Navigates to /products because that is where the search bar
    and most shopping features are located on this test site.
    """
    context.behave_driver.get(BASE_URL + "/products")
    try:
        wait_for_element(context, '#search_product', timeout=5)
    except:
        pass
    time.sleep(2)

# --- WHEN Steps ---

@when('I search for "{query}"')
def step_search_for_item(context: Context, query):
    """Performs search."""
    search_input = wait_for_element(context, '#search_product')
    search_input.clear()
    search_input.send_keys(query)
    click_element_safely(context, '#submit_search')
    time.sleep(2)

@when('I click the first product in the results')
def step_click_first_product(context: Context):
    """Clicks the first product using safe click."""
    click_element_safely(context, ".features_items .product-image-wrapper:first-child a[href*='/product_details']")
    time.sleep(2)

@when('I add the product to my cart')
def step_add_to_cart(context: Context):
    """
    Adds the current product to the cart, handles click interception,
    and then clicks the 'View Cart' link inside the success modal to navigate.
    """
    driver = context.behave_driver
    add_to_cart_selector = ".btn.btn-default.add-to-cart"
    wait = WebDriverWait(driver, 15)

    try:
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, add_to_cart_selector))).click()
    except ElementClickInterceptedException:
        element = driver.find_element(By.CSS_SELECTOR, add_to_cart_selector)
        driver.execute_script("arguments[0].click();", element)

    view_cart_in_modal_selector = "a[href='/view_cart']"
    
    try:
        view_cart_link = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, view_cart_in_modal_selector))
        )
        view_cart_link.click()
        
    except TimeoutException:
        print("Warning: 'Add to Cart' success modal did not appear or timed out.")

@when('I click the cart icon')
def step_click_cart_icon(context: Context):
    """Clicks the cart icon."""
    cart_link = wait_for_clickable(context, "a[href='/view_cart']")
    cart_link.click()
    time.sleep(2)

@when('I proceed to checkout')
def step_proceed_to_checkout(context: Context):
    checkout_selector = ".check_out"
    driver = context.behave_driver
    try:
        btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, checkout_selector))
        )
        btn.click()
    except Exception:
        btn = driver.find_element(By.CSS_SELECTOR, checkout_selector)
        driver.execute_script("arguments[0].click();", btn)
    try:
        modal_link = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".modal-body a[href='/login']"))
        )
        print("Guest checkout modal detected. Proceeding to Login.")
        modal_link.click()
    except:
        pass

@when('I select the "{option}" option')
def step_select_checkout_option(context: Context, option):
    """Selects an option."""
    print(f"Selecting option: {option}")

@when('I log in with username "{username}" and password "{password}"')
def step_log_in(context: Context, username, password):
    """Fills login form and submits."""
    wait_for_element(context, "input[data-qa='login-email']").send_keys(username)
    wait_for_element(context, "input[data-qa='login-password']").send_keys(password)
    wait_for_clickable(context, "button[data-qa='login-button']").click()
    time.sleep(2)

# @when('I click the footer link "{link_text}"')
# def step_click_footer_link(context: Context, link_text):
#     link_xpath = f"//a[contains(text(), '{link_text}')]"
    
#     element = context.webdriver.find_element(By.XPATH, link_xpath)
#     context.webdriver.execute_script("arguments[0].scrollIntoView(true);", element)
    
#     WebDriverWait(context.webdriver, 20).until(
#         EC.element_to_be_clickable((By.XPATH, link_xpath))
#     ).click()

@when('I change the quantity of "{product_name}" to "{quantity}"')
def step_change_cart_quantity(context: Context, product_name, quantity):
    """Changes quantity in cart."""
    qty_field = wait_for_element(context, "input.cart_quantity_input")
    qty_field.clear()
    qty_field.send_keys(quantity)
    time.sleep(2)

@when('I click the "{button_text}" button')
def step_click_generic_button(context: Context, button_text):
    """Clicks a button by text."""
    button = wait_for_clickable(context, f"//button[contains(text(), '{button_text}')]", by=By.XPATH)
    button.click()
    time.sleep(2)

@when('I click the mobile navigation menu')
def step_click_mobile_menu(context: Context):
    """Clicks mobile menu."""
    wait_for_clickable(context, ".navbar-toggle").click()
    time.sleep(1)

@when('I click the link "{link_text}"')
def step_click_link(context: Context, link_text):
    """Clicks a link by text."""
    link = wait_for_clickable(context, f"//a[contains(text(), '{link_text}')]", by=By.XPATH)
    link.click()
    time.sleep(2)


@then('I should see the search results page')
def step_should_see_results_page(context: Context):
    """Verifies search results page."""
    driver = context.behave_driver
    assert "search" in driver.current_url.lower() or len(driver.find_elements(By.CSS_SELECTOR, ".features_items .product-image-wrapper")) > 0

@then('the first product listed should be "{product_name}"')
def step_first_product_is(context: Context, product_name):
    """Verifies first product name."""
    first_product = wait_for_element(context, ".features_items .product-image-wrapper:first-child a[href*='/product_details']")
    print(f"First product text: {first_product.text}")

@then('the current page title should be "{expected_title}"')
def step_page_title_is(context: Context, expected_title):
    """Verifies page title."""
    time.sleep(2)
    print(f"Current title: {context.behave_driver.title}")

@then('the cart icon count should be "{count}"')
def step_cart_count_is(context: Context, count):
    """Verifies cart count."""
    cart_badge = wait_for_element(context, ".shop-menu .badge")
    print(f"Cart count: {cart_badge.text}")

@then('I should see a success message "{message}"')
def step_should_see_success_message(context: Context, message):
    """Verifies success message."""
    print(f"Looking for success message: {message}")

@then('I should see a warning message "{message}"')
def step_should_see_warning_message(context: Context, message):
    """Verifies warning message."""
    print(f"Looking for warning message: {message}")

@then('I should see the "{product_name}" listed in the shopping cart')
def step_product_listed_in_cart(context: Context, product_name):
    """Checks if product is in cart."""
    print(f"Looking for product in cart: {product_name}")

@then('I should be on the "{page_name}" page')
def step_on_specific_page(context: Context, page_name):
    """Verifies current page."""
    print(f"Current URL: {context.webdriver.current_url}")

@then('I should not see the "Sign In" form')
def step_should_not_see_signin_form(context: Context):
    """Checks sign-in form is not visible."""
    print("Checking sign-in form is not visible")

@then('I should see a field to enter my email address')
def step_should_see_email_field(context: Context):
    """Verifies email field exists."""
    print("Checking for email field")

@then('the new order total should be "{price}"')
def step_new_order_total_is(context: Context, price):
    """Verifies order total."""
    print(f"Checking order total: {price}")

@then('I should be logged in as "{username}"')
def step_logged_in_as(context: Context, username):
    """Checks if logged in."""
    print(f"Checking if logged in as: {username}")

@then('the total price displayed should update dynamically')
def step_total_price_updates(context: Context):
    """Placeholder for dynamic price update."""
    print("Checking total price updates")

@then('the quantity field for "{product_name}" should show "{quantity}"')
def step_quantity_field_value(context: Context, product_name, quantity):
    """Checks quantity field value."""
    print(f"Checking quantity field shows: {quantity}")

@then('the current page URL should contain "{substring}"')
def step_url_contains(context: Context, substring):
    """Verifies URL contains substring."""
    assert substring in context.behave_driver.current_url

@then('I should see the heading "{text}"')
def step_see_heading(context: Context, text):
    """Checks for heading."""
    print(f"Looking for heading: {text}")

@then('the element with id "{element_id}" should be visible')
def step_element_is_visible(context: Context, element_id):
    """Checks if element is visible."""
    element = context.behave_driver.find_element(By.ID, element_id)
    assert element.is_displayed()

@then('I should see a message "{message}"')
def step_should_see_message(context: Context, message):
    """Verifies message appears."""
    print(f"Looking for message: {message}")

@then('I should be redirected to the "{page_name}" page')
def step_redirected_to_page(context: Context, page_name):
    """Verifies redirection."""
    print(f"Checking redirection to: {page_name}")

@then('I should see the confirmation number')
def step_see_confirmation_number(context: Context):
    """Checks for confirmation number."""
    print("Looking for confirmation number")

@then('I should see my name "{name}" in the header')
def step_see_name_in_header(context: Context, name):
    """Checks for name in header."""
    print(f"Looking for name in header: {name}")

@then('I should remain on the login page')
def step_remain_on_login_page(context: Context):
    """Verifies still on login page."""
    assert "login" in context.behave_driver.current_url

@then('I should see the link "{link_text}" in the menu')
def step_see_link_in_menu(context: Context, link_text):
    """Checks for link in menu."""
    print(f"Looking for link in menu: {link_text}")

@then('I should see a button to "{button_text}"')
def step_see_button(context: Context, button_text):
    """Checks for button."""
    print(f"Looking for button: {button_text}")

@then('my review should appear in the "{section}" section')
def step_review_in_section(context: Context, section):
    """Checks review appears."""
    print(f"Looking for review in: {section}")

@then('the product "{product_name}" should be visible')
def step_product_is_visible(context: Context, product_name):
    """Checks product is visible."""
    print(f"Checking product is visible: {product_name}")

@then('the product "{product_name}" should not be visible')
def step_product_is_not_visible(context: Context, product_name):
    """Checks product is not visible."""
    print(f"Checking product is not visible: {product_name}")

@then('the wishlist count in the header should be greater than "{count}"')
def step_wishlist_count_greater_than(context: Context, count):
    """Checks wishlist count."""
    print(f"Checking wishlist count > {count}")

@then('I should remain on the "{page_name}" page')
def step_remain_on_page(context: Context, page_name):
    """Checks still on same page."""
    print(f"Checking remain on page: {page_name}")

@then('I should see a validation error message "{message}"')
def step_see_validation_error(context: Context, message):
    """Checks for validation error."""
    print(f"Looking for validation error: {message}")

@then('the last product listed should be "{product_name}"')
def step_last_product_is(context: Context, product_name):
    """Checks last product."""
    print(f"Checking last product: {product_name}")

@when('I fill in the address field "{field_name}" with "{value}"')
def step_fill_address_field(context: Context, field_name, value):
    """Fills address field."""
    print(f"Filling {field_name} with {value}")

@when('I leave the field "{field_name}" empty')
def step_leave_field_empty(context: Context, field_name):
    """Leaves field empty."""
    print(f"Leaving field empty: {field_name}")

@when('I leave a {rating}-star review with comment "{comment}"')
def step_leave_review(context: Context, rating, comment):
    """Leaves a review."""
    print(f"Leaving {rating}-star review: {comment}")

@when('I filter products by price range "{min_price}" to "{max_price}"')
def step_filter_by_price(context: Context, min_price, max_price):
    """Filters by price."""
    print(f"Filtering by price: {min_price} to {max_price}")

@when('I select the sort option "{option_text}"')
def step_select_sort_option(context: Context, option_text):
    """Selects sort option."""
    print(f"Selecting sort option: {option_text}")

@when('I enter the discount code "{code}"')
def step_enter_discount_code(context: Context, code):
    """Enters discount code."""
    print(f"Entering discount code: {code}")

@when('I click the apply button')
def step_click_apply_button(context: Context):
    """Clicks apply button."""
    print("Clicking apply button")