import time
from json import loads

from behave import *
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from features.fixtures import find_by_link, find_input, check_tabs_qty


@given('go to {page_name}: <{link}>')
@when('go to {page_name}: <{link}>')
def step_impl(context, page_name, link):
    context.browser.get(link)
    WebDriverWait(context.browser, 5).until(EC.url_to_be(link))


@given('try go to {page_name}: <{link}>')
def step_impl(context, page_name, link):
    context.browser.get(link)


@when('type {input}: <{value}>')
def type_input(context, input, value):
    find_input(context.browser, input).send_keys(value)


@when('type {input}-')
def type_many_values(context, input):
    step_text = loads(context.text)
    for value in step_text['values']:
        clear_input(context, input)
        type_input(context, input, value)
        context.execute_steps(u'''
            When click on <btn-primary>
        ''')
        if input == 'senha' and context.browser.find_element_by_id('swal2-title').text == 'Erro!':
            context.browser.find_element_by_class_name('swal2-confirm').click()


@given('click on <{input}>')
@when('click on <{input}>')
@then('click on <{input}>')
def click_on_btn(context, input):
    try:
        context.browser.find_element_by_xpath(input).click()
    except NoSuchElementException:
        try:
            context.browser.find_element_by_id(input).click()
        except NoSuchElementException:
            try:
                context.browser.find_element_by_class_name(input).click()
            except NoSuchElementException:
                try:
                    link_button = find_by_link(context, input)
                    if link_button is not None:
                        link_button.click()
                except NoSuchElementException as e:
                    raise e


@when('choose item from <{input}>')
def step_impl(context, input):
    list_ele = find_input(context.browser, input)
    click_on_select_items(context, list_ele, input)


def click_on_select_items(context, list_ele, input):
    list_itens = list_ele.find_elements_by_tag_name('option')
    i = 0
    for _ in list_itens:
        item = list_itens[i]
        item.click()
        if i < len(list_itens):
            click_on_btn(context, 'btn-primary')
            if 'agendamentos' in context.browser.current_url:
                show_registrations(context)
                list_ele = find_input(context.browser, input)
                list_itens = list_ele.find_elements_by_tag_name('option')
            i += 1


@when('choose <{item_text}> from <{input}>')
def step_impl(context, item_text, input):
    list_ele = find_input(context.browser, input)
    list_itens = list_ele.find_elements_by_tag_name('option')
    for item in list_itens:
        if item.text == item_text:
            item.click()
            break


@then('redirect to {page_name}: <{link}> on window <{window_handle_number}>')
def step_impl(context, page_name, link, window_handle_number):
    window = context.browser.window_handles[int(window_handle_number) - 1]
    context.browser.switch_to_window(window)
    WebDriverWait(context.browser, 5).until(EC.url_to_be(link))


@then('show registrations of that page')
def show_registrations(context):
    assert EC.visibility_of_element_located((By.TAG_NAME, 'thead'))
    assert EC.visibility_of_element_located((By.TAG_NAME, 'tbody'))


@given('user is logged in Admin Panel')
def login_admin_panel(context):
    try:
        context.browser.find_element_by_class_name('btn-sm')
    except NoSuchElementException:
        # Log in using default user in Admin Panel
        context.execute_steps(u'''
            Given go to Admin Panel: <http://192.168.201.15:88/admin/>
            When type login: <01000417107>
            And type password: <connect_tester>
            And click on <btn-light>
            Then redirect to Admin Panel Dashboard: <http://192.168.201.15:88/admin/dashboard> on window <1>
        ''')


@when('delete <{cpf}> user')
def step_impl(context, cpf):
    td_list = context.browser.find_elements_by_tag_name('td')
    for td in td_list:
        if td.text == cpf:
            td_test = td
    tr_test = td_test.find_element_by_xpath('..')
    tr_test.find_element_by_class_name('btn-danger').click()
    context.browser.find_element_by_id('remove-user-button').click()


