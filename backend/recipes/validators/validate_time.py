from rest_framework.validators import ValidationError as RFError


def validate_time(value):
    if value < 1:
        raise RFError(['Время не может быть менее минуты.'])
