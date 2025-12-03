from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.common.exceptions import ElementClickInterceptedException

def clear_cart(driver):
    # Remove all items from the cart if present
    try:
        driver.get("https://automationexercise.com/view_cart")
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "cart_quantity_delete"))
        )
        delete_buttons = driver.find_elements(By.CLASS_NAME, "cart_quantity_delete")
        for btn in delete_buttons:
            try:
                btn.click()
                time.sleep(0.5)  # Wait for DOM update
            except Exception:
                pass
    except Exception:
        pass  # No items to delete or cart already empty


@given('the cart is empty')
def given_cart_is_empty_step(context):
    close_ads_iframe(context.behave_driver)
    clear_cart(context.behave_driver)


# --- Common / Navigation Steps ---

@given('I navigate to the Automation Exercise homepage')
def navigate_homepage_step(context):
    driver = context.behave_driver
    driver.get("https://automationexercise.com/")
    close_ads_iframe(driver)
    # WebDriverWait(driver, 10).until(
    #     EC.visibility_of_element_located((By.XPATH, "//img[@alt='Website for automation practice']"))
    # )

@when('I navigate to the Login/Signup page')
def navigate_login_signup_step(context):
    driver = context.behave_driver
    close_ads_iframe(driver)
    try:
        elem = driver.find_element(By.CSS_SELECTOR, "a[href='/login']")
        driver.execute_script("arguments[0].scrollIntoView();", elem)
        try:
            elem.click()
        except ElementClickInterceptedException as e:
            print(f"[WARN] Click intercepted: {e}. Trying JS click.")
            driver.execute_script("arguments[0].click();", elem)
        except Exception as e:
            print(f"[ERROR] JS click also failed: {e}")
            raise AssertionError("Could not click Login/Signup link.")
    except Exception as e:
        raise AssertionError(f"Login/Signup link not found or not clickable: {e}")

@when('I navigate to the Contact Us page')
def navigate_contact_us_step(context):
    context.behave_driver.find_element(By.CSS_SELECTOR, "a[href='/contact_us']").click()

@when('I navigate to the Products page')
def navigate_products_page_step(context):
    driver = context.behave_driver
    close_ads_iframe(driver)
    driver.find_element(By.CSS_SELECTOR, "a[href='/products']").click()

@when('I navigate to the Cart page')
def navigate_cart_page_step(context):
    driver = context.behave_driver
    max_retries = 3
    for attempt in range(max_retries):
        try:
            elem = driver.find_element(By.CSS_SELECTOR, "a[href='/view_cart']")
            driver.execute_script("arguments[0].scrollIntoView();", elem)
            try:
                elem.click()
                return
            except Exception as e:
                print(f"[WARN] Normal click failed: {e}. Trying JS click.")
                try:
                    driver.execute_script("arguments[0].click();", elem)
                    return
                except Exception as js_e:
                    print(f"[ERROR] JS click also failed: {js_e}")
                    time.sleep(1)
        except Exception as retry_e:
            print(f"[ERROR] Retry {attempt+1} failed to find/click Cart page link: {retry_e}")
            time.sleep(1)
    print(f"[ERROR] Could not click Cart page link after {max_retries} attempts.")

@when('I click on the Test Cases button')
def click_test_cases_button_step(context):
    context.behave_driver.find_element(By.CSS_SELECTOR, "a[href='/test_cases']").click()

@then('I should be on the "Test Cases" page')
def be_on_test_cases_page_step(context):
    WebDriverWait(context.behave_driver, 5).until(
        EC.url_contains("/test_cases")
    )

@then('the page title should be "{title}"')
def verify_page_title_step(context, title):
    assert context.behave_driver.title == title

# --- Account Management Steps ---

@when('I enter "{name}" and "{email}" into the new user signup')
def enter_new_user_signup_step(context, name, email):
    # Appending timestamp to email to ensure uniqueness if needed
    unique_email = email.replace("@", f"_{int(time.time())}@")
    context.created_email = unique_email # Store for login steps if needed
    
    context.behave_driver.find_element(By.CSS_SELECTOR, "input[data-qa='signup-name']").send_keys(name)
    context.behave_driver.find_element(By.CSS_SELECTOR, "input[data-qa='signup-email']").send_keys(unique_email)

