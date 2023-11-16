from fastapi import FastAPI, status
from settings import settings
from typing import Dict
from services import connector

app = FastAPI(**settings.app_description)


@app.post("/api/get_form/{params}", tags=["Forms"], status_code=status.HTTP_200_OK)
async def get_form(params: str) -> Dict:
    response_dict = await connector.match_template_in_db(params)
    return response_dict
