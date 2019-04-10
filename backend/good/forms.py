#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Forms."""

from django.core.exceptions import ValidationError
import django.forms as forms
from django.utils.translation import ugettext as _
from ..insufficient.forms import CalcForm as InsufCalcForm


class CalcForm(InsufCalcForm):
    """Calculation form that inherits InsufCalcForm."""

    op = forms.ChoiceField(choices=(
        ("+", "ADD"), ("-", 'SUB'),
        ("*", "MUL"), ("/", "DIV"),
    ))

    error_messages = {
        'zero': _("The value can't be divided by 0.")
    }

    operations = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a / b,
    }

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)

        def validate_ob_b(value):
            """Validate B-operand to avoid 0-division error."""
            if self.data["op"] == "/" and value == 0:
                raise ValidationError(
                    self.error_messages["zero"], code='zero'
                )

        self.fields["b"].validators.append(validate_ob_b)

    def process(self):
        """Process the operation."""
        data = self.clean()
        return self.operations[data['op']](data['a'], data['b'])
