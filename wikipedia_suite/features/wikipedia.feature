Feature: Wikipedia basic functionality using built-in behave-webdriver steps

  Background:
    Given I open the browser
    And I navigate to "https://www.wikipedia.org/"

  # 1
  Scenario: Load the Wikipedia homepage
    Then the page title should be "Wikipedia"

  # 2
  Scenario: Verify the search box is visible
    Then the element "#searchInput" should be visible

  # 3
  Scenario: Search for Python
    When I fill in "#searchInput" with "Python"
    And I click on the element "button[type='submit']"
    Then the page title should contain "Python"

  # 4
  Scenario: Select English language
    When I click on the element "#js-link-box-en"
    Then the page title should contain "Wikipedia"

  # 5
  Scenario: Select the Japanese language
    When I click on the element "#js-link-box-ja"
    Then the current URL should contain "/wiki/"

  # 6
  Scenario: Footer should be visible
    Then the element ".footer" should be visible

  # 7
  Scenario: Verify logo is visible
    Then the element ".central-featured-logo" should be visible

  # 8
  Scenario: Check that language links exist
    Then the element ".central-featured-lang" should be visible

  # 9
  Scenario: Verify search button exists
    Then the element "button[type='submit']" should be present

  # 10
  Scenario: Verify languages dropdown is present
    Then the element "#searchLanguage" should be present
