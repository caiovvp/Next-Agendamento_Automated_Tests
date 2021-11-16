Feature: Create, edit name, working hours, link for a location and delete it

  Scenario: Go to Locations Tab
    Given user is logged in Admin Panel
    When click on </postos-de-vacinacao/>

  Scenario: Create new location
    When click on <btn-primary>
    And type nome: <Local Teste>
    And type localizacao: <https://www.teste.com.br/>
    And type cnes: <1234567>
    And click on <btn-primary>
    Then show message
    """
      {
        "message": "Local de vacinação salvo com sucesso",
        "web_ele": "//*[@id='swal2-html-container']"
      }
    """
    And click on <swal2-confirm>
    And click on </admin/>

  Scenario: Create a location with same name
    When click on </postos-de-vacinacao/>
    And click on <btn-primary>
    And type nome: <Local Teste>
    And type localizacao: <https://www.teste.com.br/>
    And type cnes: <1234567>
    And click on <btn-primary>
    Then show message
    """
      {
        "message": "Já existe um local de vacinação cadastrado com o mesmo nome",
        "web_ele": "//*[@id='swal2-html-container']"
      }
    """
    And click on <swal2-confirm>

  Scenario: Find new location in user panel and check redirected URL
    Given go to locations page: <http://192.168.201.15:88/locais-de-vacinacao>
    When find <Local Teste> [type: <tag>, name: <tr>] in <border-1>
    Then redirect to Local Teste URL: <https://www.teste.com.br/> on window <2>
    And close browser window <2>

  Scenario: Edit name and url of test location
    Given go to locations tab: <http://192.168.201.15:88/postos-de-vacinacao/>
    When find <Local Teste> [type: <class>, name: <btn-warning>] in <table-striped> (FOR LISTS)
    And clear <nome>
    And type nome: <Local Teste Editado>
    And clear <localizacao>
    And type localizacao: <https://www.teste.com.br/teste>
    And click on <btn-primary>
    Then show message
    """
      {
        "message": "Local de vacinação alterado com sucesso",
        "web_ele": "//*[@id='swal2-html-container']"
      }
    """
    And click on <swal2-confirm>

  Scenario: Edit working hours of test location
    Given go to locations tab: <http://192.168.201.15:88/postos-de-vacinacao/>
    When find <Local Teste Editado> [type: <class>, name: <btn-info>] in <table-striped> (FOR LISTS)
    And clear and type <open_1>: <000001>
    And clear and type <close_1>: <235959>
    And click on <btn-primary>
    Then show message
    """
      {
        "message": "Horários salvos com sucesso",
        "web_ele": "//*[@id='swal2-html-container']"
      }
    """
    And click on <swal2-confirm>

  Scenario: Delete edited location
    Given user is logged in Admin Panel
    And go to locations tab: <http://192.168.201.15:88/postos-de-vacinacao/>
    When find <Local Teste Editado> [type: <class>, name: <btn-danger>] in <table-striped> (FOR LISTS)
    Then show message
    """
      {
        "message": "Local de vacinação removido com sucesso",
        "web_ele": "//*[@id='swal2-html-container']"
      }
    """
    And click on <swal2-confirm>
    And log out of Admin Panel

