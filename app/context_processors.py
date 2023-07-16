from .forms import SubscribersForm, PatternsForm, MailingForm


def subscribersform(request):
    return {
        "subscribersform": SubscribersForm(),
        "patternsform": PatternsForm(),
        "mailingform": MailingForm(),
    }
