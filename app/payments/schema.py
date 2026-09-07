from decimal import Decimal
from pydantic import BaseModel
from app.models import DonationType

class PaymentCreate(BaseModel):
    amount: Decimal
    donation_type:DonationType


class PaymentOrderResponse(BaseModel):
    payment_id: int
    provider: str
    provider_order_id: str
    amount: Decimal
    currency: str
    status: str


class PaymentVerifyRequest(BaseModel):
    provider_order_id: str
    provider_payment_id: str
    signature: str


class PaymentSuccessResponse(BaseModel):
    message: str
    payment_id: str
    donation_id: int
    receipt_id: str
    receipt_number: str