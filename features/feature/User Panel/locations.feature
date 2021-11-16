    Feature: Check vaccination locations and see it on Google Maps

      Scenario: Check location for each address
        Given user is on home page
        When go to locations page
        And click on address icon
        Then open google maps page for that address

