#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Utils."""

from functools import wraps

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDict
from django.utils.translation import ugettext as _

UNIQUE_MESSAGE = _(
    '{name} must not have more than 1 value, however it has {size}'
)


def check_query_unique(dct: MultiValueDict):
    """
    Check whether the query doesn't have more than 1 values.

    Params:
        dct: the Multi-Value Dict.

    Returns:
        Nothing when there's no error, raises ValidationError on error.

    """
    ret = {}
    for (name, value) in dct.lists():
        if len(value) > 1:
            ret.setdefault(name, [])
            ret[name].append(ValidationError(
                UNIQUE_MESSAGE.format(name=name, size=len(value)),
                code='invalid'
            ))
    if ret:
        raise ValidationError(ret)


def require_query_uniqueness(func):
    """Require query uniqueness."""
    @wraps(func)
    def inside(req, *args, **kwargs):
        """Inside the wrapper."""
        try:
            check_query_unique(req.GET)
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=417)
        return func(req)
    return inside
