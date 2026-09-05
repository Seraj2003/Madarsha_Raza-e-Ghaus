from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies.auth import get_current_donor


def get_donation (donor_id:int = Depends(get_current_donor), db: Session =  Depends(get_db)):
    pass