from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from models import  Users, BorrowerProfile, LenderProfile, Loan, EMIWallet, Transaction, EMIPayment
from db import engine

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
