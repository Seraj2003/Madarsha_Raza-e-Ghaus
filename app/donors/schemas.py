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
    