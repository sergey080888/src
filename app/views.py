# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from string import Template

from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from mailganer.settings import EMAIL_HOST_USER
from .forms import SubscribersForm, PatternsForm, MailingForm
from .models import Subscribers, Letters, Mailing
from .task import send_mail_task, send_mails_task


def list_subscribers(request):
    if request.method == "POST":
        form = SubscribersForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            error = "Форма не верна"
    subscribers = Subscribers.objects.order_by("-add_date").all()
    context = {
        "subscribers": subscribers,
    }
    return render(request, "app/subscribers.html", context)


def letters(request):
    error = ""
    if request.method == "POST":
        form = PatternsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("letters")
        else:
            error = "Форма не верна"
    letters = Letters.objects.order_by("-id").all()
    context = {"error": error, "letters": letters}
    return render(request, "app/letters.html", context)


def mailing(request):
    mailings = Mailing.objects.order_by("-id").all()
    context = {"mailings": mailings, "mailingform": MailingForm()}
    return render(request, "app/mailing.html", context)


def send_mails(request):
    """Отправляет рассылки по списку"""
    send_mails_task.delay()
    return HttpResponse(
        '<h1>рассылки разосланы</h1><br><a href="{}">На главную</a>'.format(
            reverse("home")
        )
    )


def make_read(request):
    """Делает отметку о прочтении"""
    id = request.GET.get("id")
    if request.method == "GET" and id:
        try:
            mailing = Mailing.objects.filter(id=id)
        except ValueError:
            return HttpResponse("Необходим целый параметр")
        else:
            if mailing:
                mailing.update(read=True, sent=True)
                resp = "Письмо отмечено прочитанным"
                return HttpResponse(resp)
            else:
                return HttpResponse("Обьект не найден")
    else:
        return HttpResponse("ТОЛЬКО GET ЗАПРОСЫ")


def validate_email(request):
    """Проверка email"""
    if request.method == "POST":
        email = request.POST.get("email", None)
        if not Subscribers.objects.filter(email=email).exists():
            name = request.POST.get("name", None)
            surname = request.POST.get("surname", None)
            birthday = request.POST.get("birthday", None)
            new_subscriber = Subscribers(
                email=email, name=name, surname=surname, birthday=birthday
            )
            new_subscriber.save()
            success = "Подписчик добавлен в базу"
            return HttpResponse(success)
        else:
            return HttpResponse("Такой email уже существует")
    else:
        return HttpResponse("Только для POST запросов")


def validate_mailing(request):
    """Проверка формы создания рассылки"""
    if request.method == "POST":
        subscriber = request.POST.get("subscriber", None)
        letter = request.POST.get("letter", None)
        send_date = request.POST.get("send_date", None)
        if (
            Subscribers.objects.filter(email=subscriber).exists()
            and Letters.objects.filter(id=letter).exists()
        ):
            if not send_date:
                send_date = None
            mailing = Mailing(
                subscriber_id=subscriber, letter_id=letter, send_date=send_date
            )

            mailing.save()
            success = "Рассылка добавлена в базу"
            return HttpResponse(success)
        else:
            return HttpResponse("Такой email или шаблон не существует")
    else:
        return HttpResponse("Только для POST запросов")


def home(request):
    return render(request, "app/base.html")
