from typing import Optional

from pydantic import BaseModel, \
    Field, \
    ConfigDict


class NewPasswordCredentials(BaseModel):
    model_config = ConfigDict(extra='forbid')
    login: str = Field(..., description='Логин')
    old_password: str = Field(..., description='Старый Пароль', alias='oldPassword')
    new_password: str = Field(..., description='Новый пароль', alias='newPassword')
    token: str = Field(..., description='Токен')