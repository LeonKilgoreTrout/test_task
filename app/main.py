from fastapi import FastAPI, Response, status
from pydantic import BaseModel, create_model
from settings import settings
from typing import Dict, List
from app.services import parse_string, match_template_in_db
from app.exceptions import ValidatorException as e


app = FastAPI(**settings.app_description)


class TemplateNameModel(BaseModel):
    template_names: List[str]


class ErrorModel(BaseModel):
    err: create_model('ErrNameModel', type=(str, e.__name__), text=(str, e.__doc__))


error_response = {
    422: {
        'model': ErrorModel,
        'description': 'Validation Error',
    }
}


@app.post("/api/get_form/{params}",
          tags=["Forms"],
          responses=error_response,
          status_code=status.HTTP_200_OK)
async def get_form(
        params: str,
        response: Response
        ) -> TemplateNameModel | ErrorModel | Dict:

    # здесь намеренно использован собственный парсер, легко заменяется урллибовским
    params_list = parse_string(params)

    response.status_code = status.HTTP_200_OK
    response_dict = await match_template_in_db(params_list)
    if "err" in response_dict.keys():
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return_model = ErrorModel(**response_dict)
    elif "template_names" in response_dict.keys():
        return_model = TemplateNameModel(**response_dict)
    else:
        return_model = response_dict
    return return_model
