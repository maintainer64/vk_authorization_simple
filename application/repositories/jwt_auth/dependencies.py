import logging
from dataclasses import dataclass
from starlette.requests import Request

from application.usecases.check_token_backend import BackendValidatorTokenUseCase


logger = logging.getLogger(__name__)


@dataclass
class DependenciesGetUserId:
    uc: BackendValidatorTokenUseCase

    async def get_user_id(
        self,
        request: Request,
    ) -> int:
        logger.info("Обработка заголовка авторизации")
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        return await self.uc.validate_get_user_id(token=token)
