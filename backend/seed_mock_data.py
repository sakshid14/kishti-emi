from sqlmodel import Session, SQLModel, create_engine
from datetime import datetime, timedelta, date
import uuid

from models import Users, BorrowerProfile, LenderProfile, Loan, EMIWallet, Transaction, EMIPayment

DATABASE_URL = "postgresql+psycopg2://reconrebels_1:Loknath%404044@recons.postgres.database.azure.com/postgres"
engine = create_engine(DATABASE_URL)

def create_mock_data():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Create Users
        borrower_id = uuid.uuid4()
        lender_id = uuid.uuid4()

        borrower = Users(
            id=borrower_id,
            email="barber@example.com",
            role="borrower",
            password="barber123"
        )
        lender = Users(
            id=lender_id,
            email="finbank@example.com",
            role="lender",
            password="finbank123"
        )

        session.add_all([borrower, lender])
        session.commit()

        # BorrowerProfile and LenderProfile
        borrower_profile = BorrowerProfile(
            user_id=borrower_id,
            business_name="Elegant Cuts",
            owner_name="Ravi Mehra",
            pan_number="ABCDE1234F",
            gst_number="27ABCDE1234F1Z5",
            business_address="102 Salon Street, Pune",
            contact_number="9876543210",
            bank_account_number="111122223333",
            ifsc_code="HDFC0001234",
            created_at=datetime.now()
        )

        lender_profile = LenderProfile(
            user_id=lender_id,
            organization_name="FinBank Capital",
            contact_person="Priya Singh",
            license_number="LIC123456789",
            address="5 MG Road, Mumbai",
            contact_number="9988776655",
            email="contact@finbank.com",
            created_at=datetime.now()
        )

        session.add_all([borrower_profile, lender_profile])
        session.commit()

        # Loan
        loan = Loan(
            borrower_id=borrower_id,
            lender_id=lender_id,
            lender_name="FinBank Capital",
            principal_amount=100000.0,
            interest_rate=12.5,
            tenure_months=12,
            monthly_emi=9000.0,
            outstanding_amount=90000.0,
            disbursement_date=date(2025, 1, 1),
            emi_date=5,
            status="active",
            emi_collection_percentage=0.1
        )

        session.add(loan)
        session.commit()

        # EMI Wallet
        emi_wallet = EMIWallet(
            borrower_id=borrower_id,
            current_balance=3000.0,
            total_monthly_emi=9000.0,
            collected_this_month=3000.0,
            last_updated=datetime.now()
        )

        session.add(emi_wallet)
        session.commit()

        # Transactions
        transaction1 = Transaction(
            borrower_id=borrower_id,
            loan_id=loan.id,
            type="credit",
            amount=1000.0,
            description="Haircut payment",
            timestamp=datetime.now(),
            status="blocked",
            payment_method="UPI",
            reference_number="TXN001"
        )

        transaction2 = Transaction(
            borrower_id=borrower_id,
            loan_id=loan.id,
            type="credit",
            amount=2000.0,
            description="Salon product sale",
            timestamp=datetime.now(),
            status="blocked",
            payment_method="Card",
            reference_number="TXN002"
        )

        session.add_all([transaction1, transaction2])
        session.commit()

        # EMI Payment
        emi_payment = EMIPayment(
            loan_id=loan.id,
            borrower_id=borrower_id,
            lender_id=lender_id,
            amount=9000.0,
            due_date=date(2025, 2, 5),
            status="pending"
        )

        session.add(emi_payment)
        session.commit()

        print("✅ Mock data inserted successfully!")

if __name__ == "__main__":
    create_mock_data()