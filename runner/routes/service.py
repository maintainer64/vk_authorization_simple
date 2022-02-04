import logging
from fastapi import Body

from dataclasses import dataclass

from starlette.requests import Request

from application.dependencies.interface import RPCMethod
from application.repositories.jwt_auth.dependencies import DependenciesGetUserId
from application.repositories.jwt_auth.tokenaizer import JWTTokensDTO
from application.repositories.vk_client.models import ProfileVkResponse
from application.usecases.generate_token_backend import BackendGeneratorTokenUseCase
from application.usecases.profile_logics import BackendProfileViewUseCase
from application.usecases.refresh_token_backend import BackendRefreshTokenUseCase

logger = logging.getLogger(__name__)


@dataclass
class ServiceEntrypoint(RPCMethod):
    uc_generate: BackendGeneratorTokenUseCase
    uc_refresh: BackendRefreshTokenUseCase
    uc_view_profile: BackendProfileViewUseCase
    dp: DependenciesGetUserId

    @property
    def methods(self) -> list:
        return [self.access_by_code, self.access_by_refresh, self.profile_get]

    async def access_by_code(self, code: str = Body(..., min_length=1)) -> JWTTokensDTO:
        return await self.uc_generate.execute(code=code)

    async def access_by_refresh(self, refresh_token: str = Body(..., min_length=1)) -> JWTTokensDTO:
        return await self.uc_refresh.execute(refresh_token=refresh_token)

    async def profile_get(self, request: Request) -> ProfileVkResponse:
        user_id = await self.dp.get_user_id(request=request)
        logger.info(f"Method profile_get on user {user_id=}")
        return await self.uc_view_profile.execute(user_id=user_id)
