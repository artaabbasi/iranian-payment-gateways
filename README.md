# 🏦 Iranian Payment Gateways SDK

**All-in-One SDK to integrate Iranian payment gateways** in Python projects (Django, FastAPI, etc.). 🚀

---
## ✨ Features

- Unified interface for multiple Iranian gateways.
- Supports synchronous and asynchronous operations.
- Standardized exceptions and error handling.
- Easily extendable to new gateways.

---

## 📦 Installation

Copy the `gateways` and `lib` folders into your project.  
No external PyPI package required. Python ≥ 3.10 recommended.

```bash
# Example project structure
your_project/
├── app/
├── gateways/
├── lib/
└── ...
```

---

## 🛠 Supported Gateways

| Gateway Name          | Status      |
|----------------------|------------|
| BehpardakhtGateway    | ✅ Done    |
| SampleGateway         | ✅ Done    |
| SamanGateway          | ⏳ In progress |
| MellatGateway         | ⏳ In progress |

> You can request additional gateways by opening an issue or contacting the maintainers. 💬

---

## 🔧 Usage

### Unified Gateway API

```python
from gateways.sample_gateway.sample_gateway import SampleGateway
from gateways.sample_gateway.datamodel.gateway_info_datamodel import GatewayInfoDataModel
from gateways.sample_gateway.schema.pay_schema import PaySchema
from gateways.sample_gateway.schema.verify_schema import VerifySchema

# Initialize gateway
gateway_info = GatewayInfoDataModel(username="user", password="pass")
gateway = SampleGateway(info=gateway_info)

# Pay
pay_schema = PaySchema(amount=1000, transaction_id="1234")
pay_response = gateway.pay(pay_schema)
print(pay_response.url)

# Verify
verify_schema = VerifySchema(transaction_id="1234", amount=1000)
verify_response = gateway.verify(verify_schema)
print(verify_response.verified)
```

### Exception Handling

```python
from lib.gateway.base_exception import GatewayError, GatewayConnectionError

try:
    response = gateway.pay(pay_schema)
except GatewayConnectionError as e:
    print(f"Connection failed: {e}")
except GatewayError as e:
    print(f"Gateway error: {e.code} - {e.text}")
```

---

## Django Example (Django ORM) 🐍

```python
# models.py
from django.db import models

class PaymentTransaction(models.Model):
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.IntegerField()
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

# views.py
from django.http import JsonResponse
from gateways.sample_gateway.sample_gateway import SampleGateway
from gateways.sample_gateway.datamodel.gateway_info_datamodel import GatewayInfoDataModel
from gateways.sample_gateway.schema.pay_schema import PaySchema

def pay_view(request):
    gateway_info = GatewayInfoDataModel(username="user", password="pass")
    gateway = SampleGateway(info=gateway_info)
    
    pay_schema = PaySchema(amount=1000, transaction_id="txn_001")
    response = gateway.pay(pay_schema)
    
    # Save transaction
    PaymentTransaction.objects.create(
        transaction_id=pay_schema.transaction_id,
        amount=pay_schema.amount
    )
    
    return JsonResponse({"pay_url": response.url})
```

---

## FastAPI Example (SQLAlchemy) ⚡

```python
# models.py
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PaymentTransaction(Base):
    __tablename__ = "payment_transaction"
    transaction_id = Column(String, primary_key=True, unique=True)
    amount = Column(Integer)
    verified = Column(Boolean, default=False)

# main.py
from fastapi import FastAPI
from sqlalchemy.orm import Session
from gateways.sample_gateway.sample_gateway import SampleGateway
from gateways.sample_gateway.datamodel.gateway_info_datamodel import GatewayInfoDataModel
from gateways.sample_gateway.schema.pay_schema import PaySchema

app = FastAPI()

@app.post("/pay")
def pay(amount: int, transaction_id: str, db: Session):
    gateway_info = GatewayInfoDataModel(username="user", password="pass")
    gateway = SampleGateway(info=gateway_info)
    
    pay_schema = PaySchema(amount=amount, transaction_id=transaction_id)
    response = gateway.pay(pay_schema)
    
    # Save transaction
    db_transaction = PaymentTransaction(transaction_id=transaction_id, amount=amount)
    db.add(db_transaction)
    db.commit()
    
    return {"pay_url": response.url}
```

---

## Contributing 📝

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License ⚖️

MIT License

---
