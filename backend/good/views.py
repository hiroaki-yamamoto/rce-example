#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Good views."""

from django.http import JsonResponse
from django.views.generic import View

from .forms import CalcForm

# Create your views here.


class GoodView(View):
    """Good view."""

    def get(self, req):
        """Get handler."""
        form = CalcForm(data=req.GET)
        if form.is_valid():
            return JsonResponse({"result": form.process()})
        return JsonResponse(form.errors, status=417)
