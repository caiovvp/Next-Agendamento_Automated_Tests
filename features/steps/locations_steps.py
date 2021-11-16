from behave import *

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from features.fixtures import find_by_link


@given('user is on home page')
def step_impl(context):
    context.browser.get('http://192.168.201.15:88/')
    WebDriverWait(context.browser, 5).until(EC.url_to_be('http://192.168.201.15:88/'))


@when('go to locations page')
def step_impl(context):
    locations_anchor = find_by_link(context, '/locais-de-vacinacao')
    locations_btn = locations_anchor.find_elements_by_xpath('..')
    locations_btn[0].click()
    WebDriverWait(context.browser, 5).until(EC.url_to_be('http://192.168.201.15:88/locais-de-vacinacao'))


@when('click on address icon')
def step_impl(context):
    locations_div = context.browser.find_element_by_class_name('border-1')
    locations_list = locations_div.find_elements_by_tag_name('td')
    for loc in locations_list:
        anchor = loc.find_element_by_tag_name('a')
        link = anchor.get_attribute('href')
        handles = [context.browser.window_handles]
        anchor.click()
        WebDriverWait(context.browser, 5).until(EC.new_window_is_opened(handles))
        context.browser.switch_to.window(context.browser.window_handles[1])
        WebDriverWait(context.browser, 5).until(EC.url_to_be(link))
        context.browser.close()
        context.browser.switch_to.window(context.browser.window_handles[0])


@then('open google maps page for that address')
def step_impl(context):
    # Verification already being done on the step before
    pass