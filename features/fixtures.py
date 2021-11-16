from datetime import date
import datetime
import random
from json import loads

from ipython_genutils.py3compat import xrange
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver import Firefox
from selenium.webdriver import DesiredCapabilities, Remote
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# FUNCTION THAT INSTANCES THAT THE BROWSER IS CHROME AND THAT IT QUITS ONCE THE TEST IS OVER
def browser_chrome(context):
    # -- BEHAVE-FIXTURE: Similar to @contextlib.contextmanager
    # -- IF WANT TO RUN ON CONNECT REMOTE SERVER
    # capability = DesiredCapabilities.FIREFOX
    # context.browser = Remote('http://srv01.connect.com.vc:4444/wd/hub', capability)
    # -- IF WANT TO RUN ON LOCAL MACHINE FIREFOX
    context.browser = Firefox(executable_path='C:\Selenium WebDriver\geckodriver.exe')
    yield context.browser
    # -- CLEANUP-FIXTURE PART:
    # context.browser.quit()


# FUNCTION TO TIMEOUT THE TEST IF NECESSARY
def timeout_for_page_load(context):
    context.browser.set_page_load_timeout(5)


# -- NOTE: Change False for True if you want ipdb debugger running when an error happens
BEHAVE_DEBUG_ON_ERROR = False
def setup_debug_on_error(userdata):
    global BEHAVE_DEBUG_ON_ERROR
    BEHAVE_DEBUG_ON_ERROR = userdata.getbool("BEHAVE_DEBUG_ON_ERROR")


# LOAD INFORMATION ON THE STEP DEFINITION AND RUN CONFIRM_MESSAGE() WITH THE PARAMETERS LOADED
def show_message(context):
    text_from_step = loads(context.text)
    WebDriverWait(context.browser, 5).until(EC.presence_of_element_located((By.XPATH, text_from_step['web_ele'])))
    confirm_message(context, text_from_step['web_ele'], text_from_step['message'])


# CONFIRM IF MESSAGE IS INSIDE THE TEXT OF A WEB ELEMENT
def confirm_message(context, web_ele, message):
    box = context.browser.find_element_by_xpath(web_ele)
    assert message in box.text


# RETURNS A WEB ELEMENT THAT CONTAINS THE HREF "LINK" IN ITS PROPERTIES
def find_by_link(context, link):
    anchors_list = context.browser.find_elements_by_tag_name('a')
    for element in anchors_list:
        if link in element.get_attribute('href'):
            element_parent = element.find_element_by_xpath('..')
            return element_parent


# CALCULATES A RANDOM CPF AND RETURNS IT (NOT FORMATTED, ONLY NUMBERS)
def cpf():
    def calculate_cpf(digs):
        s = 0
        qtd = len(digs)
        for i in xrange(qtd):
            s += n[i] * (1 + qtd - i)
        res = 11 - s % 11
        if res >= 10:
            return 0
        return res

    n = [random.randrange(10) for i in xrange(9)]
    n.append(calculate_cpf(n))
    n.append(calculate_cpf(n))
    return "%d%d%d%d%d%d%d%d%d%d%d" % tuple(n)


# CALCULATES A RANDOM INDEX FOR AN ITEM ON A LIST
def random_option(options_list):
    if len(options_list) == 1:
        random_num = 0
    else:
        random_num = random.randint(0, (len(options_list) - 1))
    return random_num


# GENERATE RANDOM DATE TIME AND RETURNS IT
def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_datetime = start_date + datetime.timedelta(days=random_number_of_days)
    return random_datetime.strftime('%d\%m\%Y')


