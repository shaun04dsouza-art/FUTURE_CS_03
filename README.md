# 🔐 Secure File Sharing System  
**Author:** Shaun D’Souza  

---

## 📘 About the Project  
This project is a **Secure File Sharing System** built using **Python Flask** and **AES-256-GCM encryption**.  
It allows users to upload files that are **encrypted before storage** and securely **decrypted on download**, ensuring confidentiality and integrity of data.

---

## ⚙️ Features  
- 🔒 AES-256-GCM encryption & decryption  
- 🗂 Secure upload and download portal  
- 🧾 SHA-256 file integrity verification  
- 🔑 Environment-based key management (`FILE_KEY`)  
- 💡 Simple user interface using Flask  

---

## 🛠 Tools & Technologies  
| Tool | Purpose |
|------|----------|
| **Python Flask** | Backend framework |
| **PyCryptodome** | AES encryption/decryption |
| **HTML / CSS** | Frontend interface |
| **Git & GitHub** | Version control |
| **PowerShell / CMD** | Environment setup |
| **Postman / curl** | API testing (optional) |

---

## 🚀 Setup & Run Instructions  

```powershell
# 1️⃣ Create & activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2️⃣ Install dependencies
pip install flask pycryptodome

# 3️⃣ Generate & set AES key
python -c "import os,binascii; print(binascii.hexlify(os.urandom(32)).decode())"
$env:FILE_KEY="paste_your_hex_key_here"

# 4️⃣ Run the application
python app.py
