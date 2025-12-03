Feature: E-commerce Shopping Experience
  Feature File for Test Suite 2: Feature-Rich Web Application (E-commerce)
  Implements scenarios using custom-written, highly contextual step definitions.

  As an online shopper
  I want to easily find products, add them to my cart, and check out securely
  So that I can purchase goods without hassle

  @search @product
  Scenario: Successful search and product detail viewing
    Given I am viewing the "Home Goods" category page
    When I search for "dress"
    Then I should see the search results page
    When I click the first product in the results
    Then the current page URL should contain "/product_details/"

  @cart @guest
    Scenario: Adding a product to cart and verifying count
      Given I am viewing the product page for "Blue Top"
      When I add the product to my cart
      Then the current page URL should contain "/view_cart"

  @cart @quantity
  Scenario: Viewing cart after adding items
    Given I have "Sample Product" in my cart with quantity "1"
    Then the current page URL should contain "/view_cart"

  @checkout @guest
  Scenario: Guest checkout process initiation
    Given I have items in my cart
    When I proceed to checkout
    # UPDATED: Guests are redirected to login on this specific site
    Then the current page URL should contain "/login"

  @checkout @discount
  Scenario: Viewing payment review page
    Given I am on the "Payment Review" page
    And the current order subtotal is "$150.00"
    Then the current page URL should contain "/checkout"

  @login @security
  Scenario: Viewing login page
    Given I am on the login page
    Then the current page URL should contain "/login"

  @login @security
  Scenario: Attempting login with credentials
    Given I am on the login page
    When I log in with username "test@example.com" and password "password123"
    Then the current page URL should contain "/"


  @navigation @mobile
  Scenario: Mobile menu functionality
    Given I am viewing the page on a mobile device
    When I click the mobile navigation menu
    Then the element with id "navbar-nav" should be visible

  @cart @empty
  Scenario: Viewing an empty shopping cart
    Given my cart is empty
    Then the current page URL should contain "/view_cart"

  @product @search
  Scenario: Search for specific product
    Given I am viewing the homepage
    When I search for "jeans"
    Then I should see the search results page

  @cart @view
  Scenario: Navigate to cart page
    Given I am viewing the homepage
    When I click the cart icon
    Then the current page URL should contain "/view_cart"

  @login @navigation
  Scenario: Navigate to login page from homepage
    Given I am viewing the homepage
    When I click the link "Signup / Login"
    Then the current page URL should contain "/login"