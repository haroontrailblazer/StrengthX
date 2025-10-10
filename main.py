import zxcvbn as zac
import hashlib
from pwnedpasswords import pwnedpasswords as pwned

# Example usage

while True:
    pwd = input("Enter a password to evaluate (or 'exit' to quit): ")
    pwdh = hashlib.sha1(pwd.encode("utf-8")).hexdigest().upper()
    if pwd.lower()=='exit':
        break
    
    # Calling the evaluation function
    eval= zac.zxcvbn(pwd)
    cout= pwned.check(pwd)
    
    # Displaying the results (result is between 0 and 4) Arguments: eval, feedback[warning, suggestions]
    Measures = [eval['guesses'],
                eval['guesses_log10'],
                eval['score'],
                eval['calc_time'],
                eval['crack_times_display'],
                eval['crack_times_seconds'],
                eval['password'],
                eval['sequence'],
                eval['feedback'],
                eval['match_sequence'],
                cout]
    print(f"the password has been found {cout} times in data breaches.") if cout>0 else "Good news: the password isnt found in data breaches."