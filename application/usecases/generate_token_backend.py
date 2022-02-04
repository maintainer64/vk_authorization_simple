import logging
from dataclasses import dataclass
from datetime import datetime, timedelta

from application.repositories.jwt_auth.models import ProfileDTO
from application.repositories.jwt_auth.tokenaizer import TokenizerRepository, JWTTokensDTO
from application.repositories.database.Profile import User
from application.repositories.vk_client.repository import VkClientApi

logger = logging.getLogger(__name__)


@dataclass
class BackendGeneratorTokenUseCase:
    jwt_repo: TokenizerRepository
    vk_client: VkClientApi

    async def execute(self, code: str) -> JWTTokensDTO:
        vk_token = await self.vk_client.get_access_token(code=code)
        vk_profile = await self.vk_client.get_profile_by_token(token=vk_token.access_token)
        expired_vk_token = datetime.now() + timedelta(seconds=vk_token.expires_in - 60)
        profile = ProfileDTO(
            access_token=vk_token.access_token,
            expired_at=expired_vk_token,
            user_id=vk_profile.id,
            first_name=vk_profile.first_name,
            last_name=vk_profile.last_name,
            photo_200=vk_profile.photo_200,
        )
        tokens = self.jwt_repo.generate_tokens_data(profile)
        await User.create_or_update(
            profile=profile, refresh_token=tokens.refresh.token if tokens.refresh is not None else ""
        )
        return tokens
