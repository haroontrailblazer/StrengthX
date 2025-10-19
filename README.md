# StrengthX 🔒

![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg) 
![Python Version](https://img.shields.io/badge/Python-3.11+-blue.svg) 
![Contributors](https://img.shields.io/badge/Contributors-4-orange.svg) 

**StrengthX** is a web application that helps users evaluate the strength of their passwords and check if their passwords have been involved in known data breaches. It provides a quick and secure way to improve password security and promote safe online practices.  

---

## Features

- 🔍 **Password Strength Check**: Evaluates the complexity of the entered password.  
- ⚠️ **Breach Verification**: Checks how many times a password has been exposed in known data breaches.  
- 🔒 **Privacy-Focused**: Passwords are never stored in the backend; all checks are done securely.  
- 💻 **Interactive UI**: User-friendly interface for seamless password testing.  

---

## Contributors

- **Backend Developers**: Haroon K M, Balamurugan T
- **Frontend Developer**: Sujay S
- **Documentation**: Enbachozhan V

---

## Technology Stack

- **Backend**: Python  
- **Frontend**: Streamlit  
- **Libraries/Tools**: `zxcvbn`, `hashlib`, `pwnedpasswords` API  

---

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/haroontrailblazer/StrengthX.git
    ```
2. Navigate to the project folder:
    ```bash
    cd StrengthX
    ```
3. Create and activate a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate   # Linux/macOS
    venv\Scripts\activate      # Windows
    ```
4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Run the application:
    ```bash
    streamlit run app.py
    ```

---

## Usage

1. Enter a password in the input field.  
2. View the password strength score and suggestions to improve it.  
3. Check if the password has been exposed in data breaches.  
4. Adjust your password accordingly for better security.  

---

## Security & Privacy

- All passwords are processed locally in the browser or hashed before any breach verification.  
- No user passwords or sensitive information are stored on the server.  

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).  

---

## Contact

For queries or contributions, feel free to contact the contributors listed above or open an issue in the repository.

---

**StrengthX – Empowering safer online practices, one password at a time.**
