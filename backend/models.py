from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, date
import uuid

class Users(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str
    role: str  # borrower | lender
    password: str 

class BorrowerProfile(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    business_name: str
    owner_name: str
    pan_number: str
    gst_number: str
    business_address: str
    contact_number: str
    bank_account_number: str
    ifsc_code: str
    created_at: datetime

class LenderProfile(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    organization_name: str
    contact_person: str
    license_number: str
    address: str
    contact_number: str
    email: str
    created_at: datetime

class Loan(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    borrower_id: uuid.UUID = Field(foreign_key="users.id")
    lender_id: uuid.UUID = Field(foreign_key="users.id")
    lender_name: str
    principal_amount: float
    interest_rate: float
    tenure_months: int
    monthly_emi: float
    outstanding_amount: float
    disbursement_date: date
    emi_date: int
    status: str
    emi_collection_percentage: float

class EMIWallet(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    borrower_id: uuid.UUID = Field(foreign_key="users.id")
    current_balance: float
    total_monthly_emi: float
    collected_this_month: float
    last_updated: datetime

class Transaction(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    borrower_id: uuid.UUID = Field(foreign_key="users.id")
    loan_id: uuid.UUID = Field(foreign_key="loan.id")
    type: str
    amount: float
    description: Optional[str]
    timestamp: datetime
    status: str
    payment_method: Optional[str]
    reference_number: Optional[str]

class EMIPayment(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    loan_id: uuid.UUID = Field(foreign_key="loan.id")
    borrower_id: uuid.UUID = Field(foreign_key="users.id")
    lender_id: uuid.UUID = Field(foreign_key="users.id")
    amount: float
    due_date: date
    status: str
