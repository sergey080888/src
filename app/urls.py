from django.conf.urls import url

from app.views import (
    list_subscribers,
    letters,
    mailing,
    send_mails,
    validate_email,
    validate_mailing,
    home,
    make_read,
)

urlpatterns = [
    url(r"^make_read", make_read, name="make_read"),
    url(r"^subscribers", list_subscribers, name="subscribers"),
    url(r"^letters", letters, name="letters"),
    url(r"^mailing", mailing, name="mailing"),
    url(r"^send_mails", send_mails, name="send_mails"),
    url(r"^validate_email", validate_email, name="validate_email"),
    url(r"^validate_mailing", validate_mailing, name="validate_mailing"),
    url(r"", home, name="home"),
]
