# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import sistemi.contenttypes


class SistemiContenttypesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=sistemi.contenttypes)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'sistemi.contenttypes:default')


SISTEMI_CONTENTTYPES_FIXTURE = SistemiContenttypesLayer()


SISTEMI_CONTENTTYPES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(SISTEMI_CONTENTTYPES_FIXTURE,),
    name='SistemiContenttypesLayer:IntegrationTesting',
)


SISTEMI_CONTENTTYPES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(SISTEMI_CONTENTTYPES_FIXTURE,),
    name='SistemiContenttypesLayer:FunctionalTesting',
)


SISTEMI_CONTENTTYPES_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        SISTEMI_CONTENTTYPES_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='SistemiContenttypesLayer:AcceptanceTesting',
)
