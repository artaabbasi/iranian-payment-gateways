# SAMPLE.md

# 🚀 Sample Implementations with Iranian Payment Gateways SDK

This document provides **example usage** of the SDK in:

1. Django (using Django ORM)  
2. FastAPI (using SQLAlchemy)

---

## 1️⃣ Django Example (Django ORM)

### 1.1 Setup

```bash
pip install django
```

### 1.2 Django Model

```python
# myapp/models.py
from django.db import models

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=255, unique=True)
    amount = models.IntegerField()
    tracking_code = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### 1.3 Repository Implementation

```python
# myapp/repository.py
from myapp.models import Transaction
from gateways.behpardakht_gateway.datamodel.behpardakht_transaction_datamodel import GatewayTransactionDataModel


class DjangoTransactionRepository:
    def create(self, transaction: GatewayTransactionDataModel):
        Transaction.objects.create(
            transaction_id=transaction.transaction_id,
            amount=transaction.amount,
            tracking_code=getattr(transaction, "tracking_code", None)
        )

    def get(self, transaction_id: str):
        return Transaction.objects.get(transaction_id=transaction_id)

    def update(self, transaction: GatewayTransactionDataModel):
        Transaction.objects.filter(transaction_id=transaction.transaction_id).update(
            amount=transaction.amount,
            tracking_code=transaction.tracking_code
        )
```

### 1.4 Using Gateway

```python
from gateways.sample_gateway.sample_gateway import SampleGateway
from gateways.sample_gateway.schema.pay_schema import PaySchema
from gateways.sample_gateway.schema.verify_schema import VerifySchema
from gateways.sample_gateway.schema.after_pay_schema import AfterPaySchema

gateway = SampleGateway()

# Create Payment
pay_data = PaySchema(amount=100_000, callback_url="https://example.com/callback")
pay_result = gateway.pay(pay_data)

# Verify Payment
verify_data = VerifySchema(transaction_id=pay_result.transaction_id, amount=100_000)
verify_result = gateway.verify(verify_data)

# After Payment
after_pay_data = AfterPaySchema(
    transaction_id=pay_result.transaction_id,
    amount=100_000,
    tracking_code="ABC123"
)
gateway.after_pay(after_pay_data)
```

---

## 2️⃣ FastAPI Example (SQLAlchemy)

### 2.1 Setup

```bash
pip install fastapi uvicorn sqlalchemy
```

### 2.2 SQLAlchemy Models

```python
# app/models.py
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transactions"
    transaction_id = Column(String, primary_key=True)
    amount = Column(Integer, nullable=False)
    tracking_code = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### 2.3 Repository Implementation

```python
# app/repository.py
from sqlalchemy.orm import Session
from app.models import Transaction
from gateways.behpardakht_gateway.datamodel.behpardakht_transaction_datamodel import GatewayTransactionDataModel


class SQLAlchemyTransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, transaction: GatewayTransactionDataModel):
        db_tx = Transaction(
            transaction_id=transaction.transaction_id,
            amount=transaction.amount,
            tracking_code=getattr(transaction, "tracking_code", None)
        )
        self.db.add(db_tx)
        self.db.commit()
        self.db.refresh(db_tx)
        return db_tx

    def get(self, transaction_id: str):
        return self.db.query(Transaction).filter_by(transaction_id=transaction_id).first()

    def update(self, transaction: GatewayTransactionDataModel):
        db_tx = self.db.query(Transaction).filter_by(transaction_id=transaction.transaction_id).first()
        db_tx.amount = transaction.amount
        db_tx.tracking_code = transaction.tracking_code
        self.db.commit()
```

### 2.4 FastAPI Endpoint Example

```python
# app/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from gateways.sample_gateway.sample_gateway import SampleGateway
from gateways.sample_gateway.schema.pay_schema import PaySchema

from app.models import Base
from app.repository import SQLAlchemyTransactionRepository

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI()
gateway = SampleGateway()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/pay")
def pay(amount: int, db: Session = Depends(get_db)):
    repo = SQLAlchemyTransactionRepository(db)
    gateway._transaction_repository = repo

    pay_data = PaySchema(amount=amount, callback_url="https://example.com/callback")
    result = gateway.pay(pay_data)
    return {"transaction_id": result.transaction_id, "url": result.url}
```

---

✅ This demonstrates **full integration** of the SDK in **Django ORM** and **FastAPI with SQLAlchemy** without installing it as a pip package.
