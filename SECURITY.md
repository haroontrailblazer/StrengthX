# 🔐 Security Policy

Thank you for taking the time to help make **StrengthX** more secure.  
We take security and privacy very seriously, especially since our project deals with password analysis and user data protection.

---

## 🛡️ Supported Versions

We currently provide security updates for the latest **main** branch.

| Version | Supported |
|----------|------------|
| `main` (latest) | ✅ Supported |
| Older versions | ⚠️ Not actively maintained |

---

## 🚨 Reporting a Vulnerability

If you discover a **vulnerability**, **security issue**, or **data privacy risk** in StrengthX:

1. **Do not open a public issue.**  
   Instead, please report it **privately** to the maintainers.

2. Contact via:
   - 📧 **Email:** [hexra2025@gmail.com](mailto:hexra2025@gmail.com)
   - Or open a **confidential GitHub Security Advisory** (if available).

3. Include in your report:
   - A clear and concise description of the vulnerability.
   - Steps to reproduce the issue (if applicable).
   - The potential impact or affected areas.
   - Any suggestions for mitigation.

We’ll acknowledge your report within **48 hours** and aim to provide a fix or response within **7 working days**, depending on severity.

---

## 🔒 Security Principles Followed

StrengthX follows key security and privacy principles:

- **No Data Storage:** User passwords or hashes are never logged, stored, or transmitted to external servers.  
- **Hashed API Queries:** All password breach checks use **SHA-1 hashing** before transmission to maintain user privacy.  
- **Zero Retention:** No personally identifiable information (PII) is stored on the server.  
- **Secure Dependencies:** All Python dependencies are regularly scanned for vulnerabilities using `pip-audit` and GitHub Dependabot.  
- **HTTPS Communication:** StrengthX is designed for deployment under HTTPS to ensure encrypted traffic.

---

## 🧠 Responsible Disclosure Guidelines

- Act in **good faith** and avoid publicly disclosing vulnerabilities before they are fixed.  
- Do not exploit, damage, or access user data during your testing.  
- Respect user privacy and comply with all applicable laws.  
- We credit responsible researchers in our release notes, if they wish.

---

## 🧩 Recommended Security Tools

Developers contributing to StrengthX are encouraged to use:
- `bandit` — for static security analysis in Python  
- `pip-audit` — to check for vulnerable dependencies  
- `pre-commit` hooks — to ensure no secrets or keys are committed

---

## 📜 Legal

By submitting a security report, you agree to allow the StrengthX maintainers to use your report for improving project security without restriction.  
This project is covered under the **Apache License 2.0**.

---

> 🛡️ Security is everyone’s responsibility — thank you for helping make StrengthX safer for all users.
