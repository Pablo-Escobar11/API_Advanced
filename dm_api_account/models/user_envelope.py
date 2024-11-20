import datetime
from enum import Enum

from pydantic import BaseModel, \
    ConfigDict
from typing import List, \
    Optional
from pydantic import BaseModel, \
    Field


class UserRoles(str, Enum):
    """[ Guest, Player, Administrator, NannyModerator, RegularModerator, SeniorModerator ]"""
    GUEST = 'Guest'
    PLAYER = 'Player'
    ADMINISTRATOR = 'Administrator'
    NANNY_MODERATOR = 'NannyModerator'
    REGULAR_MODERATOR = 'RegularModerator'
    SENIOR_MODERATOR = 'SeniorModerator'


class Rating(BaseModel):
    enabled: bool
    quality: int
    quantity: int


class User(BaseModel):
    login: str
    roles: List[UserRoles]
    medium_picture_url: str = Field(..., alias='mediumPictureUrl')
    small_picture_url: str = Field(..., alias='smallPictureUrl')
    status: str
    rating: Rating
    online: datetime
    name: str
    location: str
    registration: datetime


class UserEnvelope(BaseModel):
    model_config = ConfigDict(extra='forbid')
    resource: Optional[User] = None
    metadata: Optional[str] = None
