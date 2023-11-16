from typing import Dict, List, Type, Tuple
from app_exceptions import *
from database import session
from dataclasses import dataclass
from uuid import uuid4
from collections import OrderedDict
from validator import Validator, ValidatedStr


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
    _validate_input_string(name.strip().replace("_", "").isalnum() & name[0].isalpha(), BadNamingError)
    return param_pair


def parse_string(input_string: str) -> List[str]:
    params_list = input_string.strip().split("&")
    _validate_input_string(len(params_list) == len(set(params_list)), RepeatingNameError)
    return params_list


class Connector:

    def __init__(self):
        self.session = session
        self.validator = Validator()
        self.last_form = None

    async def match_template_in_db(self, input_string: str) -> Dict[str, ValidatedStr | str | Dict]:
        params_list = parse_string(input_string)
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

            type_ = self.validator.validate(value)
            form_field = Field(name=name, type_=type_)
            fields.append(form_field)
        fields = self._compose_dict(fields)
        db_result = await self.get_template(fields)
        if db_result is not None:
            return {
                "template_name": db_result["name"]
            }
        return fields

    @staticmethod
    def _compose_dict(fields_) -> OrderedDict:
        ordered_dict = {field_.name: field_.type_ for field_ in sorted(fields_, key=lambda x: x.name)}
        return OrderedDict(
            **ordered_dict
        )

    async def add_template(self, fields: OrderedDict[str, ValidatedStr]):
        form = {
            "name": str(uuid4()),
            **fields
        }
        await self.session._do_insert(form)

    async def get_template(self, fields: Dict[str, str]) -> Dict[str, str] | None:
        query = {'$or': [{key: {'$exists': True}} for key in fields.keys()]}
        result = await self.session._find_one(query)
        return result


connector = Connector()
