# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from sistemi.contenttypes.content.no_xml import INoXml  # NOQA E501
from sistemi.contenttypes.testing import (
    SISTEMI_CONTENTTYPES_INTEGRATION_TESTING  # noqa,
)
from zope.component import createObject, queryUtility

import unittest


class NoXmlIntegrationTest(unittest.TestCase):

    layer = SISTEMI_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_no_xml_schema(self):
        fti = queryUtility(IDexterityFTI, name='NoXml')
        schema = fti.lookupSchema()
        self.assertEqual(INoXml, schema)

    def test_ct_no_xml_fti(self):
        fti = queryUtility(IDexterityFTI, name='NoXml')
        self.assertTrue(fti)

    def test_ct_no_xml_factory(self):
        fti = queryUtility(IDexterityFTI, name='NoXml')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            INoXml.providedBy(obj),
            u'INoXml not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_no_xml_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='NoXml',
            id='no_xml',
        )

        self.assertTrue(
            INoXml.providedBy(obj),
            u'INoXml not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('no_xml', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('no_xml', parent.objectIds())

    def test_ct_no_xml_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='NoXml')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_no_xml_filter_content_type_false(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='NoXml')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'no_xml_id',
            title='NoXml container',
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
