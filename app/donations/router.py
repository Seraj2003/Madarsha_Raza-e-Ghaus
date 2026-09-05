from fastapi import FastAPI,status,APIRouter,Depends
from app.database import get_db
from app.dependencies.auth import get_current_donor
from sqlalchemy.orm import Session
from app.donations import controller


donation_router = APIRouter(prefix="/donation",tags=["donation"])


@donation_router.get("/my-donation",status_code=status.HTTP_200_OK)
def donation(donor_id : int = Depends(get_current_donor), db:Session = Depends(get_db)):
    return controller.get_donation(donor_id,db)

@donation_router.post("/donate",status_code=status.HTTP_201_CREATED)
def donate():
    pass