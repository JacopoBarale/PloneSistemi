# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from sistemi.contenttypes.testing import (
    SISTEMI_CONTENTTYPES_INTEGRATION_TESTING  # noqa,,
)
from zope.component import createObject, queryUtility

import unittest


try:
    from plone.dexterity.schema import portalTypeToSchemaName
except ImportError:
    # Plone < 5
    from plone.dexterity.utils import portalTypeToSchemaName


class SchedaIntegrationTest(unittest.TestCase):

    layer = SISTEMI_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_scheda_schema(self):
        fti = queryUtility(IDexterityFTI, name='Scheda')
        schema = fti.lookupSchema()
        schema_name = portalTypeToSchemaName('Scheda')
        self.assertIn(schema_name.lstrip('plone_0_'), schema.getName())

    def test_ct_scheda_fti(self):
        fti = queryUtility(IDexterityFTI, name='Scheda')
        self.assertTrue(fti)

    def test_ct_scheda_factory(self):
        fti = queryUtility(IDexterityFTI, name='Scheda')
        factory = fti.factory
        obj = createObject(factory)


    def test_ct_scheda_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Scheda',
            id='scheda',
        )


        parent = obj.__parent__
        self.assertIn('scheda', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('scheda', parent.objectIds())

    def test_ct_scheda_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Scheda')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_scheda_filter_content_type_false(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Scheda')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'scheda_id',
            title='Scheda container',
        )
        self.parent = self.portal[parent_id]
        obj = api.content.create(
            container=self.parent,
            type='Document',
            title='My Content',
        )
        self.assertTrue(
            obj,
            u'Cannot add {0} to {1} container!'.format(obj.id, fti.id)
        )
