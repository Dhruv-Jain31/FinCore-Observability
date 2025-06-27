from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .schemas import TransferRequest
from .metrics import TRANSFER_COUNT
from .database.models import Account
from .database.db import get_db

router = APIRouter()

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .schemas import TransferRequest
from .metrics import TRANSFER_COUNT
from .database.models import Account
from .database.db import get_db

router = APIRouter()

@router.get("/")
def welcome():
    return {"message": "Welcome to FinCore!"}

@router.post("/transfer")
def transfer_money(payload: TransferRequest, db: Session = Depends(get_db)):
    sender = db.query(Account).filter(Account.account_id == payload.from_account).first()
    receiver = db.query(Account).filter(Account.account_id == payload.to_account).first()

    if not sender or not receiver:
        raise HTTPException(status_code=404, detail="One or both accounts not found")

    if sender.balance < payload.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    sender.balance -= payload.amount
    receiver.balance += payload.amount
    db.commit()

    TRANSFER_COUNT.inc()

    return {"status": "success", "message": f"{payload.amount} transferred"}
