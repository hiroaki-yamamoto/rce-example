#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Insuf resource tests."""

import json

from urllib.parse import urlencode
from unittest import TestCase

from .views import InsufView
from ..utils import UNIQUE_MESSAGE

from ..test_base import EndpointCheckBase, RequestMethodBase

# Create your tests here.


class EndpointDefinition(object):
    """The endpoint definition."""

    view_cls = InsufView
    endpoint = "insuf"
    page_url = "/insuf"
    page_kwargs = {
        'a': 1,
        'b': 1,
        'op': '+'
    }

    def set_page_url(self):
        """Set page url."""
        self.page_url = f"/insuf?{urlencode(self.page_kwargs, doseq=True)}"


class InsufResEndpointTest(EndpointDefinition, EndpointCheckBase, TestCase):
    """Check whether the insuf endpoint exists."""

    pass


class InsufResRequestCheck(EndpointDefinition, RequestMethodBase, TestCase):
    """Insuf response request check."""

    def setUp(self):
        """Setup."""
        self.set_page_url()
        super().setUp()

    def test_method(self):
        """Test the method."""
        resp = super().test_method()
        p = json.loads(resp.content.decode('utf-8'))
        self.assertEqual(p, {'result': 2})
        return resp


class InsufReqMoreThan2ValuesTest(InsufResRequestCheck):
    """Insuf request that has more than 2 values test."""

    status_code = 417

    def setUp(self):
        """Setup."""
        self.page_kwargs = {
            'a': [1, 2],
            'b': [1, 2],
            'op': ['+', '-'],
        }
        super().setUp()

    def test_method(self):
        """Test method."""
        resp = super(InsufResRequestCheck, self).test_method()
        p = json.loads(resp.content.decode('utf-8'))
        self.assertEqual(p, {
            name: [UNIQUE_MESSAGE.format(name=name, size=len(values))]
            for (name, values) in self.page_kwargs.items()
        })


class InsufReqRCETest(InsufResRequestCheck):
    """Insuf request must have Remote Code Execution Vulnerability."""

    def setUp(self):
        """Setup."""
        self.page_kwargs = {
            'a': "0",
            'b': "100",
            'op': "x"  # This operator 'x' is inacceptable.
            # But in python, this operation represents a number 0x100 in hex.
            # It means it still has a RCE Vulnerability.
        }
        super().setUp()

    def test_method(self):
        """Test method."""
        resp = super(InsufResRequestCheck, self).test_method()
        p = json.loads(resp.content.decode('utf-8'))
        self.assertEqual(p, {"result": 0x100})
