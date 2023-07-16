# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Subscribers, Letters, Mailing


class MailingInline(admin.TabularInline):
    model = Mailing
    extra = 3


@admin.register(Subscribers)
class SubscribersAdmin(admin.ModelAdmin):
    list_display = ["email", "name", "surname", "birthday", "add_date"]


@admin.register(Letters)
class LettersAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "text", "add_date"]
    inlines = [
        MailingInline,
    ]