@when('I click the Signup button')
def click_signup_button_step(context):
    context.behave_driver.find_element(By.CSS_SELECTOR, "button[data-qa='signup-button']").click()

@when('I fill in the account details with password "{password}", first name "{first}", last name "{last}", and address "{address}"')
def fill_account_details_step(context, password, first, last, address):
    driver = context.behave_driver
    # Select Title
    driver.find_element(By.ID, "id_gender1").click()
    
    driver.find_element(By.ID, "password").send_keys(password)
    
    # Date of birth (generic selection)
    driver.find_element(By.ID, "days").send_keys("1")
    driver.find_element(By.ID, "months").send_keys("January")
    driver.find_element(By.ID, "years").send_keys("2000")
    
    driver.find_element(By.ID, "first_name").send_keys(first)
    driver.find_element(By.ID, "last_name").send_keys(last)
    driver.find_element(By.ID, "address1").send_keys(address)
    driver.find_element(By.ID, "country").send_keys("United States")
    driver.find_element(By.ID, "state").send_keys("NY")
    driver.find_element(By.ID, "city").send_keys("New York")
    driver.find_element(By.ID, "zipcode").send_keys("10001")
    driver.find_element(By.ID, "mobile_number").send_keys("1234567890")

@when('I click the Create Account button')
def click_create_account_button_step(context):
    context.behave_driver.find_element(By.CSS_SELECTOR, "button[data-qa='create-account']").click()

@then('I should see the "{message}" success message')
def see_success_message_step(context, message):
    element = WebDriverWait(context.behave_driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h2[data-qa='account-created']"))
    )
    assert message.lower() in element.text.lower()

@when('I log in with email "{email}" and password "{password}"')
def login_with_email_password_step(context, email, password):
    context.behave_driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-email']").send_keys(email)
    context.behave_driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-password']").send_keys(password)
    context.behave_driver.find_element(By.CSS_SELECTOR, "button[data-qa='login-button']").click()

@then('I should see the logged in user "{username}" in the navbar')
def see_logged_in_user_navbar_step(context, username):
    element = WebDriverWait(context.behave_driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Logged in as')]"))
    )
    assert username in element.text

@then('I should see the error message "{message}"')
def see_error_message_step(context, message):
    element = context.behave_driver.find_element(By.CSS_SELECTOR, "form[action='/login'] p")
    assert message in element.text

@given('I am logged in with "{email}" and "{password}"')
def given_logged_in_with_email_password_step(context, email, password):
    # Reuse steps
    context.execute_steps(u'''
        When I navigate to the Login/Signup page
        And I log in with email "{}" and password "{}"
    '''.format(email, password))

@when('I click the Logout button')
def click_logout_button_step(context):
    context.behave_driver.find_element(By.CSS_SELECTOR, "a[href='/logout']").click()

@then('I should be redirected to the Login page')
def should_be_redirected_to_login_page_step(context):
    WebDriverWait(context.behave_driver, 5).until(
        EC.url_contains("/login")
    )

@when('I click the Delete Account button')
def click_delete_account_button_step(context):
    context.behave_driver.find_element(By.CSS_SELECTOR, "a[href='/delete_account']").click()

@then('I should see the "Account Deleted!" confirmation')
def see_account_deleted_confirmation_step(context):
    WebDriverWait(context.behave_driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h2[data-qa='account-deleted']"))
    )

# --- Contact Form Steps ---

@when('I submit the contact form with name "{name}", email "{email}", subject "{subject}", and message "{msg}"')
def step_impl(context, name, email, subject, msg):
    context.behave_driver.find_element(By.NAME, "name").send_keys(name)
    context.behave_driver.find_element(By.NAME, "email").send_keys(email)
    context.behave_driver.find_element(By.NAME, "subject").send_keys(subject)
    context.behave_driver.find_element(By.NAME, "message").send_keys(msg)
    context.behave_driver.find_element(By.NAME, "submit").click()

