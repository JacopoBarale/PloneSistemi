# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s sistemi.contenttypes -t test_scheda.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src sistemi.contenttypes.testing.SISTEMI_CONTENTTYPES_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/sistemi/contenttypes/tests/robot/test_scheda.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Scheda
  Given a logged-in site administrator
    and an add Scheda form
   When I type 'My Scheda' into the title field
    and I submit the form
   Then a Scheda with the title 'My Scheda' has been created

Scenario: As a site administrator I can view a Scheda
  Given a logged-in site administrator
    and a Scheda 'My Scheda'
   When I go to the Scheda view
   Then I can see the Scheda title 'My Scheda'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Scheda form
  Go To  ${PLONE_URL}/++add++Scheda

a Scheda 'My Scheda'
  Create content  type=Scheda  id=my-scheda  title=My Scheda

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Scheda view
  Go To  ${PLONE_URL}/my-scheda
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Scheda with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Scheda title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
