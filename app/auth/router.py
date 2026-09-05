from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.schemas import LoginRequest, RegisterRequest,MeResponse, UserResponse,RegisterResponse, MessageResponse,LoginResponse
from app.auth import controller
from app.dependencies.auth import get_current_donor
from app.models import Donors


auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/register",status_code=status.HTTP_200_OK,response_model=RegisterResponse)
def login(body: RegisterRequest, db: Session = Depends(get_db)):
    return controller.get_register(body,db);


@auth_router.post("/login", status_code=status.HTTP_200_OK,response_model=LoginResponse)
def register(body:LoginRequest, db: Session = Depends(get_db)):
    return controller.get_login(body,db);


@auth_router.post("/logout", status_code=status.HTTP_200_OK)
def logout(donor_id : int =  Depends(get_current_donor), db : Session =  Depends(get_db)):
    return controller.get_logout(donor_id,db)

# @auth_router.get("/me", status_code=status.HTTP_200_OK, response_model=MeResponse)
# async def register(current_donor: Donors = Depends(get_current_donor), db: Session = Depends(get_db)):
#     return await controller.get_me(current_donor,db)