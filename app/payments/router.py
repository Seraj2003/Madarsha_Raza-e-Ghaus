from fastapi import FastAPI,APIRouter,status,Depends
from sqlalchemy.orm import Session
from app.dependencies.auth import get_current_donor
from app.database import get_db
from app.payments.schema import PaymentOrderResponse,PaymentCreate,PaymentVerifyRequest
from app.payments import controller
payment_router = APIRouter(prefix="/donor/donation/payment",tags=["payment"])


@payment_router.post("/order", response_model=PaymentOrderResponse,status_code=status.HTTP_201_CREATED)
def create_order(body: PaymentCreate, current_donor : int = Depends(get_current_donor), db: Session = Depends(get_db)):
    return controller.get_payment_order(body,current_donor,db)

@payment_router.post("/verify",status_code= status.HTTP_202_ACCEPTED)
def verify_order(body:PaymentVerifyRequest, current_donor: int =Depends(get_current_donor), db: Session =  Depends(get_db)):
    return controller.get_verify_order (body,current_donor,db)