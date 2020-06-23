from django.apps import AppConfig
from django.contrib.auth.models import User

User.USERNAME_FIELD = 'email'


class TransformtoldConfig(AppConfig):
    name = 'transformToLD'
