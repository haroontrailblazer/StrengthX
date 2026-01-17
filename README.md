# StrengthX - Know How Strong Is Your Passwords

https://github.com/user-attachments/assets/50a608b8-f360-408f-bc83-86bbda26c1f5

**StrengthX** is a web application that helps users evaluate the strength of their passwords and check if their passwords have been involved in known data breaches. It provides a quick and secure way to improve password security and promote safe online practices.  

<br>
<div align="center">

![Security](https://img.shields.io/badge/Security-OWASP%20ASVS%20L1-green)

![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg) 
![Python Version](https://img.shields.io/badge/Python-3.11+-blue.svg) 
![Contributors](https://img.shields.io/badge/Contributors-5-orange.svg) 
[![Status](https://img.shields.io/badge/Status-Active-success.svg)](#)
[![Maintained](https://img.shields.io/badge/Maintained-Yes-brightgreen.svg)](#)

</div>

<div align="center">

### 🛡️ Created by Google Certified Cybersecurity Engineer

<img width="180" height="180" alt="google-cloud-cybersecurity-certificate" src="https://github.com/user-attachments/assets/cf3be9ea-a06c-471f-9b6c-ff1e6163e472" />

[![Credly Badge](https://img.shields.io/badge/View%20on-Credly-orange?style=flat&logo=credly)](https://www.credly.com/users/haroon-k-m)


**Skills:**  
Cloud Backup · Cloud Computing · Cloud Security · Compliance Lifecycle · Cybersecurity · Cyber Threat Intelligence · Data Protection · Disaster Recovery · Google Cloud · Identity And Access Management (IAM) · Network Security · Threat Detection  

</div>

---

## Features

- **Password Strength Check**: Evaluates the complexity of the entered password.  
- **Breach Verification**: Checks how many times a password has been exposed in known data breaches.  
- **Privacy-Focused**: Passwords are never stored in the backend; all checks are done securely.  
- **Interactive UI**: User-friendly interface for seamless password testing.  

---

## Contributors

- **Backend Developers**: Haroon K M
- **Backend Developers**: Balamurugan T
- **Frontend Developer**: Sujay S
- **Documentation**: Enbachozhan V
- **Security Engineer**: Harikrishnan V
  
---

## Technology Stack

- **Backend**: Python  
- **Frontend**: Streamlit
- **AI-Model**: ollama  
- **Libraries/Tools**: `zxcvbn`, `hashlib`, `pwnedpasswords`, `ollama` API 

---

## Usage

1. Enter a password in the input field.  
2. View the password strength score and suggestions to improve it.  
3. Check if the password has been exposed in data breaches.  
4. Adjust your password accordingly for better security.
5. summon SterngthX-Dildo AI to generate a strong password.

## Performance Comparison
![WhatsApp Image 2025-12-22 at 10 43 09 PM](https://github.com/user-attachments/assets/f6770611-6891-43e3-9b7a-cf6e961eaa21)

| **Legend** | 🟩 | 🟨 | 🟧 | ⬜ |
|-----------|-----|-----|-----|-----|
| **Score** | 5   | 4   | 3   | 0   |


| **Feature**                      | **StrengthX** | **LastPass** | **1Password** | **NordPass** |
|---------------------------------|----------------|--------------|----------------|--------------|
| **AI Password Generation**      | 🟩  | ⬜  | ⬜  | ⬜  |
| **Uses zxcvbn**                 | 🟩  | 🟨  | 🟨  | 🟨  |
| **Uses live breach database**   | 🟩  | ⬜  | ⬜  | 🟧  |
| **Regex-based policy enforcement** | 🟩  | 🟧  | 🟧  | 🟧  |
| **Local-only evaluation**       | 🟩  | ⬜  | ⬜  | ⬜  | 

---

## Security & Privacy
<img width="1408" height="768" alt="1766987176158" src="https://github.com/user-attachments/assets/d1d65191-fe0b-41db-8446-de0919f743af" />


### OWASP ASVS Password Policy Alignment
Open Worldwide Application Security Project / Application Security Verification Standard.

This password evaluation component has been reviewed against **OWASP ASVS v4.0.3** and meets all applicable controls within its defined scope.

### ASVS Scope & Level
- **ASVS Version:** 4.0.3  
- **ASVS Level:** Level 1 (L1)  
- **Scope:** Password evaluation only (no authentication, storage, or sessions)

### ASVS Control Mapping

| ASVS Control ID | OWASP Requirement | Implementation Detail | Compliance |
|-----------------|------------------|------------------------|------------|
| **V2.1.1** | Passwords are not stored or processed insecurely | Passwords exist only in volatile memory and are never persisted | ✅ |
| **V2.1.2** | Password strength is evaluated using entropy | Entropy-based evaluation performed using `zxcvbn` | ✅ |
| **V2.1.3** | Breached passwords are detected | Passwords are checked against Have I Been Pwned using k-anonymity | ✅ |
| **V2.1.4** | No insecure composition rules are enforced | No forced uppercase, symbols, or numeric constraints | ✅ |
| **V2.1.5** | Long passphrases are supported | No truncation; long passphrases are fully supported | ✅ |
| **V2.1.6** | Password rotation is not required without compromise | No forced periodic password rotation | ✅ |
| **V2.1.7** | Users are informed about password handling | User-facing disclosure explains secure, non-persistent handling | ✅ |
| **V6.1.2** | Weak cryptographic primitives are not misused | SHA-1 used only for HIBP interoperability, not for storage or auth | ✅ |

### Compliance Statement

> This password evaluation module is **ASVS Level 1–ready** under OWASP ASVS v4.0.3.  
> All applicable password-handling and cryptographic controls are satisfied within the defined scope.

### Auditor Notes
- Authentication, session management, and authorization are intentionally out of scope
- SHA-1 usage is strictly limited to external breach detection compatibility
- No password data is logged, rendered, or persisted
- All passwords are processed locally in the browser and hashed before any breach verification.  
- No user passwords or sensitive information are stored on the server.  
- Fully Fully compliant with OWASP Password Guidelines
  
---

## License

This project is licensed under the [Apache License 2.0](LICENSE).  

---

## Contact

For queries or contributions, feel free to contact the contributors listed above or open an issue in the repository.

---

**StrengthX – Empowering safer online practices, one password at a time.**
