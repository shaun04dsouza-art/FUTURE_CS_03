# app.py — Secure File Sharing System (Flask + AES Encryption)
# Author: Shaun (Future Interns Task 3)

import os, binascii, hashlib
from flask import Flask, request, render_template_string, send_file, abort
from Crypto.Cipher import AES

# Flask app setup
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Read 32-byte AES key from environment variable
KEY_HEX = os.getenv("FILE_KEY")
if not KEY_HEX:
    raise RuntimeError(
        "⚠️ Please set FILE_KEY environment variable before running.\n"
        "Example (PowerShell):\n"
        '$env:FILE_KEY="paste_your_hex_key_here"'
    )

KEY = binascii.unhexlify(KEY_HEX)  # Convert hex -> bytes (32 bytes = AES-256)

# Simple web page
HTML = """
<!doctype html>
<html>
<head>
  <title>🔐 Secure File Sharing</title>
  <style>
    body { font-family: Arial; background:#f2f2f2; margin:40px; }
    h1 { color:#333; }
    form, ul { background:white; padding:20px; border-radius:10px; box-shadow:0 2px 6px rgba(0,0,0,0.15); }
    input[type=file] { margin-bottom:10px; }
  </style>
</head>
<body>
  <h1>🔐 Secure File Sharing System</h1>
  <h3>Upload a File (It will be AES Encrypted)</h3>
  <form method="post" enctype="multipart/form-data" action="/upload">
    <input type="file" name="file" required>
    <br>
    <input type="submit" value="Upload">
  </form>
  <br>
  <h3>Encrypted Files</h3>
  <ul>
  {% for f in files %}
    <li>{{f}} — <a href="/download/{{f}}">Download (Decrypt)</a></li>
  {% else %}
    <li>No files uploaded yet.</li>
  {% endfor %}
  </ul>
</body>
</html>
"""

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

@app.route("/")
def index():
    files = [f[:-4] for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".enc")]
    return render_template_string(HTML, files=files)

@app.route("/upload", methods=["POST"])
def upload():
    uploaded_file = request.files.get("file")
    if not uploaded_file:
        return "❌ No file selected.", 400

    data = uploaded_file.read()
    digest = sha256_bytes(data)

    nonce = os.urandom(12)
    cipher = AES.new(KEY, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    filename = os.path.basename(uploaded_file.filename)
    enc_path = os.path.join(UPLOAD_FOLDER, filename + ".enc")

    with open(enc_path, "wb") as f:
        f.write(nonce + tag + ciphertext)
    with open(enc_path + ".sha256", "w") as f:
        f.write(digest)

    return f"✅ File '{filename}' encrypted and saved successfully!"

@app.route("/download/<path:filename>")
def download(filename):
    enc_path = os.path.join(UPLOAD_FOLDER, filename + ".enc")
    hash_path = enc_path + ".sha256"

    if not os.path.exists(enc_path):
        return abort(404)

    raw = open(enc_path, "rb").read()
    nonce = raw[:12]
    tag = raw[12:28]
    ciphertext = raw[28:]

    try:
        cipher = AES.new(KEY, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    except Exception:
        return "❌ Decryption failed (corrupted or wrong key).", 400

    expected = open(hash_path).read().strip() if os.path.exists(hash_path) else None
    actual = sha256_bytes(plaintext)
    if expected and expected != actual:
        return "⚠️ File integrity check failed!", 500

    from io import BytesIO
    file_obj = BytesIO(plaintext)
    file_obj.seek(0)
    return send_file(file_obj, as_attachment=True, download_name=filename)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
