import behave_webdriver
from behave_webdriver.steps import *

def before_all(context):
    context.behave_driver = behave_webdriver.Chrome.headless()
    # Set a larger window size for headless mode to prevent element overlap issues
    context.behave_driver.set_window_size(1920, 1080)

def after_all(context):
    context.behave_driver.quit()