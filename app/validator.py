from datetime import datetime
from email_validator import validate_email, EmailNotValidError
from typing import Literal


ValidatedStr = Literal["date", "phone", "email", "text"]


def add_type(type_: ValidatedStr):
    def decorator(func):
        def wrap(*args, **kwargs):
            d = func(*args, **kwargs)
            return d, type_
        return wrap
    return decorator


class Validator:
    """ Class for fields validation """
    def __init__(self):
        self._validation_ordered_functions = [
            self._validate_date,
            self._validate_phone_ru,
            self._validate_email
        ]
        self.last_validated_field = None

    def validate(self, field_value: str) -> ValidatedStr:

        for func in self._validation_ordered_functions:
            validation_successful, type_ = func(field_value)
            if validation_successful:
                return type_

        return "text"

    @staticmethod
    @add_type(type_="email")
    def _validate_email(email: str) -> bool:
        try:
            validate_email(email, check_deliverability=False)
            return True
        except EmailNotValidError:
            return False

    @staticmethod
    @add_type(type_="date")
    def _validate_date(date: str):
        for template in ("%d.%m.%Y", "%Y-%m-%d"):
            try:
                datetime.strptime(date, template).date()
                return True
            except ValueError:
                pass
        return False

    @staticmethod
    @add_type(type_="phone")
    def _validate_phone_ru(phone: str):
        phone = phone.strip().replace(" ", "")
        startswith = phone.startswith("+7")
        isdigit = phone[1:].isdigit()
        length = len(phone) == 12
        statements = (startswith, isdigit, length)
        return all(statements)


validator = Validator()
