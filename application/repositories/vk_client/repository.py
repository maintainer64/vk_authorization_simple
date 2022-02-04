import logging

import aiohttp

from application.repositories import validators
from application.repositories.vk_client.models import (
    ApiVkConfig,
    AccessTokenVkResponse,
    ApiVkError,
    ProfileVkResponse,
    ProfileVkResponseList,
)

logger = logging.getLogger(__name__)


class VkClientApi:
    def __init__(
        self,
        transport: aiohttp.ClientSession,
        config: ApiVkConfig,
    ):
        self.transport = transport
        self.config = config

    async def get_access_token(self, code: str) -> AccessTokenVkResponse:
        logger.info("VkClientApi. Get access token on VK by code")
        parameters = self.config.dict()
        parameters["code"] = code
        response = await self.transport.get(
            "https://oauth.vk.com/access_token",
            params=parameters,
        )
        try:
            logger.info("VkClientApi. Access token loading and validate")
            data = await response.json()
            model_valid: AccessTokenVkResponse = validators.validate_dict(data, AccessTokenVkResponse)
            logger.debug(f"VkClientApi, get Access token {model_valid.dict()=}")
            return model_valid
        except Exception as e:
            raise ApiVkError() from e

    async def get_profile_by_token(self, token: str) -> ProfileVkResponse:
        logger.info("VkClientApi. Get profile user by token")
        headers = {
            "content-type": "application/x-www-form-urlencoded",
        }
        response = await self.transport.post(
            url="https://api.vk.com/method/users.get",
            headers=headers,
            data=f"fields=photo_200&access_token={token}&v=5.131",
        )
        try:
            logger.info("VkClientApi. Profile loading and validate")
            data = await response.json()
            model_valid: ProfileVkResponseList = validators.validate_dict(data, ProfileVkResponseList)
            return model_valid.response[0]
        except Exception as e:
            raise ApiVkError() from e
