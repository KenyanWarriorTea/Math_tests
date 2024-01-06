from django.db.models import Count

from testsite.settings import EMAIL_HOST_USER
from .models import *
import smtplib
from email.mime.text import MIMEText
from django.core.mail import send_mail


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        ]


class DataMixin:
    paginate_by = 2

    def get_user_context(self, **kwargs):
        context = kwargs

        return context



from django.core.mail import send_mail

def send_email(subject, message, recipient_list):
    send_mail(subject, message, 'asllsackl@gmail.com', recipient_list)
