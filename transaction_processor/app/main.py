# API endpoints

import sqlite3

from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field

from app.database import get_connection, init_db

app = FastAPI(title = "Transaction  Processor")

@app.on_event("startup")
def startup():
    init_db()

class AccountCreate(BaseModel):
    owner: str = Field(min_length=1, max_length=100)
    balance: float = Field(ge=0)

class TransferCreate(BaseModel):
    from_account_id: int = Field(gt=0)
    to_account_id: int = Field(gt=0)
    amount: float = Field(gt=0)

@app.post("/accounts", status_code=status.HTTP_201.CREATED)
def create_account(account: AccountCreate):
    conn = get_connection()

    try:
        cursor = conn.execute(
            "INSERT INTO accounts (owner, balance) VALUES (?, ?)",
            (account.owner, account.balance),
        )
        conn.commit()

        return {
            "id": cursor.lastrowid,
            "owner": account.owner,
            "balance": account.balance
        }
    finally:
        conn.close()


@app.get("/accounts/{account_id}")
def get_account(account_id: int):
    conn = get_connection()
    try:
        account = conn.execute(
            "SELECT id, owner, balance FROM accounts WHERE id = ?",
            (account_id,),
        ).fetchone()
    
        if account is None:
            raise HTTPException(status_code=404, detail="account not found")
        
        return dict(account)

    finally:
        conn.close()


@app.post("/transfers", status_code=status.HTTP_201_CREATED)
def transfer_money(transfer: TransferCreate):
    if transfer.from_account_id == transfer.to_account_id:
        raise HTTPException(status_code=400, detail="Source and Destination account must differ")

    conn = get_connection()

    try:
        conn.execute("BEGIN")

        sender = conn.execute(
            "SELECT id, balance FROM accounts WHERE id = ? ",
            (transfer.from_account_id,),
        ).fetchone()

        receiver = conn.execute(
            "SELECT id FROM accounts WHERE id = ? ",
            (transfer.to_account_id,),
        ).fetchone()

        if sender is None or receiver is None:
            raise HTTPException(status_code=404, detail="Account not found")
        
        if sender["balance"] < transfer.amount:
            raise HTTPException(
                status_code=400,
                detail="Insufficient Balance",
            )

        conn.execute(
            "UPDATE accounts SET balance = balance - ? WHERE id = ?",
            (transfer.amount, transfer.from_account_id)
        )

        conn.execute(
            "UPDATE accounts SET balance = balance + ? WHERE id = ?",
            (transfer.amount, transfer.to_account_id)
        )

        cursor = 