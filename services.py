from typing import Dict, List, Type, Tuple, Literal
from app_exceptions import *
from email_validator import validate_email, EmailNotValidError
from datetime import datetime
from database import session
from dataclasses import dataclass, field, asdict
from uuid import uuid4


StrType = Literal["date", "phone", "email", "text"]


def add_type(type_: StrType):
    def decorator(func):
        def wrap(*args, **kwargs):
            d = func(*args, **kwargs)
            return d, type_
        return wrap
    return decorator


@dataclass
class Field:
    name: str
    value: str
    type_: StrType | None = None
    is_validated: bool = False


@dataclass
class Form:
    name: str = str(uuid4())
    fields: List[Field] = field(default_factory=list)


class Parser:

    def __init__(self):
        self.validator = Validator()
        self.session = session
        self.last_form = None

    def compose_form_from_string(self, input_string: str):
        params_list = input_string.strip().split("&")
        self._validate_input_string(len(params_list) == len(set(params_list)), RepeatingNameError)
        form = Form()
        for param in params_list:
            name, value = self._validate_pair_param(param)
            form_field = Field(name=name, value=value)
            form_field = self.validator.validate(form_field)
            form.fields.append(form_field)

        try:
            form_dict = self.correct_dict(form)
            print("before_db", form_dict)
            result = session.find_one(form_dict)
            print("after_db", result)
            return form_dict if result else self.wrong_dict(form)

        except Exception as e:
            print(e)

    @staticmethod
    def correct_dict(form: Form):
        d = {
            field_.name: field_.value for field_ in form.fields
        }
        d["name"] = form.name
        return d

    @staticmethod
    def wrong_dict(form: Form):
        d = {
            field_.name: field_.type_ for field_ in form.fields
        }
        return d

    @staticmethod
    def _validate_input_string(statement: bool, exception: Type[ValidatorException]) -> None:
        try:
            assert statement
        except AssertionError:
            raise exception

    def _validate_pair_param(self, param) -> Tuple[str, StrType]:
        self._validate_input_string("=" in param, NoPairProvidedError)
        self._validate_input_string(param[0] != "=", NoNameProvidedError)
        self._validate_input_string(param[-1] != "=", NoValueProvidedError)
        param_pair = param.split("=")
        self._validate_input_string(len(param_pair) == 2, PairAmbiguousError)
        name = param_pair[0]
        self._validate_input_string(name.strip().replace("_", "").isalnum() & name[0].isalpha(), BadNamingError)
        return param_pair


class Validator:
    """ Class for fields validation """
    def __init__(self):
        self._validation_ordered_functions = [
            self._validate_date,
            self._validate_phone_ru,
            self._validate_email
        ]
        self.last_validated_field = None

    def validate(self, form_field: Field) -> Field:

        for func in self._validation_ordered_functions:
            validation_successful, type_ = func(form_field.value)
            if validation_successful:
                form_field.type_ = type_
                form_field.is_validated = True
                self.last_validated_field = form_field
            elif not form_field.is_validated:
                form_field.type_ = "text"

        return form_field

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


s = Parser()
ss = s.compose_form_from_string("f_name1=12.12.2012&f_name4=+77992379428&f_name2=value2@sd.ty&s=3fe")
print(ss)
