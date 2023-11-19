from typing import Dict, List, Type, Tuple
from app.exceptions import *
from app.database import session
from dataclasses import dataclass
from uuid import uuid4
from collections import OrderedDict
from app.validator import validator, ValidatedStr


@dataclass
class Field:
    name: str
    type_: ValidatedStr


def _validate_input_string(statement: bool, exception: Type[ValidatorException]) -> None:
    try:
        assert statement
    except AssertionError:
        raise exception


def _validate_params(params):
    _validate_input_string("=" in params, NoPairProvidedError)
    _validate_input_string(params[0] != "=", NoNameProvidedError)
    _validate_input_string(params[-1] != "=", NoValueProvidedError)
    param_pair = params.split("=")
    _validate_input_string(len(param_pair) == 2, PairAmbiguousError)
    name = param_pair[0]
    _validate_input_string("template_name" != name, NameFieldIsNotAllowed)
    _validate_input_string(name.strip().replace("_", "").isalnum() & name[0].isalpha(), BadNamingError)
    return param_pair


def parse_string(input_string: str) -> List[str]:
    params_list = input_string.strip().split("&")
    _validate_input_string(len(params_list) == len(set(params_list)), RepeatingNameError)
    return params_list


def _compose_dict(fields_: List[Field]) -> OrderedDict:
    ordered_dict = {field_.name: field_.type_ for field_ in sorted(fields_, key=lambda x: x.name)}
    return OrderedDict(
        **ordered_dict
    )


def _validate(params_list: List[str]) -> List[Field] | Dict:
    fields = []
    for params in params_list:
        try:
            name, value = _validate_params(params)
        except ValidatorException as e:
            return {
                "err": {
                    "type": e.__class__.__name__,
                    "text": e.__doc__
                }
            }
        type_ = validator.validate(value)
        form_field = Field(name=name, type_=type_)
        fields.append(form_field)
    return fields


async def match_template_in_db(params_list: List[str]) -> Dict[str, ValidatedStr | Dict | List]:

    fields = _validate(params_list)
    if isinstance(fields, Dict):
        return fields
    fields_dict = _compose_dict(fields)
    db_result = await session.find_all(fields_dict)
    if db_result is not None:
        return {
            "template_names": db_result
        }
    else:
        return fields_dict
