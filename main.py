import zxcvbn as zac

# Example usage

while True:
    pwd = input("Enter a password to evaluate (or 'exit' to quit): ")
    if pwd.lower()=='exit':
        break
    
    # Calling the evaluation function
    
    eval= zac.zxcvbn(pwd)
    
    # Displaying the results (result is between 0 and 4) Arguments: eval, feedback[warning, suggestions]
    feedback = eval['feedback']
    print(f"Password strength score (0-4): {eval['score']}")
    print(f"Feedback: {feedback['warning']}")
    print(f' Suggestions: {feedback["suggestions"] if feedback["suggestions"] else "None"}')
    print(f"Estimated guesses: {eval['guesses']}")
    print(f"Estimated crack time (seconds): {eval['crack_times_seconds']}")