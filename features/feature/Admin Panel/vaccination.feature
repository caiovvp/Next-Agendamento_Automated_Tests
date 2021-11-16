Feature: User tries to vaccinate and write details on the system

  Scenario: Go to Vaccination Tab
    Given user is logged in Admin Panel
    And go to Dashboard Page: <http://192.168.201.15:88/admin/dashboard>
    And go to Vaccination Tab: <http://192.168.201.15:88/vacinacao/>

  Scenario: One dose vaccination
    When <vacinar dose única> with <Janssen> for filter <AGENDADO DOSE ÚNICA>
    Then check vaccination message: Vacinação lançada com sucesso

  Scenario: First dose vaccination
    When <vacinar dose 1> with <Astrazeneca> for filter <AGENDADO DOSE 1>
    Then check vaccination message: Vacinação lançada com sucesso

  Scenario: Second dose vaccination
    When <vacinar dose 2> with <Astrazeneca> for filter <AGENDADO DOSE 2>
    Then check vaccination message: Vacinação lançada com sucesso

  Scenario: Person did not come to vaccinate
    When <Não compareceu> with <Janssen> for filter <AGENDADO DOSE 1>
    Then check vaccination message: Não comparecimento lançado com sucesso