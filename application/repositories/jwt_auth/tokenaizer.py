from datetime import datetime
from typing import Optional
from jwt import decode as jwt_decode, encode as jwt_encode, PyJWTError
from pydantic import ValidationError, BaseModel, Field

from application.repositories.jwt_auth.models import AccessTokenHash, RefreshTokenHash, ProfileDTO


class TokenDataDTO(BaseModel):
    token: str
    exp: int


class JWTTokensDTO(BaseModel):
    access: Optional[TokenDataDTO] = Field(None)
    refresh: Optional[TokenDataDTO] = Field(None)


class TokenizerRepository:
    def __init__(self, secret_key_access: str, secret_key_refresh: str):
        self.algorithm = "HS256"
        self.secret_key_access = secret_key_access
        self.secret_key_refresh = secret_key_refresh
        self.lifetime_access = 10800

    def __create_refresh_token(self, *, profile: ProfileDTO) -> TokenDataDTO:
        token = RefreshTokenHash.create(profile=profile)
        encoded_jwt = jwt_encode(token.dict(), self.secret_key_refresh, algorithm=self.algorithm)
        return TokenDataDTO(token=encoded_jwt, exp=token.exp)

    def decode_refresh_token(self, token: str) -> Optional[RefreshTokenHash]:
        token_obj: RefreshTokenHash = self.__check_payload_token(
            token=token, secret_key=self.secret_key_refresh, algorithm=self.algorithm, model_validate=RefreshTokenHash
        )  # type: ignore
        if not token_obj:
            return None
        now = datetime.now().timestamp()
        if token_obj.exp < now:
            return None
        return token_obj

    def __create_access_token(self, *, profile: ProfileDTO) -> TokenDataDTO:
        token = AccessTokenHash.create(profile=profile, lifetime=self.lifetime_access)
        encoded_jwt = jwt_encode(token.dict(), self.secret_key_access, algorithm=self.algorithm)
        return TokenDataDTO(token=encoded_jwt, exp=token.exp)

    def decode_access_token(self, token: str) -> Optional[AccessTokenHash]:
        token_obj: AccessTokenHash = self.__check_payload_token(
            token=token, secret_key=self.secret_key_access, algorithm=self.algorithm, model_validate=AccessTokenHash
        )  # type: ignore
        if token_obj is None:
            return
        now = datetime.now().timestamp()
        if token_obj.exp < now:
            return None
        return token_obj

    @staticmethod
    def __check_payload_token(
        token: Optional[str], secret_key: str, algorithm: str, model_validate: BaseModel
    ) -> Optional[BaseModel]:
        try:
            payload = jwt_decode(token, secret_key, algorithms=algorithm)  # type: ignore
            return model_validate.parse_obj(payload)
        except (PyJWTError, ValidationError):
            return None

    def generate_tokens_data(self, profile: ProfileDTO) -> JWTTokensDTO:
        return JWTTokensDTO(
            refresh=self.__create_refresh_token(profile=profile),
            access=self.__create_access_token(profile=profile),
        )
