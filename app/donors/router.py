from fastapi import FastAPI,Depends,APIRouter,status
from app.models import Donors
from sqlalchemy.orm import Session
from app.dependencies.auth import get_current_donor
from app.donors.schemas import DonorDashboardResponse,DonorProfileResponse
from app.database import get_db
from app.donors import controller
donor_router = APIRouter(prefix="/donor",tags=["Donors"])

# @donor_router.get("/profile")
# async def profile(current_donor: Donors = Depends(get_current_donor)):
#      print(current_donor)
@donor_router.get("/dashboard",response_model=DonorDashboardResponse,status_code=status.HTTP_200_OK)
def dashboard(current_donor: Donors = Depends(get_current_donor),db:Session = Depends(get_db)):
     return controller.get_dashboard(current_donor,db)

@donor_router.get("/profile",status_code=status.HTTP_200_OK )
def profile(current_donor : Donors = Depends(get_current_donor), db: Session = Depends(get_db)):
     return controller.get_profile(current_donor,db)


