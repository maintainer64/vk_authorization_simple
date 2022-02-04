import datetime
from typing import Optional

import peewee

from application.repositories.database.bind import db_manager, database
from application.repositories.jwt_auth.models import ProfileDTO
from application.repositories.vk_client.models import ProfileVkResponse


class User(peewee.Model):
    id = peewee.IntegerField(primary_key=True, index=True, null=False)
    first_name = peewee.CharField(null=False)
    last_name = peewee.CharField(null=False)
    photo_200 = peewee.CharField(null=False)
    refresh_token = peewee.TextField(index=True, null=True)
    vk_access_token = peewee.CharField(null=True)
    vk_access_token_expired_at = peewee.DateTimeField(null=True)
    created_at = peewee.DateTimeField(null=False)
    updated_at = peewee.DateTimeField(null=False)

    @classmethod
    async def get_vk_access_token_by_id_and_not_expired(cls, user_id: int) -> Optional[str]:
        now = datetime.datetime.now()
        query = cls.select(cls.vk_access_token).where((cls.id.in_((user_id,))) & (cls.vk_access_token_expired_at > now))
        try:
            profile: "User" = await db_manager.get(query)
            return profile.vk_access_token
        except Exception:
            import traceback

            traceback.print_exc()
            return None

    @classmethod
    async def update_by_vk_profile(cls, vk_profile: ProfileVkResponse):
        now = datetime.datetime.now()
        query = cls.update(
            {
                cls.first_name: vk_profile.first_name,
                cls.last_name: vk_profile.last_name,
                cls.photo_200: vk_profile.photo_200,
                cls.updated_at: now,
            }
        ).where(cls.id == vk_profile.id)
        await db_manager.execute(query)

    @classmethod
    async def get_by_refresh_token(cls, refresh_token: str) -> Optional[ProfileDTO]:
        query = cls.select().where(cls.refresh_token == refresh_token).order_by(cls.id.desc()).limit(1)
        try:
            profile: "User" = await db_manager.get(query)
            return ProfileDTO(
                access_token=profile.vk_access_token,
                expired_at=profile.vk_access_token_expired_at,
                user_id=profile.id,
                first_name=profile.first_name,
                last_name=profile.last_name,
                photo_200=profile.photo_200,
            )
        except Exception:
            return None

    @classmethod
    async def set_refresh_token_on_profile(cls, user_id: int, refresh_token: str):
        now = datetime.datetime.now()
        query = cls.update({cls.refresh_token: refresh_token, cls.updated_at: now}).where(cls.id == user_id)
        await db_manager.execute(query)

    @classmethod
    async def create_or_update(cls, profile: ProfileDTO, refresh_token: str = None) -> Optional["ProfileDTO"]:
        now = datetime.datetime.now()
        query = cls.insert(
            id=profile.user_id,
            first_name=profile.first_name,
            last_name=profile.last_name,
            photo_200=profile.photo_200,
            refresh_token=refresh_token,
            vk_access_token=profile.access_token,
            vk_access_token_expired_at=profile.expired_at,
            created_at=now,
            updated_at=now,
        ).on_conflict(
            conflict_target=(cls.id,),
            update={
                cls.first_name: profile.first_name,
                cls.last_name: profile.last_name,
                cls.photo_200: cls.photo_200,
                cls.refresh_token: refresh_token,
                cls.vk_access_token: profile.access_token,
                cls.vk_access_token_expired_at: profile.expired_at,
                cls.updated_at: now,
            },
        )
        await db_manager.execute(query)
        return profile

    class Meta:
        db_table = "usersdata"
        database = database
