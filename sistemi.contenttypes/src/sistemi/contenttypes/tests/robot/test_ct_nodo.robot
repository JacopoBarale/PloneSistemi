# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s sistemi.contenttypes -t test_nodo.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src sistemi.contenttypes.testing.SISTEMI_CONTENTTYPES_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/sistemi/contenttypes/tests/robot/test_nodo.robot
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

Scenario: As a site administrator I can add a Nodo
  Given a logged-in site administrator
    and an add Nodo form
   When I type 'My Nodo' into the title field
    and I submit the form
   Then a Nodo with the title 'My Nodo' has been created

Scenario: As a site administrator I can view a Nodo
  Given a logged-in site administrator
    and a Nodo 'My Nodo'
   When I go to the Nodo view
   Then I can see the Nodo title 'My Nodo'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Nodo form
  Go To  ${PLONE_URL}/++add++Nodo

a Nodo 'My Nodo'
  Create content  type=Nodo  id=my-nodo  title=My Nodo

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Nodo view
  Go To  ${PLONE_URL}/my-nodo
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Nodo with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Nodo title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
