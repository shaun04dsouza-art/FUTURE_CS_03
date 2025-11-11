# 🔐 Security Overview  
**Future Interns – Cyber Security Task 3**  
**Project:** Secure File Sharing System  
**Author:** Shaun D’Souza  

---

## 1️⃣ Encryption Method  
- **Algorithm:** AES (Advanced Encryption Standard) in **GCM mode**  
- **Key Size:** 256 bits (32 bytes)  
- **Purpose:** AES-GCM provides both confidentiality and integrity.  
- Each file uses a unique 12-byte random **nonce** and 16-byte **authentication tag**.  
- Stored file format: `nonce | tag | ciphertext`

---

## 2️⃣ Key Management  
- Key is **not hard-coded** in code.  
- Loaded from environment variable `FILE_KEY`.  
- Key generation example:  
  ```powershell
  python -c "import os,binascii; print(binascii.hexlify(os.urandom(32)).decode())"
  $env:FILE_KEY="your_32_byte_hex_key_here"
  ```
- In production, store the key in a secure vault or `.env` file that is **not committed** to Git.

---

## 3️⃣ Integrity Verification  
- SHA-256 hash of the plaintext is created before encryption.  
- Saved as `<filename>.enc.sha256`.  
- On download, the hash of the decrypted file is compared with the stored hash to verify that the file was not altered.

---

## 4️⃣ File Handling and Storage  
- Uploaded files are never stored in plaintext.  
- Decryption occurs only in memory during download.  
- `uploads/` folder is ignored in `.gitignore` to avoid committing encrypted data.

---

## 5️⃣ Deployment and Best Practices  
- Use **HTTPS** to secure file transfer.  
- Limit upload size and sanitize filenames.  
- Rotate keys periodically.  
- Add authentication and access control for multi-user deployments.

---

## 6️⃣ Summary  
The system demonstrates how encryption, key management, and integrity verification protect sensitive data both **at rest** and **in transit**, meeting real-world security requirements in corporate and healthcare environments.
