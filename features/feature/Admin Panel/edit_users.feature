Feature: Change user permissions and/or profile informations

  Scenario: User is Admin
    Given user is logged in Admin Panel
    Then show all Dashboard tabs

  Scenario: User is not Admin
    When create new non-admin user
    And log out of Admin Panel
    And login with non-admin user
    Then show only vaccination tab

  Scenario: non-admin user tried to access admin-only tabs
    Given try go to Users Tab: <http://192.168.201.15:88/usuarios/>
    Then show message
    """
      {
        "message": "Você não tem acesso a essa categoria",
        "web_ele": "//*[@id='swal2-html-container']"
      }
    """
    And click on <swal2-confirm>
    And log out of Admin Panel

  Scenario: Non-admin user is deleted
    Given user is logged in Admin Panel
    When click on </usuarios/>
    And delete <008.261.020-77> user
    Then show message
    """
      {
        "message": "Usuário removido com sucesso",
        "web_ele": "//*[@id='swal2-html-container']"
      }
    """
    And click on <swal2-confirm>
    And log out of Admin Panel