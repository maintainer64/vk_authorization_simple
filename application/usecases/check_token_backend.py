from dataclasses import dataclass

from application.repositories.jwt_auth.exceptions import Unauthorized
from application.repositories.jwt_auth.models import AccessTokenHash
from application.repositories.jwt_auth.tokenaizer import TokenizerRepository


@dataclass
class BackendValidatorTokenUseCase:
    jwt_repo: TokenizerRepository

    async def validate(self, jwt_data_token: str) -> AccessTokenHash:
        try:
            token = self.jwt_repo.decode_access_token(token=jwt_data_token)
            if token is None:
                raise Exception("Token is null")
            int(token.user_id)
        except Exception as err:
            raise Unauthorized() from err
        return token

    async def validate_get_user_id(self, token: str) -> int:
        token_data = await self.validate(jwt_data_token=token)
        return int(token_data.user_id)
