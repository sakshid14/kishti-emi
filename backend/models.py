from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, date
# from pydantic import BaseModel
import uuid

# class ProductDataInput:
#     product_category: str
#     cost_price: float
#     base_selling_price: float
#     season: str  # e.g., 'Summer', 'Winter', 'Autumn', 'Spring', 'Festival', 'Monsoon'
#     market_demand: str  # e.g., 'High', 'Medium', 'Low'
#     marketing_spend_per_unit: float
#     operational_cost_per_unit: float
#     discount_percentage: float
#     competitor_price: float
#     transaction_date: date
#     actual_selling_price: float
#     gross_profit_per_unit: float
#     profit_percentage: float
    

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
    
class TransactionCreatePayload(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    borrower_id: uuid.UUID
    loan_id: uuid.UUID
    type: str
    amount: float
    description: Optional[str]
    status: str
    payment_method: Optional[str]
    reference_number: Optional[str]
    
class DataPoint():
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    borrower_id: uuid.UUID
    loan_id: uuid.UUID
    type: str
    amount: float
    description: Optional[str]
    status: str
    payment_method: Optional[str]
    reference_number: Optional[str]
    
class ProductData(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    borrower_id: uuid.UUID = Field(foreign_key="borrowerprofile.id")  # Foreign key to BorrowerProfile

    product_category: str
    cost_price: float
    base_selling_price: float
    season: str  # 'Summer', 'Winter', 'Autumn', 'Spring', 'Festival', 'Monsoon'
    market_demand: str  # 'High', 'Medium', 'Low'
    marketing_spend_per_unit: float
    operational_cost_per_unit: float
    discount_percentage: float
    competitor_price: float
    transaction_date: date
    actual_selling_price: float
    gross_profit_per_unit: float
    profit_percentage: float

