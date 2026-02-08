# 🇮🇷 Iranian Payment Gateways (Python)

A modular, extensible Python library that provides a **unified interface** for integrating Iranian online payment gateways.

This library is designed with **clean architecture principles**, strong typing, and clear separation between:
- core gateway contracts
- gateway-specific schemas
- persistence models

---

## ✨ Key Features

- 🔌 Unified gateway interface (`BasePaymentGateway`)
- 🧩 Strongly-typed schemas using Generics
- 🔄 Sync & Async API support
- 🏗 Clean separation of core logic and gateway implementations
- 📦 Framework-agnostic (Django, FastAPI, Flask, etc.)
- ➕ Easy to add new payment gateways

---

## 📦 Project Structure

```
iranian-payment-gateways/
│
├── gateways/
│   ├── __init__.py
│   └── sample_gateway/
│       ├── sample_gateway.py
│       ├── info_repository.py
│       ├── transaction_repository.py
│       ├── datamodel/
│       │   ├── gateway_info_datamodel.py
│       │   └── gateway_transaction_datamodel.py
│       └── schema/
│           ├── pay_schema.py
│           ├── verify_schema.py
│           └── after_pay_schema.py
│
└── lib/
    ├── __init__.py
    └── gateway/
        ├── base_payment_gateway.py
        └── schema/
            ├── base_pay_schema.py
            ├── base_verify_schema.py
            ├── base_after_pay_schema.py
            ├── pay_out_schema.py
            └── verify_out_schema.py
```

---

## 🧠 Core Concept

At the heart of the library is the `BasePaymentGateway`, a **generic abstract base class**:

```python
class BasePaymentGateway(Generic[P, AP, V]):
    def pay(self, data: P) -> PayOutSchema: ...
    def verify(self, data: V) -> VerifyOutSchema: ...
    def after_pay(self, data: AP) -> None: ...
```

Each gateway:
- defines its **own schemas**
- implements the same **core contract**
- remains interchangeable at runtime

---

## 🚀 Quick Start

### 1️⃣ Get a gateway

```python
from gateways import get_gateway_from_name

GatewayClass = get_gateway_from_name("sample")
gateway = GatewayClass()
```

### 2️⃣ Create a payment

```python
from gateways.sample_gateway.schema.pay_schema import PaySchema

pay_data = PaySchema(
    amount=100_000,
    callback_url="https://example.com/callback"
)

result = gateway.pay(pay_data)
print(result.url)
print(result.transaction_id)
```

### 3️⃣ Verify payment

```python
from gateways.sample_gateway.schema.verify_schema import VerifySchema

verify_data = VerifySchema(
    transaction_id=result.transaction_id,
    amount=100_000
)

verify_result = gateway.verify(verify_data)
if verify_result.verified:
    print("Payment verified")
```

### 4️⃣ After payment (callback handling)

```python
from gateways.sample_gateway.schema.after_pay_schema import AfterPaySchema

after_pay_data = AfterPaySchema(
    transaction_id=result.transaction_id,
    amount=100_000,
    tracking_code="ABC123"
)

gateway.after_pay(after_pay_data)
```

### ⚡ Async Support

```python
result = await gateway.a_pay(pay_data)
verify_result = await gateway.a_verify(verify_data)
await gateway.a_after_pay(after_pay_data)
```

---

## 🏭 Gateway Factory

```python
gateway_map = {
    "sample": SampleGateway,
}
```

```python
GatewayClass = get_gateway_from_name("sample")
gateway = GatewayClass()
```

---

## 🧪 Sample Gateway

The included `SampleGateway` demonstrates:
- full payment lifecycle
- repository usage
- schema validation
- transaction persistence

It is intended for **learning and testing purposes**.

---

## 🛡 Error Handling

All gateways return standardized output schemas:
- `PayOutSchema`
- `VerifyOutSchema`

---

## 📜 License

MIT License  
Free to use, modify, and distribute.
