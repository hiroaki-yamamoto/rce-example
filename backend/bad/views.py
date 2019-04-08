#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Bad view."""

from django.http import JsonResponse
from django.views.generic import View

# Create your views here.


class BadView(View):
    """Bad view."""

    def get(self, req):
        """Bad view."""
        a = req.GET["a"]
        b = req.GET["b"]
        op = req.GET["op"]
        return JsonResponse({"result": eval(f"{a}{op}{b}")})
