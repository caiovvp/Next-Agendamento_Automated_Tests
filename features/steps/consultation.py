import random

from behave import *

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from features.fixtures import random_numbers, cpf, find_by_link


@when('go to consultation page')
def step_impl(context):
    consultation_anchor = find_by_link(context, '/consulta-cadastro')
    consultation_btn = consultation_anchor.find_elements_by_xpath('..')
    consultation_btn[0].click()
    WebDriverWait(context.browser, 5).until(EC.url_to_be('http://192.168.201.15:88/consulta-cadastro'))


@when('type invalid CPF')
def step_impl(context):
    cpf_input = context.browser.find_element_by_id('cpf')
    random_numbers(cpf_input, 11)


@when('type not registered CPF')
def step_impl(context):
    cpf_input = context.browser.find_element_by_id('cpf')
    cpf_input.send_keys(cpf())


@when('type registered CPF on upper input')
def step_impl(context):
    cpf_input = context.browser.find_element_by_id('header_cpf')
    cpf_list = []
    file = open("registered_cpf", "r")
    file_lines = file.readlines()
    for cpf in file_lines:
        cpf_list.append(cpf[:14])
    if len(cpf_list) > 0:
        registered_cpf = cpf_list[random.randrange(0, len(cpf_list))]
    else:
        raise ValueError('No registered cpf found on registered_cpf database')
    cpf_input.send_keys(registered_cpf)


@when('click on search button')
def step_impl(context):
    search_btn = context.browser.find_element_by_id('button-addon2')
    search_btn.click()


@then('close message box')
def step_impl(context):
    ok_button = context.browser.find_element_by_class_name('swal2-confirm')
    ok_button.click()


@then('show registration stats')
def step_impl(context):
    result = context.browser.find_element_by_class_name('result-container')
    tbody = result.find_element_by_tag_name('tbody')
    trs = tbody.find_elements_by_tag_name('tr')
    for tr in trs:
        assert tr.text != ''
