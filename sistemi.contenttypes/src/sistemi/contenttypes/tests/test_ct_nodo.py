# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from sistemi.contenttypes.testing import (
    SISTEMI_CONTENTTYPES_INTEGRATION_TESTING  # noqa,,,
)
from zope.component import createObject, queryUtility

import unittest


try:
    from plone.dexterity.schema import portalTypeToSchemaName
except ImportError:
    # Plone < 5
    from plone.dexterity.utils import portalTypeToSchemaName


class NodoIntegrationTest(unittest.TestCase):

    layer = SISTEMI_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_nodo_schema(self):
        fti = queryUtility(IDexterityFTI, name='Nodo')
        schema = fti.lookupSchema()
        schema_name = portalTypeToSchemaName('Nodo')
        self.assertIn(schema_name.lstrip('plone_0_'), schema.getName())

    def test_ct_nodo_fti(self):
        fti = queryUtility(IDexterityFTI, name='Nodo')
        self.assertTrue(fti)

    def test_ct_nodo_factory(self):
        fti = queryUtility(IDexterityFTI, name='Nodo')
        factory = fti.factory
        obj = createObject(factory)


    def test_ct_nodo_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Nodo',
            id='nodo',
        )


        parent = obj.__parent__
        self.assertIn('nodo', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('nodo', parent.objectIds())

    def test_ct_nodo_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Nodo')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )
