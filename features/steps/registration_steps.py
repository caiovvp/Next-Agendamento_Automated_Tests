from datetime import date
import random
from behave import *

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from features.fixtures import fill_registration_form, random_date, save_and_clear, \
    show_message, validate_birth_date, find_and_clear_input, find_by_link, random_numbers, find_input


@given('go to the registration page')
def step_impl(context):
    registration_anchor = find_by_link(context, '/cadastro')
    registration_btn = registration_anchor.find_elements_by_xpath('..')
    registration_btn[0].click()
    WebDriverWait(context.browser, 5).until(EC.url_to_be('http://192.168.201.15:88/cadastro'))


@when('fill the form with valid infos')
def step_impl(context):
    fill_registration_form(context)


@when('required information is blank')
def step_impl(context):
    registration_div = context.browser.find_element_by_xpath('/html/body/div/div[2]/div[2]')
    required_inputs = create_req_list(registration_div, 'input')
    required_selects = create_req_list(registration_div, 'select')
    clear_inputs(context, required_inputs)
    clear_inputs(context, required_selects)


def create_req_list(div, tag):
    tag_list = div.find_elements_by_tag_name(tag)
    req_list = []
    for web_ele in tag_list:
        if web_ele.get_attribute('required'):
            req_list.append(web_ele)
    return req_list


def clear_inputs(context, req_list):
    for req_ele in req_list:
        input_value = req_ele.get_attribute('value')
        req_options = req_ele.find_elements_by_tag_name('option')
        if len(req_options) > 0:
            i = 0
            for req_option in req_options:
                if req_option.get_attribute('value') == '':
                    req_option.click()
                    send(context, 'form')
                    index_list = []
                    for num in range(0, len(req_options)):
                        if num != i:
                            index_list.append(num)
                    random.shuffle(index_list)
                    req_options[index_list[0]].click()
                i += 1
        else:
            req_ele.clear()
            send(context, 'form')
            req_ele.send_keys(f'{input_value}')


@when('send {info_name}')
def send(context, info_name):
    if info_name == 'valid-form':
        context.cpf_number = context.browser.find_element_by_id('cpf').get_attribute('value')
        context.browser.find_element_by_id('email').send_keys('.com.vc')
        context.browser.find_element_by_class_name('btn-success').click()
    elif info_name == 'form':
        context.browser.find_element_by_class_name('btn-success').click()
    else:
        input = context.browser.find_element_by_class_name('btn-primary')
        input.click()


@when('cpf is not valid')
def step_impl(context):
    cpf_input = context.browser.find_element_by_id('cpf')
    value = save_and_clear(cpf_input)
    random_numbers(cpf_input, 11)
    send(context, 'form')
    WebDriverWait(context.browser, 5).until(EC.visibility_of_element_located((By.ID, "swal2-html-container")))
    show_message(context)
    context.browser.find_element_by_class_name('swal2-confirm').click()
    cpf_input = context.browser.find_element_by_id('cpf')
    cpf_input.clear()
    cpf_input.send_keys(value)


@when('birth date is not valid')
def step_impl(context):
    input = random_date(date.today(), date(9999, 12, 31))
    validate_birth_date(context, input)


@when('birth date is incomplete')
def step_impl(context):
    validate_birth_date(context, '05')


@when('email without @')
def step_impl(context):
    email_input = context.browser.find_element_by_id('email')
    context.email_value = save_and_clear(email_input)
    email_input.send_keys('suporte02connect.com.vc')


@when('email without .com')
def step_impl(context):
    email_input = find_and_clear_input(context, 'email')
    email_input.send_keys('suporte02@connect')


@then('show message')
def step_impl(context):
    show_message(context)


@then('form not accepted')
def step_impl(context):
    assert EC.text_to_be_present_in_element((By.ID, 'swal2-title'), 'Sucesso!')


@then('form accepted')
def step_impl(context):
    WebDriverWait(context.browser, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'mt-5')))
    WebDriverWait(context.browser, 5).until(EC.visibility_of_element_located((By.TAG_NAME, 'img')))
    show_message(context)
    file = open("registered_cpf", "a+")
    file.write(f'{context.cpf_number}\r')
    file.close()
