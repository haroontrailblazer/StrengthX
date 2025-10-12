import zxcvbn as zac
import hashlib
import re
import pwinput as pn
from pwnedpasswords import pwnedpasswords as pwned

# Example usage

while True:
    
    # Prompting user for password input
    pwd = pn.pwinput("Enter a password to evaluate (or 'exit' to quit): ",mask='*')
    if pwd.lower() =='exit':
        break
    
    # Validating password complexity
    pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$'
    
    # Regex pattern to ensure at least 8 characters, one uppercase letter, one digit, and one special character
    if not re.match(pattern, pwd):
        print("Password must be at least 8 characters long, contain at least one uppercase letter, one digit, and one special character.")
        continue
    
    # Hashing the password using SHA-1 for pwnedpasswords check
    pwdh = hashlib.sha1(pwd.encode("utf-8")).hexdigest().upper()
    
    # Calling the evaluation function
    eval= zac.zxcvbn(pwdh)
    cout= pwned.check(pwdh)
    
    # collecting all the measures Available
    Measures = [eval['guesses'],
                eval['guesses_log10'],
                eval['score'],
                eval['calc_time'],
                eval['crack_times_display'],
                eval['crack_times_seconds'],
                eval['password'],
                eval['sequence'],
                eval['feedback'],
                cout]
    
    print(f"Password has been found {cout} times in data breaches. Please choose a different password.")if cout > 0 else print("Password is strong and has not been found in data breaches.")