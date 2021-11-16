Feature: Send all the data from the registrations and vaccinations to SI-PNI

  Background:
    Given user is logged in Admin Panel

    Scenario: Synchronization successfully done
      When run script to vaccinate someone
      And go to Dashboard Page: <http://192.168.201.15:88/admin/dashboard>
      And click on </vacinacao/sincronizacao-pni>
      Then show the sincronization loading
      And show message
      """
        {
          "message": "A sincronização foi feita com sucesso",
          "web_ele": "//*[@id='swal2-html-container']"
        }
      """

    Scenario: Synchronization is up to date
      Then show message
      """
        {
          "message": "Não há vacinações a serem sincronizadas",
          "web_ele": "//*[@id='swal2-html-container']"
        }
      """


    Scenario: Synchronization failed
      Given user log in with cpf <00000000000> and password <senhas@123>
      Then show message
        """
          {
            "message": "Alguns registros não foram sincronizados",
            "web_ele": "//*[@id='swal2-html-container']"
          }
        """
      And show a list of vaccinations that failed synchronization


