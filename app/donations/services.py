from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models import Donations, Receipts


def generate_receipt_number(db: Session) -> str:
    number = db.execute(
        text("SELECT nextval('receipt_number_seq')")
    ).scalar_one()

    year = datetime.now().year

    return f"MRE{year}{number:06d}"


def create_donation(
    payment,
    db: Session
):
    # Prevent duplicate donation
    existing_donation = (
        db.query(Donations)
        .filter(
            Donations.payment_id == payment.id
        )
        .first()
    )

    if existing_donation:
        return existing_donation

    now = datetime.now()

    donation = Donations(
    donor_id=payment.donor_id,
    type=payment.donation_type,       # currently None
    amount=payment.amount,
    payment_mode="UPI",            # currently None
    donation_month=now.month,
    donation_year=now.year,
    transaction_reference=payment.payment_id,
    payment_id=payment.id,
    )

    db.add(donation)

    # Generate donation.id
    db.flush()

    return donation


def create_receipt(
    donation,
    db: Session
):
    # Prevent duplicate receipt
    existing_receipt = (
        db.query(Receipts)
        .filter(
            Receipts.donation_id == donation.id
        )
        .first()
    )

    if existing_receipt:
        return existing_receipt

    receipt = Receipts(
        donation_id=donation.id,
        amount=donation.amount,
        receipt_number=generate_receipt_number(db),
        status="issued"
    )

    db.add(receipt)

    db.flush()

    return receipt