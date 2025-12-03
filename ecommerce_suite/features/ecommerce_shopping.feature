Feature: E-Commerce Shop Operations
  As a shopper
  I want to browse products, search, and manage my cart
  So that I can purchase items I like

  Background:
    Given I navigate to the Automation Exercise homepage

  Scenario: View all products
    When I navigate to the Products page
    Then I should see the list of all products
    And I should see the "ALL PRODUCTS" header

  Scenario: Search for a specific product
    When I navigate to the Products page
    And I search for the product "T-Shirt"
    Then I should see "SEARCHED PRODUCTS" in the results
    And all visible products should contain "T-Shirt" in their title

  Scenario: Verify Subscription in footer
    When I scroll down to the footer
    And I enter "subscriber@example.com" into the subscription input
    And I click the subscribe arrow
    Then I should see the subscription success message "You have been successfully subscribed!"

  Scenario: Add items to cart
    Given the cart is empty
    When I navigate to the Products page
    And I hover over the first product and click Add to Cart
    And I click Continue Shopping button
    And I navigate to the Cart page
    Then I should see 1 item in the cart

  Scenario: Remove item from cart
    Given the cart is empty
    Given I have added a product to the cart
    When I navigate to the Cart page
    And I click the "X" button to remove the item
    Then I should see that the cart is empty

  Scenario: View Category Products
    When I click on the "Women" category
    And I click on the "Dress" sub-category
    Then I should see "WOMEN - DRESS PRODUCTS" in the page header

  Scenario: View Brand Products
    When I navigate to the Products page
    And I click on the "Polo" brand in the sidebar
    Then I should see "BRAND - POLO PRODUCTS" in the page header

  Scenario: Add review on product
    When I navigate to the Products page
    And I click View Product on the first item
    And I submit a review with name "Reviewer", email "rev@test.com", and message "Great product!"
    Then I should see the review success message "Thank you for your review."

  Scenario: Verify Product Quantity in Cart
    Given the cart is empty
    When I navigate to the Products page
    And I click View Product on the first item
    And I increase the quantity to "4"
    And I click the Add to Cart button
    And I navigate to the Cart page
    Then I should see "4" items in the cart for that product

  Scenario: Verify Recommended Items are visible
    When I scroll to the bottom of the page
    Then I should see the "RECOMMENDED ITEMS" header
    And I should see recommended products

  Scenario: Add Recommended Item to Cart
    Given the cart is empty
    When I scroll to the bottom of the page
    And I click Add to Cart on a recommended item
    And I click View Cart in the modal
    Then I should see 1 item in the cart

  Scenario: Verify Scroll Up using Arrow button
    When I scroll to the bottom of the page
    And I click the scroll up arrow
    Then I should see the main slider text "Full-Fledged practice website for Automation Engineers"

  Scenario: Verify Scroll Up without Arrow button
    When I scroll to the bottom of the page
    And I scroll up to the top manually
    Then I should see the main slider text "Full-Fledged practice website for Automation Engineers"

  Scenario: Proceed to Checkout (Non-Logged In)
    Given the cart is empty
    Given I have added a product to the cart
    When I navigate to the Cart page
    And I click Proceed to Checkout
    Then I should see the checkout modal requesting login

  Scenario: Search Products and Verify Cart After Login
    Given the cart is empty
    When I navigate to the Products page
    And I search for the product "Jeans"
    And I hover over the first product and click Add to Cart
    And I click Continue Shopping button
    And I navigate to the Login/Signup page
    And I log in with email "testuser_unique@example.com" and password "password123"
    And I navigate to the Cart page
    Then I should see 1 item in the cart