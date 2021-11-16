Feature: Search for a registration using filters

  Scenario: Go to Find Registrations
    Given user is logged in Admin Panel
    When click on </agendamentos>
    Then redirect to Search Registrations: <http://192.168.201.15:88/agendamentos/> on window <1>

  Scenario: Search by CPF
    When type cpf: <22539941702>
    And click on <btn-primary>
    Then show registrations of that page

  Scenario: Search by Group
    When choose item from <id_grupo>
    And click on <btn-primary>
    Then show registrations of that page

  Scenario: Search by Status
    When choose item from <status>
    And click on <btn-primary>
    Then show registrations of that page
