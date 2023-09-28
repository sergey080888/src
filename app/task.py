# -*- coding: utf-8 -*-
from datetime import datetime

from django.core.mail import EmailMultiAlternatives
from app.models import Letters, Subscribers, Mailing
from string import Template
from mailganer.settings import EMAIL_HOST_USER
from celery import shared_task


@shared_task
def send_mail_task(email, mailing_id, letter_id):
    letter = Letters.objects.get(id=letter_id)
    subscribers = Subscribers.objects.get(email=email)
    letter_text = letter.text
    title = letter.title
    name = subscribers.name
    surname = subscribers.surname
    birthday = subscribers.birthday
    mailings_text = Template(letter_text).safe_substitute(
        title=title,
        name=name,
        surname=surname,
        birthday=birthday,
        id=str(mailing_id),
    )
    # return HttpResponse(mailings_text)
    msg = EmailMultiAlternatives(
        subject="test", body=mailings_text, from_email=EMAIL_HOST_USER, to=(email),
    )
    msg.attach_alternative(mailings_text, "text/html")
    msg.send()
    Mailing.objects.filter(id=mailing_id).update(sent=True)
    return "Письмо отправлено"


# @shared_task
# def add(x, y):
#     z = x + y
#     print(z)


def send_list():
    """Создает список отправки"""
    mailing_list = list(
        Mailing.objects.filter(
            read=False,
            sent=False,
            send_date__lte=datetime.now(),
        )
    ) + list(Mailing.objects.filter(read=False, sent=False, send_date__isnull=True))

    mailing_ = ""
    mailing_res = [
        {"mailing_id": _.id, "letter_id": _.letter_id, "email": _.subscriber_id}
        for _ in mailing_list
    ]
    for _ in mailing_list:
        mailing_ += str(_.id) + " "
    return mailing_res


@shared_task
def send_mails_task():
    """Отправляет рассылки по списку"""
    count = 0
    if send_list():
        for _ in send_list():
            send_mail_task.delay(**_)
            count += 1

    return count
