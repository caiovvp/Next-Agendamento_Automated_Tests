Feature: Make a registration

  Scenario: Go to registration page
    Given user is on home page
    And go to the registration page
    When fill the form with valid infos

  Scenario: Any required information is left blank
    When required information is blank
    Then form not accepted

  Scenario: CPF is incorrectly filled
    When cpf is not valid
    """
      {
        "message": "CPF inválido",
        "web_ele": "//*[@id='swal2-html-container']"
      }
    """
    Then form not accepted

# Either less numbers than necessary or date is later than today
  Scenario: Birth Date incorrectly filled
    When birth date is not valid
    """
      {
        "message": "Data de nascimento inválida",
        "web_ele": "//*[@id='swal2-html-container']"
      }
    """
    When birth date is incomplete
    """
      {
        "message": "Data de nascimento vazia ou inválida.",
        "web_ele": "//*[@id='swal2-html-container']"
      }
    """
    Then form not accepted

  Scenario: Email is incorrectly filled
    When email without @
    Then form not accepted
    When email without .com
    Then form not accepted

  Scenario: Fill all informations correctly
    When send valid-form
    Then form accepted
    """
      {
        "message": "Pré-cadastro foi realizado com sucesso!",
        "web_ele": "/html/body/div/div[2]/div[1]/div/div/div[2]/h3"
      }
    """