# FILL UP ALL FIELDS OF THE REGISTRATION FORM WITH VALID INFORMATION
def fill_registration_form(context):
    location_select = context.browser.find_element_by_id('local_vacinacao')
    location_options = location_select.find_elements_by_tag_name('option')
    location_options[random_option(location_options)].click()

    cns_input = context.browser.find_element_by_id('cns')
    for _ in range(15):
        cns_input.send_keys(random.randint(0, 9))

    cpf_input = context.browser.find_element_by_id('cpf')
    cpf_input.send_keys(cpf())

    group_select = context.browser.find_element_by_id('grupo')
    group_options = group_select.find_elements_by_tag_name('option')
    group_options[random_option(group_options)].click()

    name_input = context.browser.find_element_by_id('nome')
    name_input.send_keys('Integra Teste')

    birth_date_input = context.browser.find_element_by_id('nascimento')
    birth_date_input.send_keys(f'{random_date(date(1900, 1, 1), date.today())}')

    mother_input = context.browser.find_element_by_id('nome_mae')
    mother_input.send_keys('Integra Teste Mãe')

    gender_select = context.browser.find_element_by_id('sexo')
    gender_options = gender_select.find_elements_by_tag_name('option')
    gender_options[random.randint(1, (len(gender_options) - 1))].click()

    email_input = context.browser.find_element_by_id('email')
    email_input.send_keys('suporte02@connect.com.vc')

    telephone_input = context.browser.find_element_by_id('telefone')
    for _ in range(10):
        telephone_input.send_keys(random.randint(0, 9))

    cellphone_input = context.browser.find_element_by_id('celular')
    for _ in range(11):
        cellphone_input.send_keys(random.randint(0, 9))

    address_input = context.browser.find_element_by_id('logradouro')
    address_input.send_keys('Rua das laranjeiras')

    profession_input = context.browser.find_element_by_id('profissao')
    profession_input.send_keys('suporte técnico')

    number_input = context.browser.find_element_by_id('numero')
    number_input.send_keys('789645')

    neighborhood_input = context.browser.find_element_by_id('bairro')
    neighborhood_input.send_keys('Jardim Primavera')

    complement_input = context.browser.find_element_by_id('complemento')
    complement_input.send_keys('Apto 502')

    city_select = context.browser.find_element_by_id('municipio')
    city_options = city_select.find_elements_by_tag_name('option')
    city_options[random_option(city_options)].click()

    cep_input = context.browser.find_element_by_id('cep')
    for _ in range(8):
        num = random.randint(0, 9)
        cep_input.send_keys(f'{num}')


# SAVE THE INPUT VALUE AND CLEAR IT LATER
def save_and_clear(input):
    input_value = input.get_attribute('value')
    input.clear()
    return input_value


# FIND AN INPUT ON THE PAGE AND CLEAR IT
def find_and_clear_input(context, id):
    input = context.browser.find_element_by_id(id)
    input.clear()
    return input


# SEND INFO TO BIRTH DATE FIELD AND CHECK IF INFO IS VALID
def validate_birth_date(context, input):
    birth_date_input = context.browser.find_element_by_id('nascimento')
    value = save_and_clear(birth_date_input)
    birth_date_input.send_keys(f'{input}')
    context.browser.find_element_by_class_name('btn-success').click()
    show_message(context)
    context.browser.find_element_by_class_name('swal2-confirm').click()
    birth_date_input = context.browser.find_element_by_id('nascimento')
    birth_date_input.clear()
    birth_date_input.send_keys(value)


# GENERATES RANDOM INTEGERS ACCORDING TO THE RANGE GIVEN
def random_numbers(web_ele, num_quantity):
    for num in range(num_quantity):
        web_ele.send_keys(f'{random.randint(0, 9)}')


# FIND INPUT BY XPATH OR ID OR CLASS NAME
def find_input(general_context, input):
    try:
        input = general_context.find_element_by_xpath(input)
        return input
    except NoSuchElementException:
        try:
            input = general_context.find_element_by_id(input)
            return input
        except NoSuchElementException:
            try:
                input = general_context.find_element_by_class_name(input)
                return input
            except NoSuchElementException:
                try:
                    input = general_context.find_element_by_name(input)
                    return input
                except NoSuchElementException:
                    try:
                        input = general_context.find_element_by_tag_name(input)
                        return input
                    except NoSuchElementException as e:
                        raise e


# CHECK IF ALL TABS ARE APPEARING ON THE ADMIN PANEL AS THEY ARE SUPPOSED
def check_tabs_qty(context, number):
    body_box = context.browser.find_element_by_class_name('body-box')
    tabs_div = body_box.find_element_by_class_name('g-0')
    tabs_list = tabs_div.find_elements_by_class_name('box-container')
    assert len(tabs_list) == number
