from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from models import Users, Loan, EMIWallet, Transaction, EMIPayment
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
