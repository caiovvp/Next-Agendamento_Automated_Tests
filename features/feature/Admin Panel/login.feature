Feature: Login into Next Admin Panel

  Background:
    Given go to Admin Panel: <http://192.168.201.15:88/admin/>

    Scenario: CPF not valid
      When type login: <12345678910>
      And type password: <test_pwd>
      And click on <btn-light>
      Then show message
      """
        {
          "message": "CPF inválido",
          "web_ele": "/html/body/div[1]/div/div[2]/div"
        }
      """
      And click on <swal2-confirm>
      
    Scenario: User doesn't exist
      When type login: <461.303.180-06>
      And type password: <connect_tester>
      And click on <btn-light>
      Then show message
      """
        {
          "message": "Login ou senha não encontrado",
          "web_ele": "/html/body/div[1]/div/div[2]/div"
        }
      """
      And click on <swal2-confirm>

    Scenario: Log in Admin Panel
      When type login: <01000417107>
      And type password: <connect_tester>
      And click on <btn-light>
      Then redirect to Admin Panel Dashboard: <http://192.168.201.15:88/admin/dashboard> on window <1>
      And log out of Admin Panel
