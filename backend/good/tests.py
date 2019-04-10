#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Good resource tests."""

import json

from urllib.parse import urlencode
from unittest import TestCase

import django.forms as forms

from .views import GoodView
from .forms import CalcForm
from ..utils import UNIQUE_MESSAGE

from ..test_base import EndpointCheckBase, RequestMethodBase

# Create your tests here.


class EndpointDefinition(object):
    """The endpoint definition."""

    view_cls = GoodView
    endpoint = "good"
    page_url = "/good"
    page_kwargs = {
        'a': 1,
        'b': 1,
        'op': '+'
    }

    def set_page_url(self):
        """Set page url."""
        self.page_url = f"/good?{urlencode(self.page_kwargs, doseq=True)}"


class GoodResEndpointTest(EndpointDefinition, EndpointCheckBase, TestCase):
    """Check whether the Good endpoint exists."""

    pass


class GoodResRequestTest(EndpointDefinition, RequestMethodBase, TestCase):
    """Good response request check."""

    def setUp(self):
        """Setup."""
        self.set_page_url()
        super().setUp()

    def test_method(self):
        """Test the method."""
        for op, res in [('+', 2), ('-', 0), ('*', 1), ('/', 1)]:
            with self.subTest(f'(op) = {op}'):
                self.page_kwargs["op"] = op
                self.set_page_url()
                resp = super().test_method()
                p = json.loads(resp.content.decode('utf-8'))
                self.assertEqual(p, {'result': res})
        return resp


class GoodReqMoreThan2ValuesTest(GoodResRequestTest):
    """Good request that has more than 2 values test."""

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
        resp = super(GoodResRequestTest, self).test_method()
        p = json.loads(resp.content.decode('utf-8'))
        self.assertEqual(p, {
            name: [UNIQUE_MESSAGE.format(name=name, size=len(values))]
            for (name, values) in self.page_kwargs.items()
        })


class GoodReqInvalidPayloadTest(GoodResRequestTest):
    """Good request that has more than 2 values test."""

    status_code = 417

    def setUp(self):
        """Setup."""
        self.page_kwargs = {
            'a': "'test+'",
            'b': "'test2'",
            'op': '+',
        }
        super().setUp()

    def test_method(self):
        """Test method."""
        resp = super(GoodResRequestTest, self).test_method()
        p = json.loads(resp.content.decode('utf-8'))
        self.assertEqual(p, {
            "a": [forms.IntegerField.default_error_messages['invalid']],
            "b": [forms.IntegerField.default_error_messages['invalid']],
        })


class GoodReqZeroDivErrorTest(GoodResRequestTest):
    """Zero-division error check."""

    status_code = 417

    def setUp(self):
        """Setup."""
        self.page_kwargs = {
            'a': "100",
            'b': "0",
            'op': '/',
        }
        super().setUp()

    def test_method(self):
        """Test method."""
        resp = super(GoodResRequestTest, self).test_method()
        p = json.loads(resp.content.decode('utf-8'))
        self.assertEqual(p, {
            "b": [CalcForm.error_messages["zero"]]
        })


class GoodReqRCETest(GoodResRequestTest):
    """Good request must have Remote Code Execution Vulnerability."""

    # Plus, op not listed case check.

    status_code = 417

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
        resp = super(GoodResRequestTest, self).test_method()
        p = json.loads(resp.content.decode('utf-8'))
        self.assertEqual(p, {
            "op": [
                forms.ChoiceField.default_error_messages['invalid_choice'] % {
                    "value": self.page_kwargs['op']
                }
            ]
        })
