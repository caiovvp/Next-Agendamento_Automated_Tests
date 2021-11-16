Feature: User tries to vaccinate and write details on the system

  Scenario: Go to Registrations page
    Given user is logged in Admin Panel
    When click on </agendamentos>
    Then redirect to Search Registrations: <http://192.168.201.15:88/agendamentos/> on window <1>

  Scenario: Search for registration in 'Aguardando' status
    When choose <Aguardando> from <status>
    And click on <btn-primary>
    Then show registrations of that page

  Scenario: Schedule first-dose vaccination for a registration
    When choose first-dose vaccination for a registration
    Then check sucess message and confirm it

  Scenario: Schedule second-dose vaccination for a registration
    When choose second-dose vaccination for a registration
    Then check sucess message and confirm it

  Scenario: Schedule one-dose-only vaccination for a registration
    When choose one-dose-only vaccination for a registration
    Then check sucess message and confirm it

