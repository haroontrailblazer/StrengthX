import zxcvbn as zac

# Password strength evaluation function

def eval_pass_strength(password):
    result = zac.zxcvbn(password)
    score = result['score']
    feedback = result['feedback']
    return score, feedback

# Example usage

while True:
    pwd = input("Enter a password to evaluate (or 'exit' to quit): ")
    if pwd.lower()=='exit':
        break
    
    # Calling the evaluation function
    
    eval,fb = eval_pass_strength(pwd)
    
    # Displaying the results (result is between 0 and 4) Arguments: eval, feedback[warning, suggestions]
    
    print(f"Password Strength Score (0-4): {eval}")
    print(f"Feedback: {fb['warning']}")
    print(f"Suggestions: {fb['suggestions'] if fb['suggestions'] else 'None'}\n")