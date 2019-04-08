#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Base classes for test."""

import json

from django.test import Client, RequestFactory
from django.urls import reverse, resolve


class ViewBase(object):
    """
    View base.

    Para-Required attribute:
        view: The **function** should connect to the endpoint.
        view_cls: The class should connect to the endpoint
            when view is not specified.
    """

    def __init__(self, *args, **kwargs):
        """Setup."""
        self.view = getattr(self, "view", None) or self.view_cls.as_view()
        super().__init__(*args, **kwargs)


class EndpointCheckBase(ViewBase):
    """
    Check url existence and URL association.

    Required attribute:
        endpoint: The endpoint. e.g. home:index
        page_url: The url associated with the endpoint. e.g. /
        view: The **function** should connect to the endpoint.
        view_cls: The class should connect to the endpoint
            when view is not specified.

    optional attribute:
        url_kwargs: Any keyword arguments to be put to reverse function.
        url_args: Any arguments to be put to reverse function.
    """

    def __init__(self, *args, **kwargs):
        """Setup."""
        self.url_kwargs = getattr(self, "url_kwargs", {})
        self.url_args = getattr(self, "url_args", [])

        super().__init__(*args, **kwargs)

    def test_url(self):
        """The URL should be found in the app."""
        self.assertEqual(
            reverse(
                self.endpoint, args=self.url_args, kwargs=self.url_kwargs
            ), self.page_url
        )

    def test_assignment(self):
        """The view should be assigned to URL."""
        self.assertEqual(
            resolve(self.page_url).func.__name__, self.view.__name__
        )


class HTTPClientBase(object):
    """
    HTTP client class.

    Required attribute:
        page_url: The url associated with the endpoint. e.g. /
    """

    def __init__(self, *args, **kwargs):
        """Setup."""
        self.client = Client()
        self.cli_kwargs = getattr(self, "cli_kwargs", None) or {}
        self.method = getattr(self, "method", None) or "get"
        self.__payload = {}
        super().__init__(*args, **kwargs)

    @property
    def request(self):
        """Make a raw request from RequestFactory."""
        return getattr(RequestFactory(), self.method.lower())(
            self.page_url, **self.cli_kwargs
        )

    def set_client_kwargs(self, **kwargs):
        """Set Client args."""
        self.cli_kwargs.update(kwargs)

    @property
    def payload(self):
        """Return payload."""
        return self.__payload

    @payload.setter
    def payload(self, value):
        """Set payload."""
        self.__payload = value
        self.refresh_payload()

    def refresh_payload(self):
        """
        Refresh payload.

        This function is an alias of
        self.set_client_kwargs(
            data=json.dumps(self.payload), content_type='application/json'
        ).
        """
        self.set_client_kwargs(
            data=json.dumps(self.payload),
            content_type="application/json"
        )

    def make_call(self):
        """Push a request the the view and return the resp from the view."""
        return getattr(self.client, self.method.lower())(
            self.page_url, **self.cli_kwargs
        )


class RequestMethodBase(ViewBase, HTTPClientBase):
    """
    URL assignment test base.

    Optional attribute:
        status_code: Expected Status Code. 200 by default.
        content_type: If this attribute is set, the test will check the
            payload type of the response when the status_code is 200
    """

    status_code = 200

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)

    def test_method(self):
        """The view should return the value of status_code."""
        ret = self.make_call()
        content_type = getattr(self, "content_type", None)
        self.assertEqual(
            ret.status_code, self.status_code,
            f"Code: {ret.status_code}, "
            f'Content: {ret.content or getattr(ret, "url", "")}'
        )
        if content_type and ret.status_code == 200:
            self.assertTrue(
                ret["content-type"].startswith(content_type),
                f'{ret["content-type"]} not start with {content_type}'
            )
        return ret
