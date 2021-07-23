from django.conf import settings
from django.contrib import messages
import requests
from django.template.loader import render_to_string
from django.core.signing import Signer
from datetime import datetime
from os.path import splitext
from organization.settings import ALLOWED_HOSTS
from django.apps import apps
from functools import wraps


signer = Signer()


def send_activation_notification(user):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'
    context = {'user': user, 'host': host, 'sign': signer.sign(user.username)}
    subject = render_to_string('email/activation_letter_subject.txt', context)
    body_text = render_to_string('email/activation_letter_body.txt', context)
    user.email_user(subject, body_text)


def set_hours(event):
    Volunteer = apps.get_model('main', 'Volunteer')
    for v in event.volunteers.all():
        vol = Volunteer.objects.get(username=v.username)
        vol.hours += event.hours
        vol.save()


def check_recaptcha(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        request.recaptcha_is_valid = None
        if request.method == 'POST':
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if result['success']:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False
                messages.error(request, 'Invalid reCAPTCHA. Пожалуйста, попробуйте ещё раз.')
        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def get_timestamp_path(instance, filename):
    return '%s%s' % (datetime.now().timestamp(), splitext(filename)[1])