@when('I accept the browser alert')
def accept_browser_alert_step(context):
    WebDriverWait(context.behave_driver, 5).until(EC.alert_is_present())
    context.behave_driver.switch_to.alert.accept()

@then('I should see the success details "{message}"')
def see_success_details_step(context, message):
    element = WebDriverWait(context.behave_driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".status.alert.alert-success"))
    )
    assert message in element.text

# --- Shop Operations Steps ---

@then('I should see the list of all products')
def see_list_of_all_products_step(context):
    products = context.behave_driver.find_elements(By.CLASS_NAME, "features_items")
    assert len(products) > 0

def close_ads_iframe(driver):
    # Hide ad iframes
    try:
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            driver.execute_script("arguments[0].style.display='none';", iframe)
    except Exception:
        pass
    # Try to click close button inside adsbygoogle overlays, else hide
    try:
        ads = driver.find_elements(By.CSS_SELECTOR, "ins.adsbygoogle")
        for ad in ads:
            try:
                close_btn = ad.find_element(By.CSS_SELECTOR, "[aria-label='Close'], .close, button, [role='button']")
                if close_btn.is_displayed() and close_btn.is_enabled():
                    close_btn.click()
                    continue
            except Exception:
                pass
            driver.execute_script("arguments[0].style.display='none';", ad)
    except Exception:
        pass

@then('I should see the "{header_text}" header')
def see_header_text_step(context, header_text):
    driver = context.behave_driver
    header = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h2.title.text-center"))
    )
    assert header.is_displayed(), "Header is not visible."

@when('I search for the product "{product_name}"')
def search_for_product_step(context, product_name):
    context.behave_driver.find_element(By.ID, "search_product").send_keys(product_name)
    context.behave_driver.find_element(By.ID, "submit_search").click()

@then('I should see "SEARCHED PRODUCTS" in the results')
def see_searched_products_in_results_step(context):
    header = context.behave_driver.find_element(By.CSS_SELECTOR, "h2.title.text-center")
    assert "SEARCHED PRODUCTS" in header.text

@then('all visible products should contain "{text}" in their title')
def all_visible_products_contain_text_step(context, text):
    product_names = context.behave_driver.find_elements(By.CSS_SELECTOR, ".productinfo p")
    for name in product_names:
        assert text.lower() in name.text.lower()

@when('I scroll down to the footer')
def scroll_down_to_footer_step(context):
    context.behave_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

@when('I enter "{email}" into the subscription input')
def enter_subscription_email_step(context, email):
    context.behave_driver.find_element(By.ID, "susbscribe_email").send_keys(email)

@when('I click the subscribe arrow')
def click_subscribe_arrow_step(context):
    context.behave_driver.find_element(By.ID, "subscribe").click()

@then('I should see the subscription success message "{message}"')
def see_subscription_success_message_step(context, message):
    element = WebDriverWait(context.behave_driver, 5).until(
        EC.visibility_of_element_located((By.ID, "success-subscribe"))
    )
    assert message in element.text

@when('I hover over the first product and click Add to Cart')
def hover_and_add_first_product_step(context):
    # Robustly click the 'Add to cart' button for the first product, retrying if stale
    from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
    driver = context.behave_driver
    max_retries = 5
    for attempt in range(max_retries):
        try:
            product = driver.find_elements(By.CLASS_NAME, "single-products")[0]
            driver.execute_script("arguments[0].scrollIntoView();", product)
            actions = ActionChains(driver)
            actions.move_to_element(product).perform()
            add_btn = product.find_element(By.CSS_SELECTOR, ".product-overlay a.add-to-cart")
            try:
                driver.execute_script("arguments[0].click();", add_btn)
            except ElementClickInterceptedException as e:
                print(f"[WARN] Click intercepted: {e}. Trying JS click.")
                driver.execute_script("arguments[0].click();", add_btn)
            # Wait for cart modal or confirmation
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#cartModal, .modal-content, .modal-backdrop"))
            )
            return
        except StaleElementReferenceException as e:
            print(f"[WARN] Stale element in add-to-cart, retrying ({attempt+1}/{max_retries}): {e}")
            time.sleep(1)
        except Exception as e:
            print(f"[ERROR] Exception in add-to-cart: {e}")
            time.sleep(1)
    raise AssertionError("Failed to click Add to Cart after multiple retries.")

