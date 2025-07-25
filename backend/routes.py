from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from models import  Users, BorrowerProfile, LenderProfile, Loan, EMIWallet, Transaction, EMIPayment, TransactionCreatePayload, ProductData
from db import engine
from datetime import datetime
import requests
from emi_predictor import predicted_emi

router = APIRouter()

@router.get("/users/{user_id}")
def get_user(user_id: str):
    with Session(engine) as session:
        user = session.get(Users, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

@router.get("/loans/{borrower_id}")
def get_loans(borrower_id: str):
    with Session(engine) as session:
        loans = session.exec(select(Loan).where(Loan.borrower_id == borrower_id)).all()
        return loans

@router.get("/emi-wallets/{borrower_id}")
def get_wallet(borrower_id: str):
    with Session(engine) as session:
        wallet = session.exec(select(EMIWallet).where(EMIWallet.borrower_id == borrower_id)).first()
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")
        return wallet

@router.get("/transactions/{borrower_id}")
def get_transactions(borrower_id: str):
    with Session(engine) as session:
        txns = session.exec(select(Transaction).where(Transaction.borrower_id == borrower_id)).all()
        return txns

@router.get("/emi-payments/{borrower_id}")
def get_emi_payments(borrower_id: str):
    with Session(engine) as session:
        payments = session.exec(select(EMIPayment).where(EMIPayment.borrower_id == borrower_id)).all()
        return payments

@router.post("/sign-in")
def sign_in(email: str, password: str):
    with Session(engine) as session:
    # Fetch the user by email
        statement = select(Users).where(Users.email == email)
        user = session.exec(statement).first()

        if not user or user.password != password:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        if user.role == "borrower":
            profile_stmt = select(BorrowerProfile).where(BorrowerProfile.user_id == user.id)
            profile = session.exec(profile_stmt).first()
            if not profile:
                raise HTTPException(status_code=404, detail="Borrower profile not found")
            return {
                "role": "borrower",
                "user_id": str(user.id),
                "business_name": profile.business_name,
                "owner_name": profile.owner_name
            }

        elif user.role == "lender":
            profile_stmt = select(LenderProfile).where(LenderProfile.user_id == user.id)
            profile = session.exec(profile_stmt).first()
            if not profile:
                raise HTTPException(status_code=404, detail="Lender profile not found")
            return {
                "role": "lender",
                "user_id": str(user.id),
                "organization_name": profile.organization_name,
                "contact_person": profile.contact_person
            }

        else:
            raise HTTPException(status_code=400, detail="Invalid role")
        
@router.get("/getUserDetails/{user_id}")
def get_user_details(user_id: str):
    with Session(engine) as session:
        # Fetch user
        user = session.get(Users, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.role != "borrower":
            raise HTTPException(status_code=400, detail="User is not a borrower")

        # Fetch borrower profile
        profile = session.exec(
            select(BorrowerProfile).where(BorrowerProfile.user_id == user_id)
        ).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Borrower profile not found")

        # Fetch loan(s)
        loans = session.exec(
            select(Loan).where(Loan.borrower_id == profile.user_id)
        ).all()

        # Fetch EMI wallet
        wallet = session.exec(
            select(EMIWallet).where(EMIWallet.borrower_id == profile.user_id)
        ).first()

        # Fetch transactions
        transactions = session.exec(
            select(Transaction).where(Transaction.borrower_id == profile.user_id)
        ).all()

        # Fetch EMI payments
        payments = session.exec(
            select(EMIPayment).where(EMIPayment.borrower_id == profile.user_id)
        ).all()

        return {
            "user": {
                "id": str(user.id),
                "email": user.email,
                "role": user.role,
            },
            "borrower_profile": profile,
            "loans": loans,
            "emi_wallet": wallet,
            "transactions": transactions,
            "emi_payments": payments
        }


@router.post("/transactions/create")
def create_transaction(payload: TransactionCreatePayload):
    with Session(engine) as session:
        new_txn = Transaction(
            borrower_id=payload.borrower_id,
            loan_id=payload.loan_id,
            type=payload.type,
            amount=payload.amount,
            description=payload.description,
            timestamp=datetime.utcnow(),
            status=payload.status,
            payment_method=payload.payment_method,
            reference_number=payload.reference_number
        )
        session.add(new_txn)
        session.commit()
        session.refresh(new_txn)

        return {"message": "Transaction created successfully", "transaction_id": str(new_txn.id), "amount": new_txn.amount}
    
    
PREDICT_EMI_SERVICE_URL = "http://0.0.0.0:8010/predict_emi"  # Replace with actual service URL

@router.post("/predictEMI/{borrower_id}")
def predict_and_block_emi(borrower_id: str):
    results = []
    with Session(engine) as session:
        # 1. Fetch loans for this borrower (or specific loan if loan_id provided)
        query = select(Loan).where(Loan.borrower_id == borrower_id)
        print(query)
        loans = session.exec(query).all()

        if not loans:
            raise HTTPException(status_code=404, detail="No loans found for this borrower")

        # 2. Fetch ProductData for this borrower
        product_data = session.exec(select(ProductData).where(ProductData.borrower_id == borrower_id)).first()
        if not product_data:
            raise HTTPException(status_code=404, detail="Product data not found for this borrower")

        for loan in loans:
            # 3. Prepare enriched payload (merge ProductData + loan details)
            payload = {
                "product_category": product_data.product_category,
                "cost_price": product_data.cost_price,
                "base_selling_price": product_data.base_selling_price,
                "season": product_data.season,
                "market_demand": product_data.market_demand,
                "marketing_spend_per_unit": product_data.marketing_spend_per_unit,
                "operational_cost_per_unit": product_data.operational_cost_per_unit,
                "discount_percentage": product_data.discount_percentage,
                "competitor_price": product_data.competitor_price,
                "transaction_date": product_data.transaction_date.isoformat(),
                "actual_selling_price": product_data.actual_selling_price,
                "gross_profit_per_unit": product_data.gross_profit_per_unit,
                "profit_percentage": product_data.profit_percentage,
                # Loan-specific fields
                "monthly_emi": loan.monthly_emi,
                "outstanding_amount": loan.outstanding_amount,
                "tenure_months": loan.tenure_months,
                "principal_amount": loan.principal_amount,
                "interest_rate": loan.interest_rate
            }

            # 4. Call external EMI prediction API
            try:
                # response = requests.post(PREDICT_EMI_SERVICE_URL, json=payload)
                response = predicted_emi(payload)
                # response.raise_for_status()
                predicted_response = response.json()
                blocked_amount = predicted_response.get("predicted_emi_contribution_percent_of_profit")
                if blocked_amount is None:
                    raise HTTPException(status_code=500, detail=f"Invalid response for loan {loan.id}")
            except requests.RequestException as e:
                raise HTTPException(status_code=500, detail=f"Prediction API call failed for loan {loan.id}: {str(e)}")

            # 5. Create emi_blocked Transaction for this loan
            new_txn = Transaction(
                borrower_id=borrower_id,
                loan_id=loan.id,
                type="emi_blocked",
                amount=blocked_amount,
                description=f"EMI amount blocked for loan {loan.id}",
                timestamp=datetime.utcnow(),
                status="pending",
                payment_method=None,
                reference_number=None
            )
            session.add(new_txn)
            session.commit()
            session.refresh(new_txn)

            # Collect result
            results.append({
                "loan_id": str(loan.id),
                "blocked_amount": blocked_amount,
                "transaction_id": str(new_txn.id)
            })

    return {
        "message": "EMI prediction and blocking completed",
        "results": results
    }