from typing import List

from fastapi_jsonrpc import BaseError
from pydantic import BaseModel, Field


class ApiVkError(BaseError):
    CODE = 4000
    MESSAGE = "Integration VK Exception"


class ApiVkConfig(BaseModel):
    client_id: int
    client_secret: str
    redirect_uri: str = "https://localhost:3000/signin/apply"


class AccessTokenVkResponse(BaseModel):
    access_token: str
    expires_in: int
    user_id: int


class ProfileVkResponse(BaseModel):
    id: int
    first_name: str = ""
    last_name: str = ""
    photo_200: str = ""


class ProfileVkResponseList(BaseModel):
    response: List[ProfileVkResponse] = Field(min_items=1)
