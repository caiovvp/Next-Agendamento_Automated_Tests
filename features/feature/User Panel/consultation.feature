    Feature: Check for status of a registration

      Scenario: Invalid CPF
        Given user is on home page
        When go to consultation page
        And type invalid CPF
        And send request
        Then show message
        """
          {
            "message": "CPF inválido",
            "web_ele": "//*[@id='swal2-html-container']"
          }
        """
        And close message box

      Scenario: Registration hasn't been done yet
        When type not registered CPF
        And send request
        Then show message
        """
          {
            "message": "CPF não encontrado",
            "web_ele": "//*[@id='swal2-html-container']"
          }
        """
        And close message box

      Scenario: Registration has been done
        When type registered CPF on upper input
        And click on search button
        Then show registration stats




