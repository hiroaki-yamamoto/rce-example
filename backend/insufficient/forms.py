#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Forms."""

import django.forms as forms


class CalcForm(forms.Form):
    """Calculator form."""

    a = forms.IntegerField()
    b = forms.IntegerField()
    op = forms.CharField(max_length=1)

    def process(self):
        """Start the calculation."""
        data = self.clean()
        return eval(f"{data['a']}{data['op']}{data['b']}")
