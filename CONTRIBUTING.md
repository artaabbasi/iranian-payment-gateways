# Contributing to Iranian Payment Gateways SDK 🚀

Thank you for your interest in contributing! ❤️

---

## Project Structure 📁

```
gateways/
  <gateway_name>/
    <gateway_name>.py          # main gateway class
    datamodel/                 # Gateway-specific datamodels
    schema/                    # Gateway-specific schemas
lib/
  gateway/
    base_payment_gateway.py    # Base gateway class
    base_exception.py          # Base exceptions
```

---

## Adding a New Gateway ➕

1. Create a new folder under `gateways/` with the gateway name.
2. Add:
   - `your_gateway.py` extending `BasePaymentGateway`.
   - `datamodel/` for gateway-specific data.
   - `schema/` for payment/verify/after_pay schemas.
3. Implement required methods:
   - `pay(data: PaySchema)`
   - `verify(data: VerifySchema)`
   - `after_pay(data: AfterPaySchema)`

💡 Use `GatewayInfoDataModel(username, password)` for your gateway info.

---

## Coding Guidelines 🧹

- Python ≥ 3.10
- Type hints required.
- Use async methods where possible (`a_pay`, `a_verify`, `a_after_pay`).
- Docstrings for all public methods.
- Follow Clean Architecture principles.

---

## Testing 🧪

- Add tests in `tests/` folder (to be created) for each gateway.
- Test both sync and async methods.
- Mock external APIs when possible.

---

## Commit & PR Guidelines 🔧

- Branch naming: `feature/<gateway_name>` or `bugfix/<issue>`
- Commit messages: Use imperative tense.
- Open PRs against `main` branch.
- Include tests and docs for new features.

---

## Gateway Requests 💬

If your favorite Iranian payment gateway is missing, please open an issue or contact the maintainers! We love to hear which gateways you need next. 🚀
