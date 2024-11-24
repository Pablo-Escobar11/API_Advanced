from typing import Optional

from pydantic import BaseModel, \
    Field, \
    ConfigDict


class ResetCredentials(BaseModel):
    model_config = ConfigDict(extra='forbid')
    login: str = Field(..., description='Логин')
    email: str = Field(..., description='email')