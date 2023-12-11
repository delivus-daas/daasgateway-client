import os
import time
from typing import Optional, NoReturn

import httpx
from pydantic import BaseModel, SecretStr, Field

from daasgateway.exceptions import DaaSGatewayClientError


class DaaSGatewayAuth(httpx.Auth):
    """
    An auth class for the DaaSGatewayClient. This class handles the authentication flow
    """

    class _Credentials(BaseModel):
        username: str
        password: SecretStr
        app_client_id: SecretStr
        region: Optional[str] = None
        id_token: SecretStr = Field(default=None)
        refresh_token: SecretStr = Field(default=None)
        expiry: Optional[int] = Field(default=None)

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        app_client_id: Optional[str] = None,
        region: Optional[str] = None,
    ):
        self._credentials = self._Credentials(
            username=username or os.environ.get("DAAS_GATEWAY_USERNAME"),
            password=password or os.environ.get("DAAS_GATEWAY_PASSWORD"),
            app_client_id=app_client_id or os.environ.get("DAAS_GATEWAY_CLIENT_ID"),
            region=region or os.environ.get("AWS_REGION"),
        )

    async def _login(self) -> NoReturn:
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(
                    f"https://cognito-idp.{self._credentials.region}.amazonaws.com/",
                    json={
                        "AuthFlow": "USER_PASSWORD_AUTH",
                        "ClientId": self._credentials.app_client_id.get_secret_value(),
                        "AuthParameters": {
                            "USERNAME": self._credentials.username,
                            "PASSWORD": self._credentials.password.get_secret_value(),
                        },
                    },
                )
                resp.raise_for_status()
            except httpx.HTTPStatusError as exc:
                raise DaaSGatewayClientError(
                    "Failed to login to Cognito",
                    status_code=exc.response.status_code if exc.response else None,
                ) from exc
            body = resp.json()
            self._credentials.id_token = body["AuthenticationResult"]["IdToken"]
            self._credentials.refresh_token = body["AuthenticationResult"][
                "RefreshToken"
            ]
            self._credentials.expiry = (
                body["AuthenticationResult"]["ExpiresIn"] + time.time()
            )

    async def _refresh(self) -> NoReturn:
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(
                    f"https://cognito-idp.{self._credentials.region}.amazonaws.com/",
                    json={
                        "AuthFlow": "REFRESH_TOKEN_AUTH",
                        "ClientId": self._credentials.app_client_id.get_secret_value(),
                        "AuthParameters": {
                            "REFRESH_TOKEN": self._credentials.refresh_token.get_secret_value(),
                        },
                    },
                )
                resp.raise_for_status()
            except httpx.HTTPStatusError as exc:
                raise DaaSGatewayClientError(
                    "Failed to refresh Cognito token",
                    status_code=exc.response.status_code,
                ) from exc
            body = resp.json()
            self._credentials.id_token = body["AuthenticationResult"]["IdToken"]
            self._credentials.refresh_token = body["AuthenticationResult"][
                "RefreshToken"
            ]
            self._credentials.expiry = (
                body["AuthenticationResult"]["ExpiresIn"] + time.time()
            )

    async def async_auth_flow(self, request):
        if self._credentials.id_token is None:
            await self._login()
        elif (
            self._credentials.expiry is not None
            and self._credentials.expiry < time.time()
        ):
            await self._refresh()
        request.headers[
            "Authorization"
        ] = f"Bearer {self._credentials.id_token.get_secret_value()}"
        yield request
