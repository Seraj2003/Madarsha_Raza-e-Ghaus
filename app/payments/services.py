import razorpay
from app.config import settings
from app.models import Donations,Receipts
from datetime import datetime
class RazorpayGateway:

    def __init__(self):
        self.client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            )
        )

    def create_order(self, amount, receipt):
        amount_paise = int(amount * 100)

        order = self.client.order.create({
            "amount": amount_paise,
            "currency": "INR",
            "receipt": receipt,
        })

        return order

    def verify_payment(
        self,
        order_id,
        payment_id,
        signature
    ):
        self.client.utility.verify_payment_signature({
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature,
        })

        return True
    