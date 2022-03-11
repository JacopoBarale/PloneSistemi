# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s sistemi.contenttypes -t test_no_xml.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src sistemi.contenttypes.testing.SISTEMI_CONTENTTYPES_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/sistemi/contenttypes/tests/robot/test_no_xml.robot
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

Scenario: As a site administrator I can add a NoXml
  Given a logged-in site administrator
    and an add NoXml form
   When I type 'My NoXml' into the title field
    and I submit the form
   Then a NoXml with the title 'My NoXml' has been created

Scenario: As a site administrator I can view a NoXml
  Given a logged-in site administrator
    and a NoXml 'My NoXml'
   When I go to the NoXml view
   Then I can see the NoXml title 'My NoXml'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add NoXml form
  Go To  ${PLONE_URL}/++add++NoXml

a NoXml 'My NoXml'
  Create content  type=NoXml  id=my-no_xml  title=My NoXml

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the NoXml view
  Go To  ${PLONE_URL}/my-no_xml
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a NoXml with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the NoXml title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
