
from fastapi  import Depends,status,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from app.database import get_db
from app.dependencies.auth import get_current_donor
from app.models import Donors,Donations,Expenses
from datetime import datetime
from app.donors.schemas import DonorDashboardResponse,DonorProfileResponse
from decimal import Decimal


def get_profile(donor: Session=Depends(get_current_donor), db: Session = Depends(get_db)):
    
    # print(donor)
    donor = (db.query(Donors).filter(Donors.id == donor).first())
    # return {
    #     donor
    # }
    if donor is None:
        raise HTTPException(
            status_code=404,
            detail="Donor not found"
        )
    return DonorProfileResponse (
        id = donor.id,
        name = donor.name,
        email = donor.email,
        phone = donor.mobile,
        monthly_amount = donor.monthly_amount,
        created_at = donor.created_at,
        
    )


def get_dashboard(
    donor_id: int = Depends(get_current_donor),
    db: Session = Depends(get_db)
):

    # --------------------------------------------------
    # 1. Get donor
    # --------------------------------------------------

    donor = (
        db.query(Donors)
        .filter(Donors.id == donor_id)
        .first()
    )

    if donor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donor not found"
        )

    now = datetime.now()

    # --------------------------------------------------
    # 2. Current month donation
    # --------------------------------------------------

    paid_amount = (
        db.query(
            func.coalesce(
                func.sum(Donations.amount),
                Decimal("0")
            )
        )
        .filter(
            Donations.donor_id == donor_id,
            Donations.donation_month == now.month,
            Donations.donation_year == now.year
        )
        .scalar()
    )

    paid_amount = Decimal(paid_amount)

    monthly_amount = Decimal(donor.monthly_amount)

    due_amount = max(
        monthly_amount - paid_amount,
        Decimal("0")
    )

    # --------------------------------------------------
    # 3. Payment status
    # --------------------------------------------------

    if paid_amount >= monthly_amount:
        payment_status = "paid"

    elif paid_amount > Decimal("0"):
        payment_status = "partial"

    else:
        payment_status = "pending"

    # --------------------------------------------------
    # 4. Donor summary
    # --------------------------------------------------

    start_date = donor.created_at

    months_elapsed = (
        (now.year - start_date.year) * 12
        + (now.month - start_date.month)
        + 1
    )

    months_elapsed = max(months_elapsed, 0)

    # Total amount donated
    total_donated = (
        db.query(
            func.coalesce(
                func.sum(Donations.amount),
                Decimal("0")
            )
        )
        .filter(
            Donations.donor_id == donor_id
        )
        .scalar()
    )

    total_donated = Decimal(total_donated)

    # Number of months in which donor made a donation
    paid_months = (
        db.query(
            Donations.donation_year,
            Donations.donation_month
        )
        .filter(
            Donations.donor_id == donor_id,
            Donations.amount > 0
        )
        .distinct()
        .count()
    )

    pending_months = max(
        months_elapsed - paid_months,
        0
    )

    # --------------------------------------------------
    # 5. Madarsa monthly collection
    # --------------------------------------------------

    monthly_collection_amount = (
        db.query(
            func.coalesce(
                func.sum(Donations.amount),
                Decimal("0")
            )
        )
        .filter(
            Donations.donation_month == now.month,
            Donations.donation_year == now.year
        )
        .scalar()
    )

    monthly_collection_amount = Decimal(
        monthly_collection_amount
    )

    # --------------------------------------------------
    # 6. Madarsa yearly collection
    # --------------------------------------------------

    yearly_collection_amount = (
        db.query(
            func.coalesce(
                func.sum(Donations.amount),
                Decimal("0")
            )
        )
        .filter(
            Donations.donation_year == now.year
        )
        .scalar()
    )

    yearly_collection_amount = Decimal(
        yearly_collection_amount
    )

    # --------------------------------------------------
    # 7. Monthly expenses
    # --------------------------------------------------

    monthly_expenses = (
        db.query(
            func.coalesce(
                func.sum(Expenses.amount),
                Decimal("0")
            )
        )
        .filter(
            extract(
                "month",
                Expenses.expense_date
            ) == now.month,

            extract(
                "year",
                Expenses.expense_date
            ) == now.year
        )
        .scalar()
    )

    monthly_expenses = Decimal(monthly_expenses)

    # --------------------------------------------------
    # 8. Yearly expenses
    # --------------------------------------------------

    yearly_expenses = (
        db.query(
            func.coalesce(
                func.sum(Expenses.amount),
                Decimal("0")
            )
        )
        .filter(
            extract(
                "year",
                Expenses.expense_date
            ) == now.year
        )
        .scalar()
    )

    yearly_expenses = Decimal(yearly_expenses)

    # --------------------------------------------------
    # 9. Balance
    # --------------------------------------------------

    balance = (
        yearly_collection_amount
        - yearly_expenses
    )

    # --------------------------------------------------
    # 10. Response
    # --------------------------------------------------

    return DonorDashboardResponse(

        donor={
            "donor_id": donor.id,
            "name": donor.name
        },

        current_month={
            "month": now.month,
            "year": now.year,
            "monthly_amount": monthly_amount,
            "due_amount": due_amount,
            "paid_amount": paid_amount,
            "status": payment_status
        },

        summary={
            "total_donated": total_donated,
            "total_paid_month": paid_months,
            "pending_month": pending_months
        },

        madarsha_history={
            "monthly_collection": monthly_collection_amount,
            "yearly_collection": yearly_collection_amount,
            "monthly_expensess": monthly_expenses,
            "yearly_expensess": yearly_expenses,
            "blance": balance
        }
    )