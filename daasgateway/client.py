from typing import List

from daasgateway.services import DaaSGatewayAPIService
from daasgateway.models import JobGroup
from daasgateway import requests


class DaaSGatewayClient:
    async def create_orders(
        self, orders: List[requests.CreateOrderRequest]
    ) -> JobGroup:
        payload = [
            order.model_dump(exclude_unset=True, exclude_none=True) for order in orders
        ]
        response = await DaaSGatewayAPIService.create_orders(payload=payload)
        job_group_uuid = response["job_group_uuid"]
        return JobGroup(uuid=job_group_uuid)

    async def create_shipping_items(
        self, shipping_items: List[requests.CreateShippingItemRequest]
    ) -> JobGroup:
        payload = [
            shipping_item.model_dump(exclude_unset=True, exclude_none=True)
            for shipping_item in shipping_items
        ]
        response = await DaaSGatewayAPIService.create_shipping_items(payload=payload)
        job_group_uuid = response["job_group_uuid"]
        return JobGroup(uuid=job_group_uuid)
