import asyncio
import logging

from daasgateway.client import DaaSGatewayClient
from daasgateway.requests import CreateOrderRequest, CreateShippingItemRequest

client = DaaSGatewayClient()
logger = logging.getLogger(__name__)


async def create_orders(orders: list):
    requests = [CreateOrderRequest.model_validate(order) for order in orders]
    create_orders_job_group = await client.create_orders(requests)
    await create_orders_job_group.wait_until_completed()
    successful_orders = []
    failed_orders = []
    for job in create_orders_job_group.jobs:
        payload = await job.payload
        if 200 <= job.status_code < 300:
            successful_orders.append(payload["order_number"])
        else:
            failed_orders.append(payload["order_number"])
    return successful_orders, failed_orders


async def create_shipping_items(order_numbers: list):
    requests = [
        CreateShippingItemRequest.model_validate(order_number)
        for order_number in order_numbers
    ]
    create_shipping_items_job_group = await client.create_shipping_items(requests)
    await create_shipping_items_job_group.wait_until_completed()
    successful_orders = []
    failed_orders = []
    for job in create_shipping_items_job_group.jobs:
        payload = await job.payload
        if 200 <= job.status_code < 300:
            successful_orders.append(payload["order_number"])
        else:
            failed_orders.append(payload["order_number"])
    return successful_orders, failed_orders


async def main(orders: list):
    # Save orders to DynamoDB
    successful_orders, failed_orders = await create_orders(orders)
    if not successful_orders:
        logger.info("No successful orders to process.")
        return
    logger.info("Successfully created orders: %s", successful_orders)
    logger.info("Failed to create orders: %s", failed_orders)
    # Create shipping items
    successful_orders, failed_orders = await create_shipping_items(successful_orders)
    if not successful_orders:
        logger.info("No successful orders to process.")
        return
    logger.info("Successfully created shipping items: %s", successful_orders)
    logger.info("Failed to create shipping items: %s", failed_orders)
    logger.info("All jobs completed.")


if __name__ == "__main__":
    # NOTE:
    # required environment variables
    # - DAAS_GATEWAY_USERNAME
    # - DAAS_GATEWAY_PASSWORD
    # - DAAS_GATEWAY_CLIENT_ID
    orders_data = [
        {
            # order data here
        }
    ]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(orders_data))
