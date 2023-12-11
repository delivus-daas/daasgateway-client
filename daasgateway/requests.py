from typing import Optional, List

from pydantic import BaseModel, Field


class Product(BaseModel):
    name: str = Field(max_length=128, strip_whitespace=True)
    product_no: Optional[str] = Field(
        default=None, max_length=64, strip_whitespace=True
    )
    metadata: Optional[dict] = Field(default=None)
    total_amount: Optional[int] = Field(default=None, ge=0)


class OrderItem(BaseModel):
    order_item_number: Optional[str] = Field(default=None, max_length=64)
    quantity: Optional[int] = Field(default=None, ge=1)
    options: Optional[str] = Field(default=None, max_length=128)
    product: Product
    total_amount: Optional[int] = Field(default=None, ge=0)
    metadata: Optional[dict] = Field(default=None)


class ShopAddress(BaseModel):
    name: str = Field(max_length=128, strip_whitespace=True)
    mobile_tel: str = Field(max_length=24, strip_whitespace=True)
    address1: str = Field(max_length=128, strip_whitespace=True)
    address2: str = Field(default="", strip_whitespace=True)
    zipcode: str = Field(min_length=5, max_length=5, strip_whitespace=True)


class CreateOrderRequest(BaseModel):
    order_number: str = Field(max_length=64, strip_whitespace=True)
    shipping_memo: Optional[str] = Field(
        default=None, max_length=128, strip_whitespace=True
    )
    orderer_name: Optional[str] = Field(
        default=None, max_length=64, strip_whitespace=True
    )
    orderer_mobile_tel: Optional[str] = Field(
        default=None, max_length=24, strip_whitespace=True
    )
    receiver_name: str = Field(max_length=64, strip_whitespace=True)
    receiver_mobile_tel: str = Field(max_length=24, strip_whitespace=True)
    receiver_address1: str = Field(max_length=64, strip_whitespace=True)
    receiver_address2: str = Field(default="", max_length=128, strip_whitespace=True)
    receiver_postcode: str = Field(min_length=5, max_length=5, strip_whitespace=True)
    order_items: List[OrderItem] = Field(default_factory=list, min_length=1)


class CreateShippingItemRequest(BaseModel):
    order_number: str = Field(max_length=64, strip_whitespace=True)
    shop_address_id: Optional[int] = Field(default=None, ge=1)
    shop_address: Optional[ShopAddress] = Field(default=None)
    address_return: Optional[ShopAddress] = Field(default=None)
    entrance_password: Optional[str] = Field(
        default=None, max_length=128, strip_whitespace=True
    )
    designated_tracking_number: Optional[str] = Field(
        default=None, min_length=10, strip_whitespace=True
    )
