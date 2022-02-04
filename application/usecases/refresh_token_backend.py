import logging
from dataclasses import dataclass
from application.repositories.jwt_auth.tokenaizer import TokenizerRepository, JWTTokensDTO
from application.repositories.database.Profile import User

from fastapi_jsonrpc import BaseError


class BackendRefreshTokenException(BaseError):
    CODE = 4000
    MESSAGE = "Refresh not valid"


logger = logging.getLogger(__name__)


@dataclass
class BackendRefreshTokenUseCase:
    jwt_repo: TokenizerRepository

    async def execute(self, refresh_token: str) -> JWTTokensDTO:
        logger.info("BackendRefreshTokenUseCase start")
        refresh_token_payload = self.jwt_repo.decode_refresh_token(token=refresh_token)
        if not refresh_token_payload:
            raise BackendRefreshTokenException
        logger.info("BackendRefreshTokenUseCase refresh validate")
        profile = await User.get_by_refresh_token(refresh_token=refresh_token)
        if not profile:
            raise BackendRefreshTokenException
        logger.info("BackendRefreshTokenUseCase generate token data")
        tokens = self.jwt_repo.generate_tokens_data(profile)
        await User.set_refresh_token_on_profile(
            user_id=profile.user_id, refresh_token=tokens.refresh.token if tokens.refresh is not None else ""
        )
        return tokens