@when('I click Continue Shopping button')
def click_continue_shopping_button_step(context):
    btn = WebDriverWait(context.behave_driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.close-modal"))
    )
    btn.click()

@then('I should see {count:d} item in the cart')
def see_item_count_in_cart_step(context, count):
    rows = context.behave_driver.find_elements(By.CSS_SELECTOR, "tbody tr[id^='product-']")
    assert len(rows) == count, f"Expected {count} item(s) in cart, found {len(rows)}."

@given('I have added a product to the cart')
def have_added_product_to_cart_step(context):
    context.execute_steps(u'When I navigate to the Products page')
    context.execute_steps(u'When I hover over the first product and click Add to Cart')
    try:
        context.execute_steps(u'When I click Continue Shopping button')
    except Exception as e:
        driver = context.behave_driver
        try:
            html = driver.page_source
            print(f"[ERROR] Could not click Continue Shopping. Page HTML:\n{html[:2000]}")
        except Exception as e2:
            print(f"[ERROR] Could not get page HTML: {e2}")
        raise
    print("[DEBUG] Product should now be in cart.")

@when('I click the "X" button to remove the item')
def click_remove_item_button_step(context):
    context.behave_driver.find_element(By.CLASS_NAME, "cart_quantity_delete").click()

@then('I should see that the cart is empty')
def see_cart_is_empty_step(context):
    # Wait for the row to disappear or the empty message
    WebDriverWait(context.behave_driver, 5).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "cart_quantity_delete"))
    )
    # Verify the empty text appears
    body_text = context.behave_driver.find_element(By.ID, "empty_cart").text
    assert "Cart is empty" in body_text

# --- MISSING STEP DEFINITIONS ---

@when('I increase the quantity to "{qty}"')
def increase_quantity_step(context, qty):
    driver = context.behave_driver
    qty_input = driver.find_element(By.ID, "quantity")
    qty_input.clear()
    qty_input.send_keys(qty)

@when('I click the Add to Cart button')
def click_add_to_cart_button_step(context):
    driver = context.behave_driver
    add_btn = driver.find_element(By.CSS_SELECTOR, "button.add-to-cart, .product-information button")
    driver.execute_script("arguments[0].scrollIntoView();", add_btn)
    try:
        add_btn.click()
    except Exception:
        driver.execute_script("arguments[0].click();", add_btn)

@then('I should see "{qty}" items in the cart for that product')
def see_qty_items_in_cart_for_product_step(context, qty):
    driver = context.behave_driver
    # Wait for the cart table and product row to appear
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "tbody tr[id^='product-']"))
    )
    # Find the first product row
    row = driver.find_element(By.CSS_SELECTOR, "tbody tr[id^='product-']")
    # Find the cart_quantity cell and its button
    qty_cell = row.find_element(By.CLASS_NAME, "cart_quantity")
    qty_btn = qty_cell.find_element(By.TAG_NAME, "button")
    qty_text = qty_btn.text.strip()
    print(f"[DEBUG] Cart quantity button value: {qty_text}")
    assert qty_text == str(qty), f"Expected {qty} items in cart for product, found {qty_text}."

@when('I scroll to the bottom of the page')
def scroll_to_bottom_step(context):
    driver = context.behave_driver
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

@then('I should see recommended products')
def see_recommended_products_step(context):
    driver = context.behave_driver
    try:
        section = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "recommended_items"))
        )
        assert section.is_displayed(), "Recommended items section is not visible."
    except Exception as e:
        raise AssertionError(f"Recommended items section not found or not visible: {e}")

