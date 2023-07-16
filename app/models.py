# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

# from django.template.backends import django
from django.db import models
from django.utils import timezone


class Subscribers(models.Model):
    """Модель подписчиков"""

    email = models.EmailField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    birthday = models.DateField()
    add_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email.encode("utf8")


class Letters(models.Model):
    """Модель шаблонов писем"""

    title = models.CharField(max_length=100, unique=True)
    text = models.TextField()
    subscriber = models.ManyToManyField(
        Subscribers, through="Mailing", related_name="letter"
    )
    add_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title.encode("utf8")


class Mailing(models.Model):
    """Модель рассылки"""

    subscriber = models.ForeignKey(
        Subscribers, on_delete=models.CASCADE, related_name="relation"
    )
    letter = models.ForeignKey(
        Letters, on_delete=models.CASCADE, related_name="relation"
    )
    send_date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    read = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return self.subscriber
