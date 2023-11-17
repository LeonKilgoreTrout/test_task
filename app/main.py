from fastapi import FastAPI, Response, status
from pydantic import BaseModel, create_model
from settings import settings
from typing import Dict
from app.services import connector, parse_string


app = FastAPI(**settings.app_description)


class TemplateNameModel(BaseModel):
    template_name: str


class ErrorModel(BaseModel):
    err: create_model('ErrNameModel', type=(str, ...), text=(str, ...))


@app.post("/api/get_form/{params}", tags=["Forms"], status_code=status.HTTP_200_OK)
async def get_form(params: str,
                   response: Response) -> TemplateNameModel | ErrorModel | Dict:

    params_list = parse_string(params)
    response.status_code = status.HTTP_200_OK
    response_dict = await connector.match_template_in_db(params_list)
    if "err" in response_dict.keys():
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return_model = ErrorModel(**response_dict)
    elif "template_name" in response_dict.keys():
        return_model = TemplateNameModel(**response_dict)
    else:
        return_model = response_dict
    return return_model
