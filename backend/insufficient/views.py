#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Insufficient Resource."""

# Create your views here.

from django.http import JsonResponse
from django.views.generic import View
from .forms import CalcForm


class InsufView(View):
    """Insufficient view."""

    def get(self, req):
        """Get handler."""
        form = CalcForm(data=req.GET)
        if form.is_valid():
            return JsonResponse({"result": form.process()})
        return JsonResponse(form.errors)