@when('repeat test login')
def repeat_test_login(context):
    # Repeat login using user that was deleted
    context.execute_steps(u'''
        Given click on <btn-danger>
        And go to Admin Panel: <http://192.168.201.15:88/admin/>
        When type login: <539.034.990-30>
        And type password: <connect_tester>
        And click on <btn-light>
    ''')


@then('show all Dashboard tabs')
def show_all_tabs(context):
    check_tabs_qty(context, 8)


@when('create new non-admin user')
def create_non_admin_user(context):
    context.execute_steps(u'''
        When click on </usuarios/>
        And click on <btn-primary>
        And type nome: <non-admin user>
        And type cpf: <00826102077>
        And type cns: <012345678912345>
        And type nascimento: <16/01/2000>
        And choose item from <sexo>
        And type email: <non_admin@gmail.com>
        And choose <Inativo> from <admin>
        And type senha: <non_admin123>
        And click on <btn-primary>
        Then show message
        """
          {
            "message": "Usuário salvo com sucesso!",
            "web_ele": "//*[@id='swal2-html-container']"
          }
        """
        And click on <swal2-confirm>
    ''')


@then('log out of Admin Panel')
@when('log out of Admin Panel')
def logout_admin_panel(context):
    context.execute_steps(u'''
        Given click on <btn-danger>
        And go to Admin Panel: <http://192.168.201.15:88/admin/>
    ''')


@when('login with non-admin user')
def create_non_admin_user(context):
    context.execute_steps(u'''
        When type login: <00826102077>
        And type password: <non_admin123>
        And click on <btn-light>
    ''')


@then('show only vaccination tab')
def show_vaccination_tab(context):
    check_tabs_qty(context, 1)


@when('choose a schedule from <{list_name}>')
def choose_schedule(context, list_name):
    try:
        find_input(context.browser, 'table-striped')
    except NoSuchElementException:
        pass
    else:
        registration_table = find_input(context.browser, 'table-striped')
        tbody = registration_table.find_element_by_tag_name(list_name)
        trs = tbody.find_elements_by_tag_name('tr')
        edit_vaccine = trs[0].find_element_by_class_name('btn-info')
        edit_vaccine.click()


@when('choose today as vaccination date')
def choose_date(context):
    date_picker = find_input(context.browser, 'datepicker')
    date_picker.click()
    today_date = find_input(context.browser, 'ui-datepicker-today')
    today_date.click()


@when('choose latest hour of the day')
def choose_time(context):
    find_input(context.browser, 'timepicker').click()
    select_list = find_input(context.browser, 'ui-timepicker-select')
    select_list.click()
    select_itens = select_list.find_elements_by_tag_name('option')
    for item in select_itens:
        if item.text == '23':
            item.click()
    minutes_list = find_input(context.browser, 'ui_tpicker_minute_slider')
    minutes_list.click()
    minutes_itens = minutes_list.find_elements_by_tag_name('option')
    for item in minutes_itens:
        if item.text == '50':
            item.click()


@when('verify <{text}> on <{class_name}>')
def verify_input_on_page(context, text, class_name):
    try:
        run_through_list(context, text, class_name)
    except NoSuchElementException:
        button_list = context.browser.find_elements_by_class_name('btn-danger')
        for button in button_list:
            if button.get_attribute('title') == 'Próxima página' and button_list[0] != button:
                button.click()
                verify_input_on_page(context, text, class_name)
            break


def run_through_list(context, text, class_name):
    status_list = context.browser.find_elements_by_class_name(class_name)
    for status in status_list:
        if status.text == text:
            context.status_tr = status.find_element_by_xpath('..')
            context.btn_info = context.status_tr.find_element_by_class_name('btn-info')
            context.btn_info.click()
            break
    if '/lancamento' not in context.browser.current_url:
        raise NoSuchElementException


