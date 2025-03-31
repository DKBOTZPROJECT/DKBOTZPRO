# 📌 DKBOTZPRO

Welcome to **DKBOTZPRO**! 🚀 This library allows you to interact with multiple services dynamically, including premium authentication, UPI QR generation, and Base64 encoding/decoding.

---
## Installation

You can install DKBotzPro using pip:

```
pip install dkbotzpro
```


## ⚡ How to Use

### 🛠 Initialization
To use the library, create an instance of `DKBotzPro` with the desired service type:

```python
from dkbotzpro import DKBotzPro

# Initialize for premium services
dkbotz = DKBotzPro("premium")

# Initialize for UPI QR generation
dkbotz = DKBotzPro("upi_qr")

# Initialize for Base64 encoding/decoding
dkbotz = DKBotzPro("base64")
```

---

## 🔑 Premium Services

### ✅ Login
Authenticate a user with username and password.

```python
status, response = dkbotz.premium_login("username", "password")
print(status, response)
```

### 🔍 Verify Product
Check if a product is valid for a user.

```python
status, response = dkbotz.premium_verify_product("username", "password", "product_name")
print(status, response)
```

### ⚙️ Edit Server
Modify server details for a specific product.

```python
status, response = dkbotz.premium_edit_server("username", "password", "product_name", "server1", 'server_main', "new_value")
print(status, response)
```

---

## 💰 UPI QR Code Generator
Generate a UPI QR code link for payment.

```python
status, qr_link = dkbotz.convert("upi_id@bank", "Payee Name", "100.00")
print(status, qr_link)
```

---

## 🔄 Base64 Encoding & Decoding

### 📝 Encode Text
Convert text into Base64 format.

```python
status, encoded = dkbotz.encode_text("Hello, DKBotz!")
print(status, encoded)
```

### 🔓 Decode Text
Convert Base64 back to plain text.

```python
status, decoded = dkbotz.decode_text(encoded)
print(status, decoded)
```

---

## ❌ Error Handling
All functions return `False` with an error message if required parameters are missing or an exception occurs.

```python
status, message = dkbotz.premium_login("username")  # Missing password
print(status, message)  # Output: False, "Missing parameters: password"
```

---

### ✨ Enjoy using DKBotzPro! 😃 Need help? Contact support! 🤖

