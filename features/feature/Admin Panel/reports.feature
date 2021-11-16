Feature: Show information of registrations and vaccinations according to the filters applied and download report

  Scenario: Go to Reports Tab
    Given user is logged in Admin Panel
    When click on </relatorios>
    Then redirect to Reports Tab: <http://192.168.201.15:88/relatorios> on window <1>

  Scenario: Send empty Final and Start Date
    When set <data_inicio> value to < >
    And set <data_fim> value to < >
    And click on <w-100>
    Then show message
    """
      {
        "message": "Data de início não pode ser vazia",
        "web_ele": "//*[@id='swal2-html-container']"
      }
    """
    And click on <swal2-confirm>

  Scenario: Send Inicial Date later than Final Date
    When set <data_inicio> value to <30/08/2021>
    And set <data_fim> value to <20/08/2021>
    And click on <w-100>
    Then show message
    """
      {
        "message": "A data de início deve ser menor que a data final",
        "web_ele": "//*[@id='swal2-html-container']"
      }
    """
    And click on <swal2-confirm>

  Scenario: Set date filters without registrations on that period
    When set <data_inicio> value to <01/08/2020>
    And set <data_fim> value to <01/08/2020>
    And choose <Sim> from <agendamento>
    And click on <w-100>
    Then dont show any registrations or vaccinations

  Scenario: Set date filters with registrations on that period
    When set <data_inicio> value to <01/06/2021>
    And set <data_fim> value to <12/12/2021>
    And choose <Todos> from <agendamento>
    And click on <w-100>
    Then show registrations and vaccinations of that day
    And find <w-25> on page

