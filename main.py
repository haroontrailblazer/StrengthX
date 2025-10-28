import zxcvbn as zac
import hashlib
import re
import streamlit as st
from pwnedpasswords import pwnedpasswords as pwned

# --- Page Configuration ---
st.set_page_config(page_title="StrengthX - Strengthen Your Password",page_icon="🔒",layout="centered")
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- SEO META TAGS ---
st.markdown("""
<head>
  <title>StrengthX - Strengthen Your Password</title>
  <meta name="description" content="Check your password strength and improve your security with StrengthX — a simple, secure, and smart tool.">
  <meta name="keywords" content="password, security, password checker, password strength, StrengthX, Haroon K M">
  <meta name="robots" content="index, follow">
</head>
""", unsafe_allow_html=True)



# --- Custom CSS Styling ---
st.markdown("""
    <style>
        body {
            background-color: black;
            color: #d1d1d1;
        }
        .title {
            font-family: 'Trebuchet MS', sans-serif;
            color: #33ff99;
            font-size: 2.5em;
            font-weight: bold;
        }
        .subtitle {
            font-size: 1.1em;
            color: #888;
        }
        .box {
            border: 2px dashed #444;
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            color: #00ff88;
            font-size: 1.3em;
            margin-top: 20px;
        }
        .footer {
            text-align: center;
            color: #888;
            font-size: 0.9em;
            margin-top: 50px;
        }
        a {
            color: #33ff99 !important;
            text-decoration: none;
        }
    </style>
""", unsafe_allow_html=True)



st.markdown("<div class='title'>StrengthX</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Strengthen your password</div>", unsafe_allow_html=True)
st.markdown("<br> </br>", unsafe_allow_html=True)



# Example usage
# Prompting user for password input
pwd = st.text_input("🔍Know how secure is your password: ", type="password", placeholder="Enter Your Password")
if not pwd:
    st.info("Your passwords are never stored or transmitted in plain text. All evaluations are handled securely at every stage.")
    st.stop()
    
    
    
# Hashing the password using SHA-1 for pwnedpasswords check
pwdh = hashlib.sha1(pwd.encode("utf-8")).hexdigest().upper()


    
# Calling the evaluation function
eval= zac.zxcvbn(pwd)
cout= pwned.check(pwdh)
    
# collecting all the measures Available
regexeval=[]
Measures = [eval['guesses'],
            eval['guesses_log10'],
            eval['score'],
            eval['calc_time'],
            eval['crack_times_display'],
            eval['crack_times_seconds'],
            eval['password'],
            eval['sequence'],
            eval['feedback'],
            cout,]

# --- Display Breach Results ---
if Measures[9]>0:
    st.error(f"⚠️ This password has appeared **{Measures[9]:,} times** in data breaches! Choose a more unique password.")
else:
    st.success( "✅ Great! This password was not found in any known data breaches.")


    
# --- Password Strength Score Interpretation ---
if eval['score']==0:
    st.error(f"The password is very weak")
elif eval['score']==1:
    st.warning(f"The password is weak")
elif eval['score']==2:
    st.info(f"The password is fair")
elif eval['score']==3:
    st.success(f"The password is strong")
else:
    st.success(f"The password is very strong")
    


st.markdown("<br> </br>", unsafe_allow_html=True)
st.divider()
   
# --- Insights ---
st.markdown('<span style="color:#33ff99; font-size:1.5em;">Detailed Analysis </span>', unsafe_allow_html=True)
st.write(f"<span style='color:#5595d4'>***Crack Time :***</span>    {eval['crack_times_display']['offline_fast_hashing_1e10_per_second']}",unsafe_allow_html = True)
st.write(f"<span style='color:#5595d4'>***Feedback :***</span>    {Measures[8]['warning'] if Measures[8]['warning'] else 'No warnings'}",unsafe_allow_html = True)

suggestions = Measures[8].get('suggestions', []) if isinstance(Measures[8], dict) else Measures[8]
if isinstance(suggestions, list):
    suggestion_text = ", ".join(suggestions) if suggestions else "No suggestions"
else:
    suggestion_text = str(suggestions) if suggestions else "No suggestions"

st.write(f"<span style='color:#5595d4'>***Suggestion :***</span>    {suggestion_text}", unsafe_allow_html=True)

# --- Regex Evaluations ---

# checking for numbers
pattern1 = r'(?=.*\d)'
if not re.search(pattern1, pwd):
    regexeval.append('Add Numbers to your password')

# checking for length
if len(pwd) < 12:
    regexeval.append('Increase Length of your Password to at least 12 characters.')

# checking for uppercase letters
pattern2 = r'(?=.*[A-Z])'
if not re.search(pattern2, pwd):
    regexeval.append('Add Uppercase letters to your password')

# checking for special characters
pattern3 = r'[!@#$%^&*()_+{}\[\]:;"\'<>?,./`~\\|\-]'
if not re.search(pattern3, pwd):
    regexeval.append('Add Special Characters to your password')
    
# Displaying regex evaluation results
while True:
    if regexeval:
        st.markdown("<span style= 'color:#5595d4'>***Additional Recommendations:***</span>", unsafe_allow_html = True)
        for recommendation in regexeval:
            st.write(f"- {recommendation}")
    break
    
st.markdown("<br> </br>", unsafe_allow_html=True)

    
# --- Info Section ---
st.markdown("### <span style='color:#FF0000'>⚠️ Attention!!</span> ###", unsafe_allow_html = True)

st.markdown("""
**Using weak passwords:**  
Weak passwords like `123456` or `qwerty` are easy to guess and vulnerable to brute-force attacks.  
Avoid simplicity – it increases the risk of unauthorized access.

**Notice:**
Your passwords are never stored, never shared, and never transmitted in plain text.
All evaluations happen securely on your own device.
""",unsafe_allow_html = True)

st.divider()

# --- Footer ---
st.markdown("""
<div class="footer" style="background-color:black;color:#333;padding:18px;border-radius:12px;max-width:820px;margin:20px auto;text-align:center;font-family:Segoe UI, Tahoma, sans-serif;">
    <p style="margin:0 0 8px;font-size:14px;">
        <strong>Contact:</strong>
        <a href="mailto:hexra2025@gmail.com" style="color:#1a73e8;text-decoration:none;margin-left:8px;">hexra2025@gmail.com</a>
    </p>
    <p style="margin:0 0 12px;font-size:14px;">
        <a href="https://www.instagram.com/hexra_?igsh=dGFqY2MzMjQ1aGJo" target="_blank" style="color:#1a73e8;text-decoration:none;margin:0 8px;">Instagram</a> |
        <a href="https://github.com/haroontrailblazer" target="_blank" style="color:#1a73e8;text-decoration:none;margin:0 8px;">GitHub</a>
    </p>
    <hr style="border:none;border-top:1px solid #e6e6e6;margin:12px 0;">
    <p style="margin:8px 0 0;color:#555;font-size:13px;line-height:1.4;text-align:left;">
        <strong>About:</strong><br>
        StrengthX is a free, open-source password strength checker designed to help you create stronger passwords and enhance your online security.
    </p>
</div>
<br>
""", unsafe_allow_html=True)