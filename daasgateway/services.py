import atexit
import os
from typing import Dict, Any, List
from uuid import UUID

import httpx

from daasgateway.auth import DaaSGatewayAuth
from daasgateway.exceptions import DaaSGatewayClientError

URLS = {
    "beta": "https://od9dawmxfa.execute-api.ap-northeast-2.amazonaws.com/beta",
    "prod": "https://3jncvwc1d1.execute-api.ap-northeast-2.amazonaws.com/prod",
}


try:
    _client = httpx.AsyncClient(
        auth=DaaSGatewayAuth(), base_url=URLS[os.getenv("DAAS_GATEWAY_ENV", "prod")]
    )
except KeyError:
    raise DaaSGatewayClientError(
        "Invalid DAAS_GATEWAY_ENV. It must be one of 'beta' or 'prod'."
    )

atexit.register(_client.aclose)


class DaaSGatewayAPIService:
    @staticmethod
    async def create_orders(payload: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            resp = await _client.post("/api/v2/order/orders/", json=payload)
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise DaaSGatewayClientError(
                "Failed to create orders.",
                status_code=exc.response.status_code,
            ) from exc
        return resp.json()

    @staticmethod
    async def create_shipping_items(payload: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            resp = await _client.post("/api/v2/order/orders/shipping/", json=payload)
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise DaaSGatewayClientError(
                "Failed to create shipping items",
                status_code=exc.response.status_code,
            ) from exc
        return resp.json()

    @staticmethod
    async def ready_for_pickup(payload: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            resp = await _client.post(
                "/api/v2/order/orders/readyforpickup/", json=payload
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise DaaSGatewayClientError(
                "Failed to set ready for pickup",
                status_code=exc.response.status_code,
            ) from exc
        return resp.json()

    @staticmethod
    async def cancel_shipping(payload: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            resp = await _client.post("/api/v2/order/shippings/cancel/", json=payload)
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise DaaSGatewayClientError(
                "Failed to cancel shipping",
                status_code=exc.response.status_code,
            ) from exc
        return resp.json()

    @staticmethod
    async def return_shipping(payload: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            resp = await _client.post("/api/v2/order/returns/", json=payload)
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise DaaSGatewayClientError(
                "Failed to return shipping",
                status_code=exc.response.status_code,
            ) from exc
        return resp.json()

    @staticmethod
    async def associate_shipping(payload: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            resp = await _client.post(
                "/api/v2/order/shippings/associate/", json=payload
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise DaaSGatewayClientError(
                "Failed to associate shippings",
                status_code=exc.response.status_code,
            ) from exc
        return resp.json()

    @staticmethod
    async def create_pickup(payload: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            resp = await _client.post("/api/v2/order/pickups/", json=payload)
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise DaaSGatewayClientError(
                "Failed to create pickup",
                status_code=exc.response.status_code,
            ) from exc
        return resp.json()

    @staticmethod
    async def create_pickup_shipping_items(
        payload: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        try:
            resp = await _client.post("/api/v2/order/pickups/shipping/", json=payload)
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise DaaSGatewayClientError(
                "Failed to create pickup shipping items",
                status_code=exc.response.status_code,
            ) from exc
        return resp.json()

    @staticmethod
    async def get_job_group_status(job_group_uuid: UUID) -> Dict[str, Any]:
        try:
            resp = await _client.get(f"/api/v1/jobs/groups/{job_group_uuid}/")
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise DaaSGatewayClientError(
                "Failed to get job group status.",
                status_code=exc.response.status_code,
            ) from exc
        return resp.json()

    @staticmethod
    async def get_job_request_payload(
        job_group_uuid: UUID, job_uuid: UUID
    ) -> Dict[str, Any]:
        try:
            resp = await _client.get(
                f"/api/v1/jobs/groups/{job_group_uuid}/jobs/{job_uuid}/request/"
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise DaaSGatewayClientError(
                "Failed to get job payload.",
                status_code=exc.response.status_code,
            ) from exc
        return resp.json()

    @staticmethod
    async def get_job_response(job_group_uuid: UUID, job_uuid: UUID) -> Dict[str, Any]:
        try:
            resp = await _client.get(
                f"/api/v1/jobs/groups/{job_group_uuid}/jobs/{job_uuid}/response/"
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise DaaSGatewayClientError(
                "Failed to get job response.",
                status_code=exc.response.status_code,
            ) from exc
        return resp.json()
