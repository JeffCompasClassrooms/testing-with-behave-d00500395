Feature:
    As a poor helpless student trying to learn how to use behave
    I want to use an easy but relevant sample page as practice for using the builtin steps
    So I don't lose my scholarship

    # 1
    Scenario: I open the locator page
        Given I open the url "https://testpages.herokuapp.com/pages/basics/locator-approaches/"
        Then I expect the url to not contain "#approaches"

    #2
    Scenario: I click on the link
        When I click on the link "partial link text link"
        Then I expect the url to contain "#approaches"

    #3
    Scenario: I open the job role page
        Given I open the url "https://testpages.herokuapp.com/pages/basics/multiple-elements-example/"
        Then I expect that element ".role-description" matches the text "Hover over a role to see its description"
        
    #4
    Scenario: I change the job role selection
        
        When I move to element "#programmer"
        And I click on the element "#programmer"
        Then I expect that element ".role-description" contains the text "Design, write, test, and maintain code to build software applications. Transform requirements into functional solutions using various programming languages and frameworks."

    #5
    Scenario: The submission message is hidden
        When I move to element ".role-container"
        Then I expect that element "#message" is not visible

    #6
    Scenario: I submit and can see submission message
        When I move to element "#submitBtn"
        And I click on the element "#submitBtn"
        And I pause for 4000ms
        Then I expect that element "#message" is visible
        
    #7
    Scenario: I fill out fields on a from
        Given I open the url "https://testpages.herokuapp.com/pages/forms/html-form/"
        When I add "Jeff" to the inputfield "input[name='username']"
        And I add "Jeff123" to the inputfield "input[name='password']"
        And I move to element "input[name='checkboxes[]'][value='cb2']"
        And I click on the element "input[name='checkboxes[]'][value='cb2']"
        And I move to element "input[value='rd1']"
        And I click on the element "input[value='rd1']"
        And I select the option with the value "ms3" for element "select[name='multipleselect[]']"
        And I select the option with the value "dd6" for element "select[name='dropdown']"
        And I move to element "input[type='submit']"
        And I click on the element "input[type='submit']"
        Then I expect that element ".explanation > *" contains the text "You submitted the form."

    #8
    Scenario: I am not redirected in 4.5 seconds
        Given I open the url "https://testpages.herokuapp.com/pages/navigation/javascript-redirects/"
        When I move to element "#delaygotobasic"
        When I click on the element "#delaygotobasic"
        And I pause for 4500ms
        Then I expect the url to not contain "redirected"

    #9
    Scenario: I am redirected in 5.5 seconds
        Given I open the url "https://testpages.herokuapp.com/pages/navigation/javascript-redirects/"
        When I move to element "#delaygotobasic"
        When I click on the element "#delaygotobasic"
        And I pause for 5500ms
        Then I expect the url to contain "redirected"

    #10
    Scenario: I see a countdown
        Given I open the url "https://testpages.herokuapp.com/pages/navigation/javascript-redirects/"
        When I click on the element "#delaynogoto"
        Then I expect that element "#countdown-render" is visible