@when('<{action}> with <{vaccine}> for filter <{status}>')
def vaccinate_a_person(context, action, vaccine, status):
    try:
        find_input(context.browser, 'table-striped')
        find_input(context.browser, 'brasao-verde')
    except NoSuchElementException:
        pass
    else:
        context.execute_steps(u'''
        When verify <{}> on <brasao-verde>
        '''.format(status))
        if '/lancamento' in context.browser.current_url:
            context.execute_steps(u'''
            When choose <{}> from <vacina>
            And choose item from <lote>
            And choose <{}> from <acao>
            And type cnes_vacinador: <CNES Teste>
            And type nome_vacinador: <Vacinador Teste>
            And click on <btn-primary>
        '''.format(vaccine, action))
        else:
            context.browser.get('http://192.168.201.15:88/vacinacao/')


@when('choose first-dose vaccination for a registration')
def vaccinate_one_dose(context):
    try:
        find_input(context.browser, 'tbody')
    except NoSuchElementException:
        pass
    else:
        context.execute_steps(u'''
            When choose a schedule from <tbody>
            And choose <Connect Group> from <local>
            And choose <Agendar dose 1> from <acao>
            And choose today as vaccination date
            And choose latest hour of the day
            And click on <btn-primary>
        ''')


@when('choose second-dose vaccination for a registration')
def vaccinate_one_dose(context):
    try:
        find_input(context.browser, 'tbody')
    except NoSuchElementException:
        pass
    else:
        context.execute_steps(u'''
            When choose a schedule from <tbody>
            And choose <Connect Group> from <local>
            And choose <Agendar dose 2> from <acao>
            And choose today as vaccination date
            And choose latest hour of the day
            And click on <btn-primary>
        ''')


@when('choose one-dose-only vaccination for a registration')
def vaccinate_one_dose(context):
    try:
        find_input(context.browser, 'tbody')
    except NoSuchElementException:
        pass
    else:
        context.execute_steps(u'''
            When choose a schedule from <tbody>
            And choose <Connect Group> from <local>
            And choose <Agendar dose única> from <acao>
            And choose today as vaccination date
            And choose latest hour of the day
            And click on <btn-primary>
        ''')


@then('check sucess message and confirm it')
def check_message_and_confirm(context):
    try:
        find_input(context.browser, 'swal2-confirm')
    except NoSuchElementException:
        pass
    else:
        context.execute_steps(u'''
            Then show message
            """
              {
                "message": "Agendamento realizado para",
                "web_ele": "//*[@id='swal2-html-container']"
              }
            """
            And click on <swal2-confirm>
            And show registrations of that page
        ''')


@then('check vaccination message: Vacinação lançada com sucesso')
def step_impl(context):
    try:
        find_input(context.browser, 'swal2-confirm')
    except NoSuchElementException:
        pass
    else:
        context.execute_steps(u'''
            Then show message
            """
              {
                "message": "Vacinação lançada com sucesso",
                "web_ele": "//*[@id='swal2-html-container']"
              }
            """
            And click on <swal2-confirm>
        ''')


@then('check vaccination message: Não comparecimento lançado com sucesso')
def step_impl(context):
    try:
        find_input(context.browser, 'swal2-confirm')
    except NoSuchElementException:
        pass
    else:
        context.execute_steps(u'''
            Then show message
            """
              {
                "message": "Não comparecimento lançado com sucesso",
                "web_ele": "//*[@id='swal2-html-container']"
              }
            """
            And click on <swal2-confirm>
        ''')


@when('find <{text}> [type: <{input_type}>, name: <{input_name}>] in <{web_ele}>')
def step_impl(context, text, input_type, input_name, web_ele):
    web_ele = find_input(context.browser, web_ele)
    if input_type == 'tag':
        item_list = web_ele.find_elements_by_tag_name(input_name)
    if input_type == 'class':
        item_list = web_ele.find_elements_by_class_name(input_name)
    for item in item_list:
        if 'btn' in input_name:
            item.click()
            break
        else:
            if item.text == text:
                find_input(item, 'a').click()
                break


