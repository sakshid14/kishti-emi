from sqlmodel import Session
from db import engine
from models import User, BorrowerProfile, LenderProfile, Loan, EMIWallet, Transaction, EMIPayment
import uuid
from datetime import datetime, date

def insert_mock_data():
    with Session(engine) as session:
        # Users
        user1 = User(id=uuid.UUID("00000000-0000-0000-0000-000000000001"), email="rajesh@techsolutions.com", role="borrower")
        user2 = User(id=uuid.UUID("00000000-0000-0000-0000-000000000002"), email="priya@manufacturing.com", role="borrower")
        user3 = User(id=uuid.UUID("00000000-0000-0000-0000-000000000003"), email="contact@quickfinance.com", role="lender")

        session.add_all([user1, user2, user3])
        
        # Borrower Profiles
        profile1 = BorrowerProfile(
            id=uuid.uuid4(), user_id=user1.id, business_name="Tech Solutions Pvt Ltd", owner_name="Rajesh Kumar",
            pan_number="ABCDE1234F", gst_number="27ABCDE1234F1Z5",
            business_address="123 Tech Park, Bangalore", contact_number="+91-9876543210",
            bank_account_number="1234567890", ifsc_code="HDFC0001234", created_at=datetime.fromisoformat("2024-01-15T00:00:00")
        )
        profile2 = BorrowerProfile(
            id=uuid.uuid4(), user_id=user2.id, business_name="Priya Manufacturing", owner_name="Priya Sharma",
            pan_number="FGHIJ5678K", gst_number="19FGHIJ5678K2M9",
            business_address="456 Industrial Area, Pune", contact_number="+91-9876543211",
            bank_account_number="0987654321", ifsc_code="ICICI0005678", created_at=datetime.fromisoformat("2024-02-01T00:00:00")
        )

        lender_profile = LenderProfile(
            id=uuid.uuid4(), user_id=user3.id, organization_name="Quick Finance Ltd",
            contact_person="Amit Verma", license_number="NBFC-2024-001",
            address="789 Financial District, Mumbai", contact_number="+91-9876543212",
            email="contact@quickfinance.com", created_at=datetime.fromisoformat("2024-01-01T00:00:00")
        )

        session.add_all([profile1, profile2, lender_profile])

        # Loans
        loan1 = Loan(id=uuid.UUID("00000000-0000-0000-0000-000000000011"), borrower_id=user1.id, lender_id=user3.id, lender_name="Quick Finance Ltd",
            principal_amount=500000, interest_rate=12, tenure_months=24, monthly_emi=23539,
            outstanding_amount=376312, disbursement_date=date.fromisoformat("2024-01-15"), emi_date=15,
            status="active", emi_collection_percentage=25)

        loan2 = Loan(id=uuid.UUID("00000000-0000-0000-0000-000000000012"), borrower_id=user1.id, lender_id=user3.id, lender_name="Quick Finance Ltd",
            principal_amount=300000, interest_rate=10, tenure_months=36, monthly_emi=9676,
            outstanding_amount=290000, disbursement_date=date.fromisoformat("2024-03-01"), emi_date=1,
            status="active", emi_collection_percentage=15)

        loan3 = Loan(id=uuid.UUID("00000000-0000-0000-0000-000000000013"), borrower_id=user2.id, lender_id=user3.id, lender_name="Quick Finance Ltd",
            principal_amount=750000, interest_rate=14, tenure_months=18, monthly_emi=46875,
            outstanding_amount=625000, disbursement_date=date.fromisoformat("2024-02-01"), emi_date=5,
            status="active", emi_collection_percentage=30)

        session.add_all([loan1, loan2, loan3])

        # EMI Wallets
        wallet1 = EMIWallet(id=uuid.uuid4(), borrower_id=user1.id, current_balance=28500,
                            total_monthly_emi=33215, collected_this_month=28500,
                            last_updated=datetime.fromisoformat("2025-01-07T10:30:00"))

        wallet2 = EMIWallet(id=uuid.uuid4(), borrower_id=user2.id, current_balance=35000,
                            total_monthly_emi=46875, collected_this_month=35000,
                            last_updated=datetime.fromisoformat("2025-01-07T14:20:00"))

        session.add_all([wallet1, wallet2])

        # Transactions
        tx1 = Transaction(id=uuid.uuid4(), borrower_id=user1.id, loan_id=loan1.id, type="incoming_payment",
                          amount=50000, description="Payment from ABC Corp",
                          timestamp=datetime.fromisoformat("2025-01-07T09:00:00"), status="completed",
                          payment_method="Bank Transfer", reference_number="TXN123456789")

        tx2 = Transaction(id=uuid.uuid4(), borrower_id=user1.id, loan_id=loan1.id, type="emi_blocked",
                          amount=12500, description="EMI blocked (25%)",
                          timestamp=datetime.fromisoformat("2025-01-07T09:05:00"), status="completed")

        tx3 = Transaction(id=uuid.uuid4(), borrower_id=user1.id, loan_id=loan2.id, type="emi_blocked",
                          amount=7500, description="EMI blocked (15%)",
                          timestamp=datetime.fromisoformat("2025-01-07T09:05:00"), status="completed")

        tx4 = Transaction(id=uuid.uuid4(), borrower_id=user1.id, loan_id=loan1.id, type="emi_paid",
                          amount=23539, description="EMI paid to Quick Finance",
                          timestamp=datetime.fromisoformat("2024-12-15T00:00:00"), status="completed")

        session.add_all([tx1, tx2, tx3, tx4])

        # EMI Payments
        emi1 = EMIPayment(id=uuid.uuid4(), loan_id=loan1.id, borrower_id=user1.id, lender_id=user3.id,
                          amount=23539, due_date=date.fromisoformat("2025-01-15"), status="scheduled")

        emi2 = EMIPayment(id=uuid.uuid4(), loan_id=loan2.id, borrower_id=user1.id, lender_id=user3.id,
                          amount=9676, due_date=date.fromisoformat("2025-01-01"), status="scheduled")

        emi3 = EMIPayment(id=uuid.uuid4(), loan_id=loan3.id, borrower_id=user2.id, lender_id=user3.id,
                          amount=46875, due_date=date.fromisoformat("2025-01-05"), status="scheduled")

        session.add_all([emi1, emi2, emi3])

        session.commit()
        print("✅ Mock data inserted successfully.")

if __name__ == "__main__":
    insert_mock_data()