@when('I click Add to Cart on a recommended item')
def add_to_cart_recommended_step(context):
    driver = context.behave_driver
    # Always navigate to the homepage (where recommended section is visible)
    driver.get("https://automationexercise.com/")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//img[@alt='Website for automation practice']"))
    )
    close_ads_iframe(driver)
    try:
        section = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "recommended_items"))
        )
        carousel_inner = section.find_element(By.CSS_SELECTOR, ".carousel-inner")
        active_items = carousel_inner.find_elements(By.CSS_SELECTOR, ".item.active")
        if not active_items:
            print(f"[DEBUG] .carousel-inner HTML: {carousel_inner.get_attribute('outerHTML')}")
            raise AssertionError("No .item.active found in recommended carousel.")
        active_item = active_items[0]
        btns = active_item.find_elements(By.CSS_SELECTOR, "a[data-product-id].add-to-cart")
        if not btns:
            print(f"[DEBUG] .item.active HTML: {active_item.get_attribute('outerHTML')}")
            raise AssertionError("No a[data-product-id].add-to-cart found in .item.active.")
        for i, b in enumerate(btns):
            print(f"[DEBUG] Button {i} HTML: {b.get_attribute('outerHTML')}")
        # Click the first visible button
        for btn in btns:
            if btn.is_displayed():
                driver.execute_script("arguments[0].scrollIntoView();", btn)
                try:
                    btn.click()
                except ElementClickInterceptedException as e:
                    print(f"[WARN] Click intercepted: {e}. Trying JS click.")
                    driver.execute_script("arguments[0].click();", btn)
                except Exception as e:
                    print(f"[ERROR] JS click also failed: {e}")
                    raise AssertionError("Could not click Add to Cart on recommended item.")
                return
        print("[ERROR] No visible Add to Cart button found in recommended section.")
        raise AssertionError("No visible Add to Cart button found in recommended section.")
    except Exception as e:
        print(f"[ERROR] Could not find Add to Cart in recommended section: {e}")
        try:
            print(f"[DEBUG] Full page HTML: {driver.page_source[:2000]}")
            driver.save_screenshot("recommended_section_failure.png")
            print("[DEBUG] Screenshot saved as recommended_section_failure.png")
        except Exception as ex:
            print(f"[DEBUG] Could not get page HTML or screenshot: {ex}")
        raise AssertionError(f"Recommended item Add to Cart button not found or not clickable: {e}")

@when('I click View Cart in the modal')
def click_view_cart_modal_step(context):
    driver = context.behave_driver
    # Wait for modal and click View Cart
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#cartModal, .modal-content"))
    )
    view_cart_btn = driver.find_element(By.CSS_SELECTOR, "a[href='/view_cart']")
    driver.execute_script("arguments[0].scrollIntoView();", view_cart_btn)
    try:
        view_cart_btn.click()
    except Exception:
        driver.execute_script("arguments[0].click();", view_cart_btn)

@when('I click the scroll up arrow')
def click_scroll_up_arrow_step(context):
    driver = context.behave_driver
    arrow = driver.find_element(By.ID, "scrollUp")
    driver.execute_script("arguments[0].scrollIntoView();", arrow)
    try:
        arrow.click()
    except Exception:
        driver.execute_script("arguments[0].click();", arrow)

@then('I should see the main slider text "{text}"')
def see_main_slider_text_step(context, text):
    driver = context.behave_driver
    slider = driver.find_element(By.CSS_SELECTOR, ".carousel-inner .item.active h2")
    assert text in slider.text

@when('I scroll up to the top manually')
def scroll_up_to_top_manually_step(context):
    driver = context.behave_driver
    driver.execute_script("window.scrollTo(0, 0);")

