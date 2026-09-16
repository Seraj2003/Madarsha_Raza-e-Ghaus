from app.payments.schema import (
    PaymentCreate,
    PaymentOrderResponse,
    PaymentVerifyRequest,
    PaymentSuccessResponse
)

from fastapi import Depends, HTTPException
from app.dependencies.auth import get_current_donor
from app.database import get_db
from sqlalchemy.orm import Session
import uuid

from app.payments.services import RazorpayGateway
from app.models import Payments
from app.donations.services import create_donation, create_receipt


def get_payment_order(
    body: PaymentCreate,
    current_donor: int = Depends(get_current_donor),
    db: Session = Depends(get_db)
):
    donor_id = current_donor

    if body.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amount must be greater than zero"
        )

    gateway = RazorpayGateway()

    payment_reference = f"DON-{donor_id}-{uuid.uuid4().hex[:8]}"

    order = gateway.create_order(
        body.amount,
        receipt=payment_reference
    )

    payment = Payments(
        donor_id=donor_id,
        provider="razorpay",
        order_id=order["id"],
        donation_type=body.donation_type, 
        amount=body.amount,
        payment_method="Online",
        currency="INR",
        status="pending"
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return PaymentOrderResponse(
        payment_id=payment.id,
        provider=payment.provider,
        provider_order_id=payment.order_id,
        amount=payment.amount,
        currency=payment.currency,
        status=payment.status
    )


def get_verify_order(
    body: PaymentVerifyRequest,
    current_donor: int = Depends(get_current_donor),
    db: Session = Depends(get_db)
):
    donor_id = current_donor

    # --------------------------------
    # 1. Find payment order
    # --------------------------------

    payment = (
        db.query(Payments)
        .filter(
            Payments.donor_id == donor_id,
            Payments.order_id == body.provider_order_id
        )
        .first()
    )

    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="Payment order not found"
        )

    # --------------------------------
    # 2. Already successful
    # --------------------------------

    if payment.status == "success":
        return PaymentSuccessResponse(
            message="Payment already successful",
            payment_id=payment.id,
            donation_id=None,
            receipt_number=None
        )

    # --------------------------------
    # 3. Verify Razorpay signature
    # --------------------------------

    gateway = RazorpayGateway()

    try:

       gateway.verify_payment(
          order_id=body.provider_order_id,
          payment_id=body.provider_payment_id,
          signature=body.signature
        )  

    except Exception as error:

        payment.status = "failed"
        db.commit()

        raise HTTPException(
            status_code=400,
            detail="Payment verification failed"
        )

    # --------------------------------
    # 4. Payment verified
    # --------------------------------

    try:

        # IMPORTANT:
        # This is Razorpay payment ID
        payment.payment_id = body.provider_payment_id

        payment.status = "success"
        payment.signature_verified = True


        # --------------------------------
        # 5. Create donation
        # ----- ---------------------------
        print(payment.donation_type)
        donation = create_donation(
            payment=payment,
            db=db
        )
        # --------------------------------
        # 6. Create receipt
        # --------------------------------

        receipt = create_receipt(
            donation=donation,
            db=db
        )

        # --------------------------------
        # 7. Commit everything
        # --------------------------------

        db.commit()

        return PaymentSuccessResponse(
           message="Payment successful",
           payment_id=payment.id,
           donation_id=donation.id,
           receipt_number=receipt.receipt_number
        )
 
    except Exception as e:
        print(type(e).__name__)

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Payment succeeded but donation processing failed"
        )