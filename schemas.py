from __future__ import annotations
from datetime import datetime
from email_validator import validate_email, EmailNotValidError
from pydantic import (
    AfterValidator, BaseModel, create_model, ConfigDict, EmailStr, field_validator, validator, model_validator, SkipValidation, ValidationInfo, ValidationError
)
from pydantic_core import PydanticCustomError
from typing import Dict, List, NewType, TypedDict, Callable, Any, cast, Tuple, TypeAlias, Type, get_type_hints
from typing_extensions import Annotated
# from pydantic.functional_validators import

# EmailStr = NewType("EmailStr", str)
DateStr = NewType("DateStr", str)
PhoneStr = NewType("PhoneStr", str)
TextStr = NewType("TextStr", str)

Str: TypeAlias = EmailStr | DateStr | PhoneStr | TextStr

CUSTOM_MESSAGES = {

}


def must_contain_phone_number(phone: str):
    phone = phone.strip().replace(" ", "")
    startswith = phone.startswith("+7")
    # print(phone, startswith)
    isdigit = phone[1:].isdigit()
    # print(phone, isdigit)
    length = len(phone) == 12
    # print(phone, length)
    statements = (startswith, isdigit, length)
    if all(statements):
        return phone
    else:
        raise ValueError


def must_contain_date(date: str):

    try:
        datetime.strptime(date, '%Y-%m-%d')
        # print(datetime.strptime(date, '%Y-%m-%d'))
        return date
    except (ValueError, TypeError):
        try:
            datetime.strptime(date, '%d.%m.%Y')
            # print(datetime.strptime(date, '%d.%m.%Y'))
            return date
        except (ValueError, TypeError):
            raise ValueError


class CustomerForm(BaseModel):
    """
        Form with customer's order
    """
    name: SkipValidation[str]
    model_config = ConfigDict(extra="allow")

    @staticmethod
    def validate_fields(value) -> Tuple[Type[Str], Str]:
        try:
            value = must_contain_date(value)
            type_ = DateStr
            print(value)
            return type_, value
        except ValueError as ve:
            print(ve)
        try:
            value = must_contain_phone_number(value)
            print(value)
            type_ = PhoneStr
            return type_, value

        except ValueError as ve:
            print(ve)
        try:
            value = must_contain_email(value)
            print(value)
            type_ = EmailStr
            return type_, value
        except ValueError as ve:
            print(ve)
        
        return TextStr, value

    @model_validator(mode="after")
    def must_contain_dateawd(self):
        validated_fields = {
            k: self.validate_fields(v) for k, v in self.__pydantic_extra__.items()
        }
        print(validated_fields)
        ValidatedForm = create_model(
            'ValidatedForm', name=(str, self.name), **validated_fields
        )
        print(get_type_hints(ValidatedForm))
        model = ValidatedForm().model_dump()
        print(model)
        return model

try:
    s = CustomerForm(name="asd",
                     order_date="20-03-1995",
                     customer_mail="asdaswd@mail.rsu",
                     customer_phone="+74532342323",
                     order_description="str")
except ValidationError as e:
    # print(e.errors())
    pass