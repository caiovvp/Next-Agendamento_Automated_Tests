Feature: Add and delete users in Admin Panel

  Scenario: Add 'test' user
    Given user is logged in Admin Panel
    When click on </usuarios/>
    And click on <btn-primary>
    And type nome-
    """
      {
        "values": ["test", "Connect Tester"]
      }
    """
    And type cpf-
    """
      {
        "values": ["0123456789", "123.abc.678-99", "539.034.990-30"]
      }
    """
    And type cns: <012345678912345>
    And type nascimento-
    """
      {
        "values": ["19/07/2287", "16/02/2001"]
      }
    """
    And choose item from <sexo>
    And type email-
    """
      {
        "values": ["caioconnect.com.vc", "caio@connect", "connect_tester@connect.com.vc"]
      }
    """
    And type senha-
    """
      {
        "values": ["test", "connect_tester"]
      }
    """
    Then show message
    """
      {
        "message": "Usuário salvo com sucesso!",
        "web_ele": "//*[@id='swal2-html-container']"
      }
    """
    And click on <swal2-confirm>

  Scenario: Log in with 'test' user
    Given click on <btn-danger>
    And go to Admin Panel: <http://192.168.201.15:88/admin/>
    When type login: <539.034.990-30>
    And type password: <connect_tester>
    And click on <btn-light>
    Then redirect to Admin Panel Dashboard: <http://192.168.201.15:88/admin/dashboard> on window <1>

  Scenario: Delete 'test' user
    When click on </usuarios/>
    And delete <539.034.990-30> user
    Then show message
    """
      {
        "message": "Usuário removido com sucesso",
        "web_ele": "//*[@id='swal2-html-container']"
      }
    """
    And click on <swal2-confirm>

    Scenario: Log in with 'test' user
      When repeat test login
      Then show message
      """
      {
        "message": "Login ou senha não encontrado",
        "web_ele": "//*[@id='swal2-html-container']"
      }
      """

