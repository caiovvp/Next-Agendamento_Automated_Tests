from behave import *

@when('execute <{number_of_times}> registrations at once')
def step_impl(context, number_of_times):
    for _ in range(0, int(number_of_times)):
        context.execute_steps(u'''
            Given user is on home page
            And go to the registration page
        ''')
        context.execute_steps(u'''
            When fill the form with valid infos
        ''')
        context.execute_steps(u'''
            When send valid-form
            Then form accepted
            """
              {
                "message": "Pré-cadastro foi realizado com sucesso!",
                "web_ele": "/html/body/div/div[2]/div[1]/div/div/div[2]/h3"
              }
            """
        ''')


@when('execute <{number_of_times}> schedules at once')
def step_impl(context, number_of_times):
    for _ in range(0, int(number_of_times)):
        context.execute_steps(u'''
            Given user is logged in Admin Panel
            When click on </agendamentos>
            Then redirect to Search Registrations: <http://192.168.201.15:88/agendamentos/> on window <1>
        ''')
        context.execute_steps(u'''
            When choose <Aguardando> from <status>
            And click on <btn-primary>
            Then show registrations of that page
        ''')
        context.execute_steps(u'''
            When choose first-dose vaccination for a registration
            Then check sucess message and confirm it
        ''')
        context.execute_steps(u'''
            When choose second-dose vaccination for a registration
            Then check sucess message and confirm it
        ''')
        context.execute_steps(u'''
            When choose one-dose-only vaccination for a registration
            Then check sucess message and confirm it
        ''')


@when('execute <{number_of_times}> vaccinations at once')
def step_impl(context, number_of_times):
    for _ in range(0, int(number_of_times)):
        context.execute_steps(u'''
            Given user is logged in Admin Panel
            And go to Dashboard Page: <http://192.168.201.15:88/admin/dashboard>
            When click on </vacinacao/>
            Then redirect to Vaccination Tab: <http://192.168.201.15:88/vacinacao/> on window <1>
        ''')
        context.execute_steps(u'''
            When <vacinar dose única> with <Janssen> for filter <AGENDADO DOSE ÚNICA>
            Then check vaccination message: Vacinação lançada com sucesso
        ''')
        context.execute_steps(u'''
            When <vacinar dose 1> with <Astrazeneca> for filter <AGENDADO DOSE 1>
            Then check vaccination message: Vacinação lançada com sucesso
        ''')
        context.execute_steps(u'''
            When <vacinar dose 2> with <Astrazeneca> for filter <AGENDADO DOSE 2>
            Then check vaccination message: Vacinação lançada com sucesso
        ''')
        context.execute_steps(u'''
            When <Não compareceu> with <Janssen> for filter <AGENDADO DOSE 1>
            Then check vaccination message: Não comparecimento lançado com sucesso
        ''')


@when('execute a complete vaccination routine <{number_of_times}>')
def step_impl(context, number_of_times):
    times = int(number_of_times)
    context.execute_steps(u'''
        When execute <()> registrations at once
        And execute <()> schedules at once
        And execute <()> vaccinations at once
    '''.format((times * 6), (times * 2), times))