#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Bad resource tests."""

import json

from urllib.parse import urlencode
from unittest import TestCase

from .views import BadView
from ..utils import UNIQUE_MESSAGE

from ..test_base import EndpointCheckBase, RequestMethodBase

# Create your tests here.


class EndpointDefinition(object):
    """The endpoint definition."""

    view_cls = BadView
    endpoint = "bad"
    page_url = "/bad"
    page_kwargs = {
        'a': 1,
        'b': 1,
        'op': '+'
    }

    def set_page_url(self):
        """Set page url."""
        self.page_url = f"/bad?{urlencode(self.page_kwargs, doseq=True)}"


class BadResEndpointTest(EndpointDefinition, EndpointCheckBase, TestCase):
    """Check whether the bad endpoint exists."""

    pass


class BadResRequestCheck(EndpointDefinition, RequestMethodBase, TestCase):
    """Bad response request check."""

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


class BadReqMoreThan2ValuesTest(BadResRequestCheck):
    """Bad request that has more than 2 values test."""

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
        resp = super(BadResRequestCheck, self).test_method()
        p = json.loads(resp.content.decode('utf-8'))
        self.assertEqual(p, {
            name: [UNIQUE_MESSAGE.format(name=name, size=len(values))]
            for (name, values) in self.page_kwargs.items()
        })


class BadReqRCETest(BadResRequestCheck):
    """Bad request must have Remote Code Execution Vulnerability."""

    def setUp(self):
        """Setup."""
        self.page_kwargs = {
            'a': "[1, 2, 3]",
            'b': "5",
            'op': "*"
        }
        super().setUp()

    def test_method(self):
        """Test method."""
        resp = super(BadResRequestCheck, self).test_method()
        p = json.loads(resp.content.decode('utf-8'))
        self.assertEqual(p, {"result": [1, 2, 3] * 5})