@when('find <{text}> [type: <{input_type}>, name: <{input_name}>] in <{web_ele}> (FOR LISTS)')
def step_impl(context, text, input_type, input_name, web_ele):
    web_ele = find_input(context.browser, web_ele)
    trs_list = web_ele.find_elements_by_tag_name('tr')
    for tr in trs_list:
        if text in tr.text:
            correct_tr = tr
    if input_type == 'tag':
        item_list = web_ele.find_elements_by_tag_name(input_name)
    if input_type == 'class':
        item_list = correct_tr.find_elements_by_class_name(input_name)
    for item in item_list:
        if 'btn' in input_name:
            item.click()
        else:
            if item.text == text:
                find_input(item, 'a').click()
                break
            if len(context.browser.window_handles) < 2:
                raise NoSuchElementException


@then('close browser window <{number}>')
def close_window(context, number):
    context.browser.close()
    context.browser.switch_to_window(context.browser.window_handles[(len(number) - 2)])


@when('clear <{input_name}>')
def clear_input(context, input_name):
    find_input(context.browser, input_name).clear()


@then('show registrations and vaccinations of that day')
def step_impl(context):
    WebDriverWait(context.browser, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'table-striped')))


@then('dont show any registrations or vaccinations')
def step_impl(context):
    WebDriverWait(context.browser, 5).until_not(EC.visibility_of_element_located((By.CLASS_NAME, 'table-striped')))


@when('clear and type <{input_name}>: <{value}>')
def step_impl(context, input_name, value):
    input = find_input(context.browser, input_name)
    input.clear()
    input.send_keys(value)


@when('set <{input_id}> value to <{value}>')
def step_impl(context, input_id, value):
    context.browser.execute_script(f"document.getElementById('{input_id}').value = '{value}';")


@then('find <{vaccine_name}> on Vaccination Tab')
def step_impl(context, vaccine_name):
    try:
        find_input(context.browser, 'table-striped')
        find_input(context.browser, 'brasao-verde')
    except NoSuchElementException:
        pass
    else:
        find_input(context.browser, 'btn-info').click()
        if find_vaccine(context, vaccine_name):
            pass
        else:
            raise AssertionError('Vaccine was found but it was not supposed to be found.')


@then('dont find <{vaccine_name}> on Vaccination Tab')
def step_impl(context, vaccine_name):
    try:
        find_input(context.browser, 'table-striped')
        find_input(context.browser, 'brasao-verde')
    except NoSuchElementException:
        pass
    else:
        if not find_vaccine(context.browser, vaccine_name):
            pass
        else:
            raise AssertionError('Vaccine was not found but it was supposed to be found.')


def find_vaccine(context, vaccine_name):
    vaccine_input = find_input(context, 'vacina')
    vaccine_options = vaccine_input.find_elements_by_class_name('option')
    vaccine_found = False
    for vaccine in vaccine_options:
        if vaccine.text == vaccine_name:
            vaccine_found = True
    return vaccine_found


@then('find <{web_ele}> on page')
def find_web_ele(context, web_ele):
    find_input(context.browser, web_ele)

@then('show the sincronization loading')
def show_sync(context):
    WebDriverWait(context.browser, 3).until(EC.visibility_of_element_located((By.ID, 'progress-modal')))
    WebDriverWait(context.browser, 3).until(EC.visibility_of_element_located((By.CLASS_NAME, 'modal-header')))

@given('user log in with cpf <{user_cpf}> and password <{user_password}>')
def step_impl(context, user_cpf, user_password):
    try:
        context.execute_steps(u'''
            Given go to Dashboard Page: <http://192.168.201.15:88/admin/dashboard>
            And click on <btn-danger>
        ''')
    except NoSuchElementException:
        context.execute_steps(u'''
            Given go to Login Page: <http://192.168.201.15:88/admin>
            When clear and type <login>: <()>
            And clear and type <password>: <()>
            And click on <btn-light>
        '''.format(user_cpf, user_password))


@then('show a list of vaccinations that failed synchronization')
def step_impl(context):
    context.browser.find_element_by_id()