
# Supported Versions

This repository currently supports security updates for the **latest main branch only**.

![Security](https://img.shields.io/badge/Security-OWASP%20ASVS%20L1-green)




## Security Scope

This project includes:
- Password strength evaluation
- Breached password checking using k-anonymity
- Client-side password input handling

This project **does NOT** include:
- Authentication or login systems
- Password storage
- Session management
- Authorization logic
- Payment processing

Security assessments are scoped accordingly.

---

## Security Standards & Compliance

This project aligns with the following standards and guidelines:

- OWASP Application Security Verification Standard (ASVS) v4.0.3  
  - Certified **ASVS Level 1–Ready** (password evaluation scope)
- OWASP Password Guidelines
- OWASP Top 10 (Input handling & data exposure)

---

## Cryptographic Practices

- Passwords are **never stored**
- Passwords are **never logged**
- Passwords are **never rendered back to the UI**
- SHA-1 is used **only** for compatibility with the Have I Been Pwned API
- SHA-1 is **not** used for authentication or storage
- Entropy-based strength estimation is performed using industry-standard methods

---

## Reporting a Vulnerability

If you discover a security vulnerability, please report it **responsibly**.

### Preferred Reporting Method
Email: haroonuint144@gmail.com


(Replace this with your actual contact email.)

### What to Include
Please include:
- A clear description of the vulnerability
- Steps to reproduce
- Potential impact
- Screenshots or proof-of-concept (if applicable)

---

## Responsible Disclosure Policy

- Please **do not** publicly disclose vulnerabilities before coordination
- We aim to acknowledge reports within **72 hours**
- We aim to provide a fix or mitigation plan within **14 days**

We appreciate responsible security research and will credit valid disclosures where appropriate.

---

## Out of Scope Vulnerabilities

The following are considered **out of scope**:
- Denial of Service (DoS) attacks
- Social engineering attacks
- Issues requiring physical access
- Vulnerabilities in third-party services or dependencies
- User-generated weak passwords (expected behavior)

---

## Future Security Roadmap

Planned security enhancements for future versions:
- Secure authentication (Argon2id / bcrypt)
- Rate limiting and brute-force protection
- Multi-factor authentication (MFA)
- ASVS Level 2 certification
- Automated dependency vulnerability scanning

---

## Acknowledgements

This project follows security-by-design principles and welcomes constructive security feedback from the community.

Thank you for helping keep this project secure.
