from behave import given, when, then
from wikipedia_suite.pages.wikipedia_page import WikipediaPage

@given('I open the browser')
def step_open_browser(context):
    # Driver is initialized in environment.py's before_all hook
    pass

@given('I navigate to "https://www.wikipedia.org/"')
def step_navigate_to_home(context):
    context.wikipedia_page = WikipediaPage(context.webdriver)
    context.wikipedia_page.navigate("https://www.wikipedia.org/")

@then('the page title should be "Wikipedia"')
def step_title_should_be_wikipedia(context):
    context.wikipedia_page.wait_for_title_to_be("Wikipedia")

@then('the element "#searchInput" should be visible')
def step_search_input_visible(context):
    context.wikipedia_page.is_element_visible(context.wikipedia_page.SEARCH_INPUT)

@when('I fill in "#searchInput" with "Python"')
def step_search_for_python(context, ):
    context.wikipedia_page.search_for("Python")

@when('I click on the element "button[type=\'submit\']"')
def step_click_search_button(context):
    # Already part of search_for step in the Page Object
    pass

@then('the page title should contain "Python"')
def step_title_contains_python(context):
    context.wikipedia_page.wait_for_title_to_contain("Python")

@when('I click on the element "#js-link-box-en"') 
def step_click_random_article(context):
    context.wikipedia_page.click_element(context.wikipedia_page.ENGLISH_LINK)

@then('the page title should contain "Wikipedia"')
def step_title_contains_wikipedia(context):
    context.wikipedia_page.wait_for_title_to_contain("Wikipedia")

@when('I click on the element "#js-link-box-ja"')
def step_click_random_article(context):
    context.wikipedia_page.click_element(context.wikipedia_page.JAPAN_LINK)

@then('the current URL should contain "/wiki/"')
def step_url_contains_wiki(context):
    context.wikipedia_page.wait_for_url_to_contain("/wiki/")

@then('the element ".footer" should be visible')
def step_footer_visible(context):
    context.wikipedia_page.is_element_visible(context.wikipedia_page.FOOTER)

@then('the element ".central-featured-logo" should be visible')
def step_logo_visible(context):
    context.wikipedia_page.is_element_visible(context.wikipedia_page.LOGO)

@then('the element ".central-featured-lang" should be visible')
def step_lang_links_visible(context):
    context.wikipedia_page.is_element_visible(context.wikipedia_page.LANGUAGE_LINKS)

@then('the element "button[type=\'submit\']" should be present')
def step_search_button_present(context):
    context.wikipedia_page.is_element_present(context.wikipedia_page.SEARCH_BUTTON)

@then('the element "#searchLanguage" should be present')
def step_lang_dropdown_present(context):
    context.wikipedia_page.is_element_present(context.wikipedia_page.LANGUAGE_DROPDOWN)