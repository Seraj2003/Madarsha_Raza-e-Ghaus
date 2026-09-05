from typing import Optional
import datetime
import decimal
import enum

from sqlalchemy import BigInteger, Boolean, CheckConstraint, Date, DateTime, Enum, ForeignKeyConstraint, Integer, Numeric, PrimaryKeyConstraint, String, Text, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class DonationType(str, enum.Enum):
    ZAKAT = 'Zakat'
    SADAQAH = 'Sadaqah'
    FITRA = 'Fitra'
    BUILDING_FUND = 'Building Fund'
    GENERAL_DONATION = 'General Donation'
    MONTHLY = 'Monthly'


class PaymentMethod(str, enum.Enum):
    UPI = 'UPI'
    CASH = 'CASH'
    BANK_TRANSFER = 'BANK TRANSFER'


class UserRole(str, enum.Enum):
    COLLECTOR = 'collector'
    ADMIN = 'admin'
    USER = 'user'


class Donors(Base):
    __tablename__ = 'donors'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='donors_pkey'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('true'))
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    monthly_amount: Mapped[decimal.Decimal] = mapped_column(Numeric(100, 2), nullable=False, server_default=text('0'))
    mobile: Mapped[Optional[str]] = mapped_column(String(15))
    email: Mapped[Optional[str]] = mapped_column(String(150))
    address: Mapped[Optional[str]] = mapped_column(Text)
    village: Mapped[Optional[str]] = mapped_column(String(100))
    district: Mapped[Optional[str]] = mapped_column(String(100))
    state: Mapped[Optional[str]] = mapped_column(String(100))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    password: Mapped[Optional[str]] = mapped_column(String(255))

    payments: Mapped[list['Payments']] = relationship('Payments', back_populates='donor')
    donations: Mapped[list['Donations']] = relationship('Donations', back_populates='donor')


class ExpenseCategories(Base):
    __tablename__ = 'expense_categories'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='expense_categories_pkey'),
        UniqueConstraint('name', name='expense_categories_name_key')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    expenses: Mapped[list['Expenses']] = relationship('Expenses', back_populates='category')


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
        UniqueConstraint('email', name='users_email_key'),
        UniqueConstraint('mobile', name='users_mobile_key')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(100))
    mobile: Mapped[Optional[str]] = mapped_column(String(15))
    role: Mapped[Optional[UserRole]] = mapped_column(Enum(UserRole, values_callable=lambda cls: [member.value for member in cls], name='user_role'), server_default=text("'user'::user_role"))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    password: Mapped[Optional[str]] = mapped_column(String(255))

    expenses: Mapped[list['Expenses']] = relationship('Expenses', back_populates='users')
    donations: Mapped[list['Donations']] = relationship('Donations', back_populates='users')


