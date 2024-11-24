from __future__ import annotations

from enum import Enum
from typing import List, \
    Optional, \
    Any

from pydantic import BaseModel, \
    Field, \
    ConfigDict
from dm_api_account.models.user_envelope import UserRole
from datetime import datetime


class Rating(BaseModel):
    enabled: bool
    quality: int
    quantity: int


class ColorSchema(Enum):
    MODERN = 'Modern'
    PALE = 'Pale'
    CLASSIC = 'Classic'
    CLASSIC_PALE = 'ClassicPale'
    NIGHT = 'Night'


class Paging(BaseModel):
    posts_per_page: int = Field(None, alias='postsPerPage')
    comments_per_page: int = Field(None, alias='commentsPerPage')
    topics_per_page: int = Field(None, alias='topicsPerPage')
    messages_per_page: int = Field(None, alias='messagesPerPage')
    entities_per_page: int = Field(None, alias='entitiesPerPage')


class Settings(BaseModel):
    color_schema: ColorSchema = Field(None, alias='colorSchema')
    nanny_greetings_message: str = Field(None, alias='nannyGreetingsMessage')
    paging: Paging


class UserDetails(BaseModel):
    login: str = Field(None, description='Login')
    roles: List[UserRole]
    medium_picture_url: str = Field(None, alias='mediumPictureUrl')
    small_picture_url: str = Field(None, alias='smallPictureUrl')
    status: str = Field(None, alias='status')
    rating: Rating
    online: datetime = Field(None, alias='online')
    name: str = Field(None, alias='name')
    location: str = Field(None, alias='location')
    registration: datetime = Field(None, alias='registration')
    icq: str = Field(None)
    skype: str = Field(None)
    original_picture_url: str = Field(None, alias='originalPictureUrl')
    info: Any = Field(None)
    settings: Settings = None


class UserDetailsEnvelope(BaseModel):
    model_config = ConfigDict(extra='forbid')
    resource: Optional[UserDetails] = None
    metadata: Optional[Any] = None
