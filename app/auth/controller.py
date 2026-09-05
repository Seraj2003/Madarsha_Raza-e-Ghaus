from app.auth.schemas import LoginRequest, UserResponse, MeResponse,RegisterRequest, LoginResponse
from fastapi import FastAPI, Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Donors
from app.uttils.security import hash_password,verify_password, create_access_token
from app.dependencies.auth  import get_current_donor
def get_register(body: RegisterRequest, db: Session):
    email = body.email.lower().strip()
    mobile = body.mobile.strip()
    exsisting_email = (db.query(Donors).filter(Donors.email == email).first())
    exsisting_mobile = (db.query(Donors).filter(Donors.mobile == mobile).first())
    if (exsisting_email):
        raise HTTPException(

            status_code=status.HTTP_409_CONFLICT,
            detail="Email Already Registered"
        )
    if (exsisting_mobile):
            raise HTTPException(
    
                status_code=status.HTTP_409_CONFLICT,
                detail="Mobile Number Already Registered"
            )
    donor = Donors(
            name = body.name.strip(),
            mobile = body.mobile,
            address = body.address,
            password = hash_password(body.password),
            monthly_amount = body.monthly_amount,
            is_active = True,
            is_verified =False
    )
    db.add(donor)
    db.commit()
    db.refresh(donor)

    return {
         "message":"User  Registtered sucessfully",
         "donor_id": donor.id
}

def get_login(body: LoginRequest, db: Session):
    donor = (db.query(Donors).filter(Donors.id == body.donor_id).first())
    print(donor)
    if not donor:
         raise HTTPException(
              status_code=status.HTTP_404_NOT_FOUND,
              detail="Donor Not Register"
         )
    if not donor.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Donor account is inactive"
        )
    
    
    if not verify_password(body.password,donor.password):
         raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              detail="Invalid Password"
         )
    token = create_access_token(donor_id=donor.id)
    print(donor)
    return LoginResponse(
         message="Login Successfully",
         access_token=token,
         token_type="bearer",
         donor=donor
    )


    
# def get_logout(donor_id : int = Depends(get_current_donor), db: Session = Depends(get_db)):
#      db.query(RefreshToken).filter(
#         RefreshToken.donor_id == donor_id,
#         RefreshToken.revoked == False
#     ).update({
#         "revoked": True
#     })

#     db.commit()

#     return {
#         "message": "Logout successful"
#     }