import logging
from dataclasses import dataclass

from application.repositories.jwt_auth.exceptions import Unauthorized
from application.repositories.jwt_auth.tokenaizer import TokenizerRepository
from application.repositories.database.Profile import User
from application.repositories.vk_client.models import ProfileVkResponse
from application.repositories.vk_client.repository import VkClientApi

logger = logging.getLogger(__name__)


@dataclass
class BackendProfileViewUseCase:
    jwt_repo: TokenizerRepository
    vk_client: VkClientApi

    async def execute(self, user_id: int) -> ProfileVkResponse:
        vk_token = await User.get_vk_access_token_by_id_and_not_expired(user_id=user_id)
        if not vk_token:
            raise Unauthorized()
        vk_profile = await self.vk_client.get_profile_by_token(token=vk_token)
        await User.update_by_vk_profile(vk_profile=vk_profile)
        return vk_profile
