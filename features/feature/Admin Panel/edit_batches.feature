Feature: Create, Edit, Inactivate and Delete vaccines as well as their respective batches

  Scenario: Go to Vaccines Tab
    Given user is logged in Admin Panel
    When click on </vacinas>

  Scenario: Create new vaccine
    When click on <btn-primary>
    And type codigo_vacina: <123teste>
    And type nome_vacina: <Vacina Teste>
    And click on <btn-primary>
    Then show message
    """
      {
        "message": "Vacina salva com sucesso",
        "web_ele": "//*[@id='swal2-html-container']"
      }
    """
    And click on <swal2-confirm>

    Scenario: Create other vaccine with same name
      When click on <btn-primary>
      And type codigo_vacina: <456teste>
      And type nome_vacina: <Vacina Teste>
      And click on <btn-primary>
      Then show message
      """
        {
          "message": "Já existe outra vacina cadastrada com esse nome",
          "web_ele": "//*[@id='swal2-html-container']"
        }
      """
      And click on <swal2-confirm>

    Scenario: Create other vaccine with same code
      When type codigo_vacina: <123teste>
      And type nome_vacina: <Vacina Nome Diferente>
      And click on <btn-primary>
      Then show message
      """
        {
          "message": "Já existe outra vacina cadastrada com esse código",
          "web_ele": "//*[@id='swal2-html-container']"
        }
      """
      And click on <swal2-confirm>

    Scenario: Edit test vaccine code and name
      Given go to Vaccines Tab: <http://192.168.201.15:88/vacinas/>
      When find <Vacina Teste> [type: <class>, name: <btn-warning>] in <table-striped> (FOR LISTS)
      And clear and type <codigo_vacina>: <123456>
      And clear and type <nome_vacina>: <Teste>
      And click on <btn-primary>
      Then show message
      """
        {
          "message": "Vacina salva com sucesso",
          "web_ele": "//*[@id='swal2-html-container']"
        }
      """
      And click on <swal2-confirm>

    Scenario: Look for vaccine without batches
      Given go to Vaccination Tab: <http://192.168.201.15:88/vacinacao/>
      When click on <btn-primary>
      Then show registrations of that page
      And dont find <Teste> on Vaccination Tab

    Scenario: Try to create Batch with negative doses or more used doses than total doses
      Given go to Vaccines Tab: <http://192.168.201.15:88/vacinas/>
      When find <Teste> [type: <class>, name: <btn-info>] in <table-striped> (FOR LISTS)
      And click on <btn-primary>
      And type lote: <teste>
      And type produtor: <teste>
      And clear and type <doses>: <-50>
      And clear and type <doses_aplicadas>: <0>
      And click on <btn-primary>
      Then show message
      """
        {
          "message": "Doses deve conter um valor inteiro válido e maior que 0",
          "web_ele": "//*[@id='swal2-html-container']"
        }
      """
      When click on <swal2-confirm>
      And type lote: <teste>
      And type produtor: <teste>
      And clear and type <doses>: <50>
      And clear and type <doses_aplicadas>: <100>
      And click on <btn-primary>
      Then show message
      """
        {
          "message": "Doses aplicadas deve ser menor ou igual a quantidade de doses",
          "web_ele": "//*[@id='swal2-html-container']"
        }
      """
      And click on <swal2-confirm>

    Scenario: Create Empty Batch for test vaccine
      Given go to Vaccines Tab: <http://192.168.201.15:88/vacinas/>
      When find <Teste> [type: <class>, name: <btn-info>] in <table-striped> (FOR LISTS)
      And click on <btn-primary>
      And type lote: <teste>
      And type produtor: <teste>
      And click on <btn-primary>
      Then show message
      """
        {
          "message": "Lote da vacina salvo com sucesso",
          "web_ele": "//*[@id='swal2-html-container']"
        }
      """
      And click on <swal2-confirm>

    Scenario: Look for vaccine with empty batch
      Given go to Vaccination Tab: <http://192.168.201.15:88/vacinacao/>
      When click on <btn-primary>
      Then show registrations of that page
      And dont find <Teste> on Vaccination Tab

    Scenario: Add doses to empty batch
      Given go to Vaccines Tab: <http://192.168.201.15:88/vacinas/>
      When find <Teste> [type: <class>, name: <btn-info>] in <table-striped> (FOR LISTS)
      And find <teste> [type: <class>, name: <btn-warning>] in <table-striped> (FOR LISTS)
      And clear and type <doses>: <100>
      And click on <btn-primary>
      Then show message
      """
        {
          "message": "Lote da vacina salvo com sucesso",
          "web_ele": "//*[@id='swal2-html-container']"
        }
      """
      And click on <swal2-confirm>

    Scenario: Look for vaccine with valid batch
      Given go to Vaccination Tab: <http://192.168.201.15:88/vacinacao/>
      When click on <btn-primary>
      Then show registrations of that page
      And find <Teste> on Vaccination Tab

    Scenario: Inactivate valid batch for test vaccine
      Given go to Vaccines Tab: <http://192.168.201.15:88/vacinas/>
      When find <Teste> [type: <class>, name: <btn-info>] in <table-striped> (FOR LISTS)
      And click on <btn-primary>
      And type lote: <teste>
      And type produtor: <teste>

    Scenario: Look for vaccine with inactive valid batch
      Given go to Vaccination Tab: <http://192.168.201.15:88/vacinacao/>
      When click on <btn-primary>
      Then show registrations of that page
      And dont find <Teste> on Vaccination Tab

    Scenario: Add doses to empty batch
      Given go to Vaccines Tab: <http://192.168.201.15:88/vacinas/>
      When find <Teste> [type: <class>, name: <btn-info>] in <table-striped> (FOR LISTS)
      And find <teste> [type: <class>, name: <btn-warning>] in <table-striped> (FOR LISTS)
      And choose <Inativo> from <status>
      And click on <btn-primary>
      Then show message
      """
        {
          "message": "Lote da vacina salvo com sucesso",
          "web_ele": "//*[@id='swal2-html-container']"
        }
      """
      And click on <swal2-confirm>

    Scenario: Look for vaccine with inactive valid batch
      Given go to Vaccination Tab: <http://192.168.201.15:88/vacinacao/>
      When click on <btn-primary>
      Then show registrations of that page
      And find <Teste> on Vaccination Tab

    Scenario: Try to delete Batch that has already been used
      Given go to Vaccines Tab: <http://192.168.201.15:88/vacinas/>
      When find <Astrazeneca> [type: <class>, name: <btn-info>] in <table-striped> (FOR LISTS)
      And find <0001> [type: <class>, name: <btn-danger>] in <table-striped> (FOR LISTS)
      Then show message
      """
        {
          "message": "Existem vacinações realizadas com esse lote",
          "web_ele": "//*[@id='swal2-html-container']"
        }
      """
      And click on <swal2-confirm>

    Scenario: Delete Test Batch
      Given go to Vaccines Tab: <http://192.168.201.15:88/vacinas/>
      When find <Teste> [type: <class>, name: <btn-info>] in <table-striped> (FOR LISTS)
      And find <teste> [type: <class>, name: <btn-danger>] in <table-striped> (FOR LISTS)
      Then show message
      """
        {
          "message": "Lote da vacina removido com sucesso",
          "web_ele": "//*[@id='swal2-html-container']"
        }
      """
      And click on <swal2-confirm>

    Scenario: Try to delete Vaccine that has already been used
      Given go to Vaccines Tab: <http://192.168.201.15:88/vacinas/>
      When find <Astrazeneca> [type: <class>, name: <btn-danger>] in <table-striped> (FOR LISTS)
      And click on <remove-vaccine-button>
      Then show message
      """
        {
          "message": "Vacina não pode ser removida pois existem lotes relacionados a ela.",
          "web_ele": "//*[@id='swal2-html-container']"
        }
      """
      And click on <swal2-confirm>

    Scenario: Delete Test Vaccine
      Given go to Vaccines Tab: <http://192.168.201.15:88/vacinas/>
      When find <Teste> [type: <class>, name: <btn-danger>] in <table-striped> (FOR LISTS)
      And click on <remove-vaccine-button>
      Then show message
      """
        {
          "message": "Vacina removida com sucesso",
          "web_ele": "//*[@id='swal2-html-container']"
        }
      """
      And click on <swal2-confirm>
