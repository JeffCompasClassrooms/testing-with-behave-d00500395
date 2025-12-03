import behave_webdriver
from behave_webdriver.steps import *

def before_all(context):
    context.behave_driver = behave_webdriver.Chrome()

def after_all(context):
    context.behave_driver.quit()
