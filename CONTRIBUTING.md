# Contributing to Iranian Payment Gateways

We welcome contributions to improve this library!  
This document explains how to **add new gateways**, improve code, and follow conventions.

---

## ➕ Adding a New Gateway

1️⃣ Create a new gateway folder:

```
gateways/<gateway_name>_gateway/
```

2️⃣ Define gateway-specific schemas:

```python
class <GatewayName>PaySchema(BasePaySchema): ...
class <GatewayName>VerifySchema(BaseVerifySchema): ...
class <GatewayName>AfterPaySchema(BaseAfterPaySchema): ...
```

3️⃣ Implement the gateway:

```python
class <GatewayName>Gateway(
    BasePaymentGateway[
        <GatewayName>PaySchema,
        <GatewayName>AfterPaySchema,
        <GatewayName>VerifySchema
    ]
):
    def pay(self, data): ...
    def verify(self, data): ...
    def after_pay(self, data): ...
```

4️⃣ Register the gateway:

```python
gateway_map["<gateway_name>"] = <GatewayName>Gateway
```

---

## 🧹 Code Style

- Python 3.10+
- Type annotations for all public functions
- Use async functions where appropriate (`a_pay`, `a_verify`, `a_after_pay`)
- Follow existing file/folder structure

---

## 🧪 Testing

- Add tests for all new gateway methods
- Use existing repository for persistence mocks
- Ensure Pay/Verify/AfterPay flows are tested
- Use `pytest` for running tests

---

## 🤝 Pull Requests

1. Fork the repository
2. Create a branch (`feature/<gateway_name>` or `fix/<issue>`)
3. Add your code and tests
4. Run `pytest` to verify everything works
5. Submit a pull request with a descriptive title and summary

---

## ❤️ Thank You

Your contribution helps make **integration with Iranian payment gateways easier for everyone**!
