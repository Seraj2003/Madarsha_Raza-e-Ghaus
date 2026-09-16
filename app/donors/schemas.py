from pydantic import BaseModel, ConfigDict
from typing import List
from decimal import Decimal
from datetime import datetime
class DonorDashboardInfo(BaseModel):
    donor_id : int
    name: str
    model_config= ConfigDict(from_attributes=True)

class CurrentMonthDonation(BaseModel):
    month: int
    year:int
    due_amount:float
    monthly_amount:float
    paid_amount:float
    status:str

class DonorSummary(BaseModel):
    total_donated:float
    total_paid_month:int
    pending_month:int
class MadarshaSummary(BaseModel):
    monthly_collection:float
    yearly_collection: float
    monthly_expensess:float
    yearly_expensess:float
    blance:float

class DonorDashboardResponse(BaseModel):
    donor:DonorDashboardInfo
    current_month:CurrentMonthDonation
    summary:DonorSummary
    madarsha_history:MadarshaSummary     

class DonorProfileResponse(BaseModel):
    id: int
    name: str
    email: str | None = None
    phone: str | None = None
    monthly_amount: Decimal
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReceiptData(BaseModel):
    receipt_number: str
    generated_at: datetime
    status: str

    cancellation_reason: str | None = None
    cancelled_at: datetime | None = None


class DonorData(BaseModel):
    id: int
    name: str
    mobile: str | None = None
    address: str | None = None


class DonationData(BaseModel):
    amount: Decimal
    donation_type: str
    month: int | None = None
    year: int | None = None


class PaymentData(BaseModel):
    payment_id: str | None = None
    status: str | None = None


class ReceiptResponse(BaseModel):
    message: str

    receipt: ReceiptData
    donor: DonorData
    donation: DonationData
    payment: PaymentData