class Expenses(Base):
    __tablename__ = 'expenses'
    __table_args__ = (
        ForeignKeyConstraint(['category_id'], ['expense_categories.id'], name='expenses_category_id_fkey'),
        ForeignKeyConstraint(['created_by'], ['users.id'], name='expenses_created_by_fkey'),
        PrimaryKeyConstraint('id', name='expenses_pkey')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    amount: Mapped[decimal.Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    expense_date: Mapped[Optional[datetime.date]] = mapped_column(Date, server_default=text('CURRENT_DATE'))
    created_by: Mapped[Optional[int]] = mapped_column(BigInteger)

    category: Mapped['ExpenseCategories'] = relationship('ExpenseCategories', back_populates='expenses')
    users: Mapped[Optional['Users']] = relationship('Users', back_populates='expenses')


class Payments(Base):
    __tablename__ = 'payments'
    __table_args__ = (
        CheckConstraint('amount > 0::numeric', name='chk_payment_amount'),
        CheckConstraint("status::text = ANY (ARRAY['pending'::character varying, 'success'::character varying, 'failed'::character varying, 'refunded'::character varying]::text[])", name='chk_payment_status'),
        ForeignKeyConstraint(['donor_id'], ['donors.id'], name='fk_payments_donor'),
        PrimaryKeyConstraint('id', name='payments_pkey'),
        UniqueConstraint('order_id', name='payments_order_id_key'),
        UniqueConstraint('payment_id', name='payments_payment_id_key')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    donor_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    provider: Mapped[str] = mapped_column(String(50), nullable=False, server_default=text("'razorpay'::character varying"))
    order_id: Mapped[str] = mapped_column(String(100), nullable=False)
    amount: Mapped[decimal.Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, server_default=text("'INR'::character varying"))
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'pending'::character varying"))
    signature_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    payment_id: Mapped[Optional[str]] = mapped_column(String(100))
    payment_method: Mapped[Optional[str]] = mapped_column(String(50))

    donor: Mapped['Donors'] = relationship('Donors', back_populates='payments')
    donations: Mapped[Optional['Donations']] = relationship('Donations', uselist=False, back_populates='payment')


class Donations(Base):
    __tablename__ = 'donations'
    __table_args__ = (
        CheckConstraint('amount > 0::numeric', name='donations_amount_check'),
        CheckConstraint('donation_month >= 1 AND donation_month <= 12', name='chk_donation_month'),
        CheckConstraint('donation_year >= 2000', name='chk_donation_year'),
        ForeignKeyConstraint(['collected_by'], ['users.id'], ondelete='RESTRICT', name='fk_collector'),
        ForeignKeyConstraint(['donor_id'], ['donors.id'], ondelete='RESTRICT', name='fk_donor'),
        ForeignKeyConstraint(['payment_id'], ['payments.id'], name='fk_donations_payment'),
        PrimaryKeyConstraint('id', name='donations_pkey'),
        UniqueConstraint('donor_id', 'donation_month', 'donation_year', name='uq_donor_month_year'),
        UniqueConstraint('payment_id', name='uq_donations_payment')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    donor_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    type: Mapped[DonationType] = mapped_column(Enum(DonationType, values_callable=lambda cls: [member.value for member in cls], name='donation_type'), nullable=False)
    amount: Mapped[decimal.Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    payment_mode: Mapped[PaymentMethod] = mapped_column(Enum(PaymentMethod, values_callable=lambda cls: [member.value for member in cls], name='payment_method'), nullable=False)
    donation_month: Mapped[int] = mapped_column(Integer, nullable=False)
    donation_year: Mapped[int] = mapped_column(Integer, nullable=False)
    transaction_reference: Mapped[Optional[str]] = mapped_column(String(100))
    collected_by: Mapped[Optional[int]] = mapped_column(BigInteger)
    donation_date: Mapped[Optional[datetime.date]] = mapped_column(Date, server_default=text('CURRENT_DATE'))
    remarks: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    payment_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    users: Mapped[Optional['Users']] = relationship('Users', back_populates='donations')
    donor: Mapped['Donors'] = relationship('Donors', back_populates='donations')
    payment: Mapped[Optional['Payments']] = relationship('Payments', back_populates='donations')
    receipts: Mapped['Receipts'] = relationship('Receipts', uselist=False, back_populates='donation')


class Receipts(Base):
    __tablename__ = 'receipts'
    __table_args__ = (
        ForeignKeyConstraint(['donation_id'], ['donations.id'], name='receipts_donation_id_fkey'),
        PrimaryKeyConstraint('id', name='receipts_pkey'),
        UniqueConstraint('donation_id', name='receipts_donation_id_key'),
        UniqueConstraint('receipt_number', name='receipts_receipt_number_key')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    donation_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    receipt_number: Mapped[str] = mapped_column(String(50), nullable=False)
    issued_date: Mapped[Optional[datetime.date]] = mapped_column(Date, server_default=text('CURRENT_DATE'))

    donation: Mapped['Donations'] = relationship('Donations', back_populates='receipts')
