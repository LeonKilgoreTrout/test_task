from __future__ import annotations
from datetime import datetime
from email_validator import validate_email, EmailNotValidError
from pydantic import (
    AfterValidator, BaseModel, ConfigDict, EmailStr, field_validator, validator, model_validator, SkipValidation, ValidationInfo, ValidationError
)
from pydantic_core import PydanticCustomError
from typing import Dict, List, NewType, TypedDict, Callable, Any, cast
from typing_extensions import Annotated
# from pydantic.functional_validators import

DateStr = NewType("Date", str)
PhoneStr = NewType("Phone", str)
TextStr = NewType("Phone", str)

CUSTOM_MESSAGES = {

}


def must_contain_phone_number(phone: str):
    phone = phone.strip().replace(" ", "")
    startswith = phone.startswith("+7")
    print(phone, startswith)
    isdigit = phone[1:].isdigit()
    print(phone, isdigit)
    length = len(phone) == 12
    print(phone, length)
    statements = (startswith, isdigit, length)
    if all(statements):
        return phone
    else:
        raise ValueError


def must_contain_date(date: str):

    try:
        datetime.strptime(date, '%Y-%m-%d')
        print(datetime.strptime(date, '%Y-%m-%d'))
        return date
    except (ValueError, TypeError):
        try:
            datetime.strptime(date, '%d.%m.%Y')
            print(datetime.strptime(date, '%d.%m.%Y'))
            return date
        except (ValueError, TypeError):
            raise ValueError


def must_contain_email(email):
    try:
        return validate_email(email).normalized
    except EmailNotValidError:
        raise ValueError


class CustomerForm(BaseModel):
    """
        Form with customer's order
    """
    name: SkipValidation[str]
    model_config = ConfigDict(extra="allow", )

    # @staticmethod
    # def make_validator(label: str) -> Callable[[str, ValidationInfo], str]:
    #     def validator(v: Any, info: ValidationInfo) -> Any:
    #         context = cast(Context, info.context)
    #         context['logs'].append(label)
    #         return v
    #     return validator

    # @staticmethod
    # def must_contain_phone_number(phone: str):
    #
    #     phone = phone.strip().replace(" ", "")
    #     startswith = phone.startswith("+7")
    #     print(phone, startswith)
    #     isdigit = phone[1:].isdigit()
    #     print(phone, isdigit)
    #     length = len(phone) == 12
    #     print(phone, length)
    #     statements = (startswith, isdigit, length)
    #     if all(statements):
    #         return phone
    #     else:
    #         raise ValueError

    # @staticmethod
    # def must_contain_date(date: str):
    #
    #     try:
    #         datetime.strptime(date, '%Y-%m-%d')
    #         print(datetime.strptime(date, '%Y-%m-%d'))
    #         return date
    #     except (ValueError, TypeError):
    #         try:
    #             datetime.strptime(date, '%d.%m.%Y')
    #             print(datetime.strptime(date, '%d.%m.%Y'))
    #             return date
    #         except (ValueError, TypeError):
    #             return False
    #
    # def apply_validator(self, key: str, value: str):
    #     field_validator(key)(self.make_validator(self.must_contain_date(value)))
    #     field_validator(key)(self.make_validator(self.must_contain_phone_number(value)))

    @staticmethod
    def validate_fields(value: str):
        value = must_contain_date(value)
        value = must_contain_phone_number(value)
        value = must_contain_email(value)
        return value

    @model_validator(mode="after")
    def must_contain_dateawd(self) -> CustomerForm:
        # print(self.__pydantic_extra__)
        self.__pydantic_extra__ = {
            k: self.validate_fields(v) for k, v in self.__pydantic_extra__.items()
        }
        return self

try:
    s = CustomerForm(name="asd", order_date="20-03-1995", customer_mail="asdaswd@mail.ru", customer_phone="+74532342323",  order_description="str")
except ValidationError as e:
    print(e.errors())