@when('I click Proceed to Checkout')
def click_proceed_to_checkout_step(context):
    driver = context.behave_driver
    close_ads_iframe(driver)
    try:
        btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.check_out"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", btn)
        try:
            btn.click()
        except ElementClickInterceptedException as e:
            print(f"[WARN] Click intercepted: {e}. Trying JS click.")
            driver.execute_script("arguments[0].click();", btn)
        except Exception as e:
            print(f"[ERROR] JS click also failed: {e}")
            raise AssertionError("Could not click Proceed to Checkout.")
    except Exception as e:
        raise AssertionError(f"Proceed to Checkout button not found or not clickable: {e}")

@then('I should see the checkout modal requesting login')
def see_checkout_modal_login_step(context):
    driver = context.behave_driver
    modal = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "checkoutModal"))
    )
    assert modal.is_displayed()

@when('I click on the "{category}" category')
def click_sidebar_category_step(context, category):
    driver = context.behave_driver
    # Find the sidebar category link by href and text
    xpath = f"//div[@class='left-sidebar']//a[@data-toggle='collapse' and contains(., '{category}') and @href='#{category}']"
    try:
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        elem = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].scrollIntoView();", elem)
        try:
            elem.click()
        except Exception:
            driver.execute_script("arguments[0].click();", elem)
    except Exception as e:
        print(f"[ERROR] Could not click category '{category}': {e}")

@when('I click on the "{sub_category}" sub-category')
def click_sidebar_sub_category_step(context, sub_category):
    driver = context.behave_driver
    # Sub-category links are inside the expanded panel for the category
    xpath = f"//div[@class='panel-collapse in']//ul/li/a[contains(., '{sub_category}') or normalize-space(text())='{sub_category}']"
    try:
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        elem = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].scrollIntoView();", elem)
        try:
            elem.click()
        except Exception:
            driver.execute_script("arguments[0].click();", elem)
    except Exception as e:
        print(f"[ERROR] Could not click sub-category '{sub_category}': {e}")

@then('I should see "{text}" in the page header')
def see_page_header_text_step(context, text):
    header = WebDriverWait(context.behave_driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h2.title.text-center"))
    )
    assert text in header.text

@when('I click on the "{brand}" brand in the sidebar')
def click_sidebar_brand_step(context, brand):
    driver = context.behave_driver
    # Brand links are in the brands-name list, match by href and text
    xpath = f"//div[@class='brands-name']//a[contains(@href, '/brand_products') and contains(., '{brand}') or normalize-space(text())='{brand}']"
    try:
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        elem = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].scrollIntoView();", elem)
        try:
            elem.click()
        except Exception:
            driver.execute_script("arguments[0].click();", elem)
    except Exception as e:
        print(f"[ERROR] Could not click brand '{brand}': {e}")

@when('I click View Product on the first item')
def click_view_product_first_item_step(context):
    driver = context.behave_driver
    close_ads_iframe(driver)
    try:
        elem = driver.find_element(By.CSS_SELECTOR, ".choose a")
        driver.execute_script("arguments[0].scrollIntoView();", elem)
        try:
            elem.click()
        except ElementClickInterceptedException as e:
            print(f"[WARN] Click intercepted: {e}. Trying JS click.")
            driver.execute_script("arguments[0].click();", elem)
        except Exception as e:
            print(f"[ERROR] JS click also failed: {e}")
            raise AssertionError("Could not click View Product link.")
    except Exception as e:
        raise AssertionError(f"View Product link not found or not clickable: {e}")

@when('I submit a review with name "{name}", email "{email}", and message "{msg}"')
def submit_review_step(context, name, email, msg):
    WebDriverWait(context.behave_driver, 5).until(
        EC.visibility_of_element_located((By.ID, "name"))
    )
    context.behave_driver.find_element(By.ID, "name").send_keys(name)
    context.behave_driver.find_element(By.ID, "email").send_keys(email)
    context.behave_driver.find_element(By.ID, "review").send_keys(msg)
    context.behave_driver.find_element(By.ID, "button-review").click()

@then('I should see the review success message "{message}"')
def see_review_success_message_step(context, message):
    element = WebDriverWait(context.behave_driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success span"))
    )
    assert message in element.text
