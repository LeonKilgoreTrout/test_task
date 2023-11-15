from fastapi import Depends, FastAPI, Response, status, Request
from settings import settings
from typing import Dict
# from schemas import CustomerForm
# from services import parse_string

app = FastAPI(**settings.get("app_description"))


@app.post("/api/get_form/{params}", tags=["Forms"], status_code=status.HTTP_200_OK)
async def get_form(params: str):
    # params_dict = parse_string(params)
    print("+++++++++++++++++++++++++++++++++++\n\n\n")
    print(Request)
    # params_form = CustomerForm(**params_dict)

    return None
