# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.forms import (
    ModelForm,
    TextInput,
    EmailInput,
    DateInput,
    Textarea,
    NumberInput,
    DateTimeInput,
    CheckboxInput,
)
from .models import Subscribers, Letters, Mailing


class SubscribersForm(ModelForm):
    class Meta:
        model = Subscribers
        fields = ("email", "name", "surname", "birthday")
        widgets = {
            "email": EmailInput(
                attrs={"class": "form-control", "id": "email", "placeholder": "email"}
            ),
            "name": TextInput(
                attrs={"class": "form-control", "id": "name", "placeholder": "Имя"}
            ),
            "surname": TextInput(
                attrs={
                    "class": "form-control",
                    "id": "surname",
                    "placeholder": "Фамилия",
                }
            ),
            "birthday": DateInput(
                attrs={
                    "class": "form-control",
                    "id": "birthday",
                    "placeholder": "День рождения YYYY-MM-DD",
                }
            ),
        }


class PatternsForm(ModelForm):
    class Meta:
        model = Letters
        fields = ("title", "text")
        widgets = {
            "title": TextInput(attrs={"class": "form-control", "placeholder": "name"}),
            "text": Textarea(attrs={"class": "form-control", "placeholder": "text"}),
        }


class MailingForm(ModelForm):
    class Meta:
        model = Mailing
        fields = ("subscriber", "letter", "send_date", "read")
        widgets = {
            "subscriber": EmailInput(
                attrs={
                    "class": "form-control",
                    "id": "subscriber",
                    "placeholder": "email",
                }
            ),
            "letter": NumberInput(
                attrs={
                    "class": "form-control",
                    "id": "letter",
                    "placeholder": "pattern_number",
                }
            ),
            "send_date": DateTimeInput(
                attrs={
                    "class": "form-control",
                    "required": False,
                    "id": "send_date",
                    "placeholder": "YYYY-MM-DD HH:MM:SS",
                }
            ),
        }
