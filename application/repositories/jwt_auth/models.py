import uuid
from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel


class ProfileDTO(BaseModel):
    access_token: str
    expired_at: datetime
    user_id: int
    first_name: str
    last_name: str = ""
    photo_200: str = ""


class AccessTokenHash(BaseModel):
    user_id: str
    exp: int
    first_name: str

    @classmethod
    def create(cls, profile: ProfileDTO, lifetime: int):
        return cls(
            user_id=str(profile.user_id),
            first_name=profile.first_name,
            exp=(datetime.now() + timedelta(seconds=lifetime)).timestamp(),
        )


class RefreshTokenHash(BaseModel):
    user_id: str
    exp: int
    otp_change: Optional[str] = None

    @classmethod
    def create(cls, profile: ProfileDTO):
        return cls(user_id=str(profile.user_id), exp=profile.expired_at.timestamp(), otp_change=uuid.uuid4().hex)
