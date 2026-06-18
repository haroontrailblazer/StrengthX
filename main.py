from pwnedpasswords import pwnedpasswords as pwned
from ollama import Client
import streamlit as st
import zxcvbn as zac
import hashlib
import math
import re
import os


# API configuration for the StrengthX AI password generator
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL")
client = Client(host=OLLAMA_API_URL)


# --- Page Configuration ---
st.set_page_config(
    page_title="StrengthX — Strengthen Your Password",
    page_icon="https://github.com/haroontrailblazer/haroontrailblazer/blob/main/Project%20Pngs/image.png?raw=true",
    layout="centered",
)

# --- SEO meta tags ---
st.markdown("""
<head>
  <title>StrengthX - Strengthen Your Password</title>
  <meta name="description" content="Check your password strength and improve your security with StrengthX — a simple, secure, and smart tool.">
  <meta name="keywords" content="password, security, password checker, password strength, StrengthX, Haroon K M">
  <meta name="robots" content="index, follow">
</head>
""", unsafe_allow_html=True)


# ---------- Inline SVG icon set (monoline, inherits currentColor) ----------
_SVG = {
    "shield":       '<path d="M12 3l7 3v5c0 4.6-3 7.6-7 9-4-1.4-7-4.4-7-9V6l7-3z"/>',
    "shield_check": '<path d="M12 3l7 3v5c0 4.6-3 7.6-7 9-4-1.4-7-4.4-7-9V6l7-3z"/><path d="M9 12l2 2 4-4.5"/>',
    "search":       '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
    "bolt":         '<path d="M13 2L4 14h7l-1 8 9-12h-7l1-8z"/>',
    "activity":     '<path d="M3 12h4l3 8 4-17 3 9h4"/>',
    "clock":        '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "key":          '<circle cx="8" cy="15" r="4.2"/><path d="M11 12l8.5-8.5"/><path d="M16.5 6l2 2"/><path d="M14 8.5l2 2"/>',
    "alert":        '<path d="M12 3.5l9.5 16.5H2.5z"/><path d="M12 10v4.5"/><circle cx="12" cy="17.6" r="0.7" fill="currentColor" stroke="none"/>',
    "check_circle": '<circle cx="12" cy="12" r="9"/><path d="M8.2 12.4l2.6 2.6 5-5.4"/>',
    "lock":         '<rect x="5" y="11" width="14" height="9" rx="2.2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    "github":       '<path d="M12 2a10 10 0 0 0-3.16 19.49c.5.09.68-.22.68-.48v-1.7c-2.78.6-3.37-1.34-3.37-1.34-.45-1.16-1.1-1.47-1.1-1.47-.9-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.9 1.52 2.34 1.08 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.94 0-1.09.39-1.98 1.03-2.68-.1-.25-.45-1.27.1-2.65 0 0 .84-.27 2.75 1.02a9.5 9.5 0 0 1 5 0c1.91-1.29 2.75-1.02 2.75-1.02.55 1.38.2 2.4.1 2.65.64.7 1.03 1.59 1.03 2.68 0 3.84-2.34 4.69-4.57 4.94.36.31.68.92.68 1.85v2.74c0 .27.18.58.69.48A10 10 0 0 0 12 2z" fill="currentColor" stroke="none"/>',
    "check":        '<path d="M5 12.5l4 4 10-10.5"/>',
    "minus":        '<path d="M6 12h12"/>',
    "arrow":        '<path d="M5 12h13"/><path d="M12 5l7 7-7 7"/>',
    "sparkles":     '<path d="M11 3.5l1.9 5.1L18 10.5l-5.1 1.9L11 17.5l-1.9-5.1L4 10.5l5.1-1.9z" fill="currentColor" stroke="none"/>'
                    '<path d="M18 13.5l.8 2.3 2.3.8-2.3.8-.8 2.3-.8-2.3-2.3-.8 2.3-.8z" fill="currentColor" stroke="none"/>',
    "robot":        '<rect x="4.5" y="7" width="15" height="11" rx="3.2"/><path d="M12 4.2V7"/>'
                    '<circle cx="12" cy="3.4" r="1.05" fill="currentColor" stroke="none"/>'
                    '<circle cx="9.2" cy="11.6" r="1.3" fill="currentColor" stroke="none"/>'
                    '<circle cx="14.8" cy="11.6" r="1.3" fill="currentColor" stroke="none"/>'
                    '<path d="M9.4 14.9c1.6 1.2 3.6 1.2 5.2 0"/>'
                    '<path d="M2.6 10.8v3.4"/><path d="M21.4 10.8v3.4"/>',
}


def ic(name, size=20, cls=""):
    return (f'<svg class="sx-ic {cls}" width="{size}" height="{size}" viewBox="0 0 24 24" '
            f'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
            f'stroke-linejoin="round">{_SVG[name]}</svg>')


# Score → (label, colour) — semantic, weak→strong
SCORE_META = {
    0: ("Very Weak", "#e5384d"),
    1: ("Weak", "#ff7a3d"),
    2: ("Fair", "#f5b000"),
    3: ("Strong", "#2bb673"),
    4: ("Very Strong", "#15a866"),
}


# --- Design System (CSS) — bold, vibrant, red (upGrad-style) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap');

:root {
    --ink:#16161a; --body:#454552; --muted:#71717f;
    --bg:#ffffff; --soft:#faf5f5; --card:#ffffff;
    --border:#ececf1; --border-2:#dedee6;
    --brand:#0bd97e; --brand-d:#06a163; --brand-2:#1cefbb;
    --brand-l:#e2faf1;
    --grad:linear-gradient(96deg,#0bd97e 0%,#1cefbb 100%);
    --good:#15a866; --good-l:#e7f7ef;
    --danger:#e5384d; --danger-l:#fdebed;
    --warn:#e0a800; --warn-l:#fef7e6;
    --shadow:0 14px 34px -16px rgba(40,16,18,0.18);
    --shadow-lg:0 34px 80px -30px rgba(40,16,18,0.28);
}
* { box-sizing:border-box; }
#MainMenu, header[data-testid="stHeader"], footer { visibility:hidden; }
[data-testid="stToolbar"], [data-testid="stDecoration"] { display:none; }

.stApp {
    background:
        radial-gradient(820px 440px at 92% -8%, rgba(28,239,187,0.13), transparent 58%),
        radial-gradient(720px 440px at 4% 0%, rgba(11,217,126,0.08), transparent 58%),
        var(--bg);
    color:var(--body);
    font-family:'Inter', system-ui, -apple-system, sans-serif;
    -webkit-font-smoothing:antialiased;
}
::selection { background:rgba(11,217,126,0.16); }
::-webkit-scrollbar { width:11px; }
::-webkit-scrollbar-thumb { background:#dcd6d7; border-radius:999px; }
::-webkit-scrollbar-thumb:hover { background:#c7bcbe; }

.block-container { max-width:1020px; padding-top:1.4rem; padding-bottom:3rem; }
.sx-ic { display:inline-block; vertical-align:middle; flex:none; }

label[data-baseweb="checkbox"] p, [data-testid="stToggle"] p, [data-testid="stWidgetLabel"] p { color:var(--muted) !important; font-weight:600; font-size:0.85rem; }

@keyframes sxUp { from{opacity:0; transform:translateY(15px);} to{opacity:1; transform:translateY(0);} }
.sx-anim { animation:sxUp .55s cubic-bezier(.2,.7,.2,1) both; }

/* ---------- Nav ---------- */
.sx-nav {
    position:sticky; top:0; z-index:100;
    display:flex; align-items:center; justify-content:space-between;
    padding:13px 22px; margin:0 0 8px;
    background:rgba(255,255,255,0.88); backdrop-filter:blur(14px); -webkit-backdrop-filter:blur(14px);
    border:1px solid var(--border); border-radius:18px; box-shadow:var(--shadow);
}
.sx-brand { display:flex; align-items:center; gap:11px; font-family:'Plus Jakarta Sans',sans-serif; font-weight:800; font-size:1.24rem; letter-spacing:-0.02em; color:var(--ink); }
.sx-brand .logo { width:37px; height:37px; border-radius:10px; object-fit:contain; background:rgba(255,255,255,0.04); box-shadow:0 9px 20px -7px rgba(11,217,126,0.45); }
.sx-brand .x { background:var(--grad); -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; }
.sx-nav-links { display:flex; align-items:center; gap:24px; font-size:0.92rem; font-weight:600; }
.sx-nav-links a { color:var(--body) !important; transition:color .2s; display:inline-flex; align-items:center; gap:6px; }
.sx-nav-links a:hover { color:var(--brand) !important; }
@media (max-width:800px){ .sx-nav-links a:not(.gh){ display:none; } }

/* ---------- Hero ---------- */
.sx-hero { text-align:center; padding:54px 16px 26px; }
.sx-eyebrow { display:inline-flex; align-items:center; gap:8px; font-size:0.74rem; font-weight:700; letter-spacing:0.09em; text-transform:uppercase; color:var(--brand); background:var(--brand-l); border:1px solid #f6cdcf; padding:8px 16px 8px 13px; border-radius:999px; }
.sx-headline { font-family:'Plus Jakarta Sans',sans-serif; font-weight:800; font-size:clamp(2.6rem,6.4vw,4.2rem); line-height:1.04; letter-spacing:-0.04em; margin:1.3rem 0 1rem; color:var(--ink); }
.sx-headline .hl { background:var(--grad); -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; }
.sx-lead { color:var(--muted); font-size:1.14rem; line-height:1.6; max-width:600px; margin:0 auto; }

/* ---------- Stats strip ---------- */
.sx-stats { display:grid; grid-template-columns:repeat(3,1fr); gap:0; background:var(--card); border:1px solid var(--border); border-radius:20px; box-shadow:var(--shadow); margin:24px auto 6px; max-width:680px; overflow:hidden; }
.sx-stat { text-align:center; padding:22px 14px; border-right:1px solid var(--border); }
.sx-stat:last-child { border-right:none; }
.sx-stat .num { font-family:'Plus Jakarta Sans',sans-serif; font-weight:800; font-size:1.9rem; letter-spacing:-0.02em; background:var(--grad); -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; }
.sx-stat .lbl { font-size:0.78rem; font-weight:600; color:var(--muted); margin-top:4px; }
@media (max-width:560px){ .sx-stats{ grid-template-columns:1fr; } .sx-stat{ border-right:none; border-bottom:1px solid var(--border);} .sx-stat:last-child{border-bottom:none;} }

/* ---------- Section ---------- */
.sx-section { background:var(--soft); border:1px solid var(--border); border-radius:28px; padding:36px 30px; margin:20px 0; }
.sx-kicker { text-align:center; font-size:0.74rem; font-weight:700; letter-spacing:0.2em; text-transform:uppercase; color:var(--brand); margin-bottom:6px; }
.sx-sec-title { text-align:center; font-family:'Plus Jakarta Sans',sans-serif; font-weight:800; font-size:1.9rem; letter-spacing:-0.025em; color:var(--ink); margin:0 0 26px; }
.sx-steps { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }
.sx-step { background:var(--card); border:1px solid var(--border); border-radius:20px; padding:28px 24px; transition:transform .22s, box-shadow .22s; }
.sx-step:hover { transform:translateY(-6px); box-shadow:var(--shadow-lg); }
.sx-step .badge { width:52px; height:52px; border-radius:15px; display:grid; place-items:center; color:#fff; background:var(--grad); box-shadow:0 12px 24px -8px rgba(11,217,126,0.55); }
.sx-step h4 { font-family:'Plus Jakarta Sans',sans-serif; font-weight:800; font-size:1.18rem; margin:18px 0 9px; color:var(--ink); }
.sx-step p { color:var(--muted); font-size:0.91rem; line-height:1.55; margin:0; }
@media (max-width:640px){ .sx-steps{ grid-template-columns:1fr; } }

/* ---------- Inline section heading ---------- */
.sx-h { font-family:'Plus Jakarta Sans',sans-serif; font-size:1.6rem; font-weight:800; letter-spacing:-0.025em; margin:36px 0 4px; color:var(--ink); }
.sx-h .hl { color:var(--brand); }
.sx-h-sub { color:var(--muted); font-size:0.96rem; margin:4px 0 0; }

/* ---------- Generic card ---------- */
.sx-card { background:var(--card); border:1px solid var(--border); border-radius:22px; padding:24px 26px; margin:14px 0; box-shadow:var(--shadow); }

/* ---------- Keyed containers ---------- */
.st-key-sx-scanner { background:var(--card); border:1px solid var(--border); border-radius:26px; padding:32px 32px !important; box-shadow:var(--shadow-lg); }
.st-key-sx-ai { background:var(--card); border:1px solid var(--border); border-radius:24px; padding:28px 32px !important; box-shadow:var(--shadow); }
.sx-scan-title { display:flex; align-items:center; gap:13px; font-family:'Plus Jakarta Sans',sans-serif; font-weight:800; font-size:1.4rem; margin:0 0 4px; color:var(--ink); }
.sx-scan-title .ico { width:44px; height:44px; border-radius:13px; display:grid; place-items:center; color:#fff; background:var(--grad); }
.sx-scan-desc { color:var(--muted); font-size:0.96rem; margin:0 0 18px; padding-left:57px; }

/* ---------- Text input ---------- */
[data-testid="stTextInput"] label { display:none; }
[data-testid="stTextInput"] div[data-baseweb="input"], [data-testid="stTextInput"] div[data-baseweb="base-input"] {
    background:#fdfbfb !important; border:1.6px solid var(--border-2) !important; border-radius:14px !important;
    transition:border-color .2s, box-shadow .2s;
}
[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within { border-color:var(--brand) !important; box-shadow:0 0 0 4px rgba(11,217,126,0.12) !important; }
[data-testid="stTextInput"] input { color:var(--ink) !important; font-family:'JetBrains Mono',monospace !important; font-size:1.06rem !important; letter-spacing:0.03em; padding:17px 15px !important; }
[data-testid="stTextInput"] input::placeholder { color:#a59b9c !important; font-family:'Inter',sans-serif !important; letter-spacing:normal; }

/* ---------- Empty state ---------- */
.sx-empty { display:flex; align-items:center; gap:14px; background:var(--soft); border:1px solid var(--border); border-radius:15px; padding:18px 20px; margin-top:6px; }
.sx-empty .ico { width:44px; height:44px; border-radius:12px; display:grid; place-items:center; color:var(--brand); background:var(--brand-l); flex:none; }
.sx-empty .t { color:var(--ink); font-weight:700; font-size:0.96rem; margin-bottom:2px; }
.sx-empty .d { color:var(--muted); font-size:0.86rem; line-height:1.5; }

/* ---------- Strength meter ---------- */
.sx-meter-head { display:flex; justify-content:space-between; align-items:baseline; margin-bottom:11px; }
.sx-meter-label { font-family:'Plus Jakarta Sans',sans-serif; font-size:1.7rem; font-weight:800; letter-spacing:-0.02em; }
.sx-meter-score { font-size:0.82rem; color:var(--muted); font-weight:700; font-family:'JetBrains Mono',monospace; }
.sx-meter { display:flex; gap:8px; }
.sx-seg { flex:1; height:12px; border-radius:999px; background:#eee9ea; transition:background .4s; }

/* ---------- Status banner ---------- */
.sx-status { display:flex; align-items:center; gap:14px; border-radius:17px; padding:18px 22px; margin:16px 0; border:1px solid var(--border); }
.sx-status .ico { flex:none; }
.sx-status.ok { background:var(--good-l); border-color:#bfe9d4; }
.sx-status.ok .ico { color:var(--good); }
.sx-status.bad { background:var(--danger-l); border-color:#f6c9ce; }
.sx-status.bad .ico { color:var(--danger); }
.sx-status-txt strong { display:block; font-size:1.06rem; margin-bottom:2px; color:var(--ink); }
.sx-status-txt span { color:var(--muted); font-size:0.89rem; line-height:1.5; }

/* ---------- Metric grid ---------- */
.sx-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin:16px 0; }
.sx-metric { background:var(--card); border:1px solid var(--border); border-radius:18px; padding:24px 16px; text-align:center; box-shadow:var(--shadow); transition:transform .2s; }
.sx-metric:hover { transform:translateY(-4px); }
.sx-metric .mic { width:42px; height:42px; margin:0 auto; border-radius:12px; display:grid; place-items:center; color:#fff; background:var(--grad); }
.sx-metric .mlabel { font-size:0.68rem; letter-spacing:0.12em; text-transform:uppercase; color:var(--muted); font-weight:700; margin-top:13px; }
.sx-metric .mval { font-family:'Plus Jakarta Sans',sans-serif; font-size:1.4rem; font-weight:800; margin-top:5px; color:var(--ink); }
.sx-metric .mval.accent { color:var(--brand); }
@media (max-width:560px){ .sx-grid{ grid-template-columns:1fr; } }

/* ---------- Insight rows ---------- */
.sx-insight { display:flex; gap:16px; padding:13px 0; border-bottom:1px solid var(--border); font-size:0.94rem; align-items:baseline; }
.sx-insight:last-child { border-bottom:none; }
.sx-insight .k { color:var(--brand); font-weight:700; min-width:108px; flex:none; }
.sx-insight .v { color:var(--body); line-height:1.5; }

/* ---------- Checklist ---------- */
.sx-check { display:flex; align-items:center; gap:14px; padding:12px 0; border-bottom:1px solid var(--border); }
.sx-check:last-child { border-bottom:none; }
.sx-check .dot { width:28px; height:28px; border-radius:9px; display:grid; place-items:center; flex:none; }
.sx-check.pass .dot { background:var(--good-l); color:var(--good); }
.sx-check.fail .dot { background:#f2eded; color:#a59b9c; }
.sx-check .ctext { font-size:0.96rem; color:var(--ink); font-weight:500; }
.sx-check.fail .ctext { color:var(--muted); font-weight:400; }

/* ---------- Button ---------- */
.stButton > button { width:100%; background:var(--grad); color:#fff !important; font-family:'Plus Jakarta Sans',sans-serif; font-weight:800; font-size:1.05rem; border:none; border-radius:13px; padding:0.9rem 1rem; transition:transform .15s, box-shadow .25s, filter .2s; box-shadow:0 18px 36px -14px rgba(11,217,126,0.7); }
.stButton > button:hover { transform:translateY(-2px); filter:brightness(1.05); box-shadow:0 24px 44px -14px rgba(11,217,126,0.8); }
.stButton > button:active { transform:translateY(0); }
.stButton > button:focus:not(:active) { color:#fff !important; }

[data-testid="stCode"] { border-radius:13px !important; border:1.6px solid var(--border-2) !important; background:#fdf8f8 !important; }
[data-testid="stCode"] code { font-family:'JetBrains Mono',monospace !important; font-size:1.06rem !important; color:var(--brand-d) !important; font-weight:700; }

/* ---------- Tips ---------- */
.sx-tip { display:flex; gap:16px; background:var(--warn-l); border:1px solid #f3e2b3; border-radius:18px; padding:22px 24px; margin:14px 0; }
.sx-tip .tic { color:var(--warn); flex:none; margin-top:1px; }
.sx-tip h4 { margin:0 0 8px; color:#9a7400; font-size:1.08rem; font-family:'Plus Jakarta Sans',sans-serif; font-weight:800; }
.sx-tip p { margin:7px 0; color:#6a5b35; font-size:0.92rem; line-height:1.55; }
.sx-tip code { background:#fbf2d6; padding:2px 8px; border-radius:6px; color:#8a6a00; font-family:'JetBrains Mono',monospace; font-size:0.85em; }

/* ---------- Footer ---------- */
.sx-footer { background:#16161a; border-radius:28px; margin-top:48px; padding:42px 36px 26px; color:#a7a7b2; }
.sx-footer-grid { display:flex; flex-wrap:wrap; justify-content:space-between; gap:30px; }
.sx-footer-brand { max-width:300px; }
.sx-footer-brand .b { display:flex; align-items:center; gap:11px; font-family:'Plus Jakarta Sans',sans-serif; font-weight:800; font-size:1.16rem; color:#fff; margin-bottom:12px; }
.sx-footer-brand .b .logo { width:31px; height:31px; border-radius:9px; display:grid; place-items:center; color:#fff; background:var(--grad); }
.sx-footer-brand p { color:#8a8a96; font-size:0.86rem; line-height:1.55; margin:0; }
.sx-fcol h5 { color:#fff; font-size:0.76rem; letter-spacing:0.12em; text-transform:uppercase; margin:0 0 14px; }
.sx-fcol a { display:flex; align-items:center; gap:7px; color:#9a9aa6 !important; font-size:0.89rem; margin-bottom:11px; transition:color .2s; }
.sx-fcol a:hover { color:var(--brand-2) !important; }
.sx-footer-bottom { display:flex; flex-wrap:wrap; justify-content:space-between; gap:10px; margin-top:30px; padding-top:20px; border-top:1px solid rgba(255,255,255,0.1); color:#71717f; font-size:0.8rem; }

a { color:var(--brand) !important; text-decoration:none; }
</style>
""", unsafe_allow_html=True)


# ---------- Nav ----------
st.markdown(f"""
<div class="sx-nav">
    <div class="sx-brand"><img class="logo" src="https://github.com/haroontrailblazer/haroontrailblazer/blob/main/Project%20Pngs/image.png?raw=true" alt="StrengthX"/>Strength<span class="x">X</span></div>
    <div class="sx-nav-links">
        <a class="gh" href="https://github.com/haroontrailblazer" target="_blank">{ic('github', 17)} GitHub</a>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------- Dark theme (applied site-wide) ----------
st.markdown("""
<style>
.stApp {
    --ink:#f2f4f8; --body:#bdc3ce; --muted:#888e9b;
    --bg:#0d0e13; --soft:#15171e; --card:#16181f;
    --border:rgba(255,255,255,0.10); --border-2:rgba(255,255,255,0.17);
    --brand:#2cf0a0; --brand-d:#1fd488; --brand-l:rgba(28,239,187,0.16);
    --good:#34d399; --good-l:rgba(52,211,153,0.15);
    --danger:#ff6b6b; --danger-l:rgba(255,107,107,0.14);
    --warn:#f5c451; --warn-l:rgba(245,196,81,0.12);
    --shadow:0 20px 48px -20px rgba(0,0,0,0.7); --shadow-lg:0 36px 84px -32px rgba(0,0,0,0.85);
}
.stApp .sx-nav { background:rgba(18,20,27,0.82) !important; }
.stApp [data-testid="stTextInput"] div[data-baseweb="input"],
.stApp [data-testid="stTextInput"] div[data-baseweb="base-input"] { background:#1b1d25 !important; }
.stApp [data-testid="stTextInput"] input { background:#1b1d25 !important; color:var(--ink) !important; }
.stApp [data-testid="stTextInput"] [data-baseweb="input"] svg,
.stApp [data-testid="stTextInput"] button svg { fill:var(--muted) !important; color:var(--muted) !important; }
.stApp [data-testid="stCode"] { background:#0b0c11 !important; }
.stApp .sx-seg { background:rgba(255,255,255,0.10); }
.stApp .sx-eyebrow { border-color:rgba(28,239,187,0.30); }
.stApp .sx-status.ok { border-color:rgba(52,211,153,0.32); }
.stApp .sx-status.bad { border-color:rgba(255,107,107,0.32); }
.stApp .sx-check.fail .dot { background:rgba(255,255,255,0.07); color:var(--muted); }
.stApp .sx-tip { border-color:rgba(245,196,81,0.26); }
.stApp .sx-tip h4 { color:var(--warn); }
.stApp .sx-tip p { color:var(--muted); }
.stApp .sx-tip code { background:rgba(245,196,81,0.14); color:var(--warn); }
</style>
""", unsafe_allow_html=True)


# ---------- Hero ----------
st.markdown(f"""
<div class="sx-hero sx-anim" id="analyzer">
    <span class="sx-eyebrow">{ic('shield_check', 14)} Smarter password security</span>
    <h1 class="sx-headline">How strong is your<br><span class="hl">password, really?</span></h1>
</div>
""", unsafe_allow_html=True)


# ---------- Scanner card (first card section) ----------
with st.container(key="sx-scanner"):
    st.markdown(f"""
    <div class="sx-scan-title"><span class="ico">{ic('search', 22)}</span> Password Analyzer</div>
    <div class="sx-scan-desc">Type a password to instantly see its strength, breach exposure and how long it would take to crack.</div>
    """, unsafe_allow_html=True)

    pwd = st.text_input(
        "Test your password",
        type="password",
        placeholder="Enter your password",
        key="pwd_input",
    )

    if not pwd:
        st.markdown(f"""
        <div class="sx-empty">
            <div class="ico">{ic('lock', 22)}</div>
            <div>
                <div class="t">Your password never leaves your control</div>
                <div class="d">Evaluated locally, never stored. Breach checks use k-anonymity — only a short hash prefix is sent, never your password.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def password_checklist(value: str):
    return [
        ("At least 12 characters long", len(value) >= 12),
        ("Contains a number", bool(re.search(r'\d', value))),
        ("Contains an uppercase letter", bool(re.search(r'[A-Z]', value))),
        ("Contains a lowercase letter", bool(re.search(r'[a-z]', value))),
        ("Contains a special character", bool(re.search(r'[!@#$%^&*()_+{}\[\]:;"\'<>?,./`~\\|\-]', value))),
    ]


# ---------- Results (shown once a password is entered) ----------
if pwd:
    pwdh = hashlib.sha1(pwd.encode("utf-8")).hexdigest().upper()  # SHA-1 only for HIBP interoperability
    evalpwd = zac.zxcvbn(pwd)
    cout = pwned.check(pwdh)

    score = evalpwd['score']
    label, color = SCORE_META.get(score, ("Unknown", "#888"))
    crack_time = evalpwd['crack_times_display']['offline_fast_hashing_1e10_per_second']
    entropy_bits = evalpwd['guesses_log10'] * math.log2(10)

    # Strength meter
    segments = "".join(
        f'<div class="sx-seg" style="background:{color};"></div>' if i <= score
        else '<div class="sx-seg"></div>'
        for i in range(5)
    )
    st.markdown(f"""
<div class="sx-card sx-anim">
    <div class="sx-meter-head">
        <span class="sx-meter-label" style="color:{color};">{label}</span>
        <span class="sx-meter-score">SCORE {score} / 4</span>
    </div>
    <div class="sx-meter">{segments}</div>
</div>
""", unsafe_allow_html=True)

    # Breach status
    if cout > 0:
        st.markdown(f"""
<div class="sx-status bad sx-anim">
    <span class="ico">{ic('alert', 26)}</span>
    <div class="sx-status-txt">
        <strong>Found in {cout:,} data breaches</strong>
        <span>This password is publicly known — choose a unique one you haven't used anywhere else.</span>
    </div>
</div>
""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
<div class="sx-status ok sx-anim">
    <span class="ico">{ic('check_circle', 26)}</span>
    <div class="sx-status-txt">
        <strong>No breaches found</strong>
        <span>This password was not found in any known data breach.</span>
    </div>
</div>
""", unsafe_allow_html=True)

    # Key metrics
    breach_val = f"{cout:,}" if cout > 0 else "0"
    breach_class = "" if cout > 0 else "accent"
    st.markdown(f"""
<div class="sx-grid sx-anim">
    <div class="sx-metric">
        <div class="mic">{ic('clock', 22)}</div><div class="mlabel">Crack Time</div>
        <div class="mval accent">{crack_time}</div>
    </div>
    <div class="sx-metric">
        <div class="mic">{ic('key', 22)}</div><div class="mlabel">Entropy</div>
        <div class="mval">{entropy_bits:.0f} bits</div>
    </div>
    <div class="sx-metric">
        <div class="mic">{ic('alert', 22)}</div><div class="mlabel">Breaches</div>
        <div class="mval {breach_class}">{breach_val}</div>
    </div>
</div>
""", unsafe_allow_html=True)

    # Security intelligence
    feedback = evalpwd['feedback']
    warning = feedback['warning'] if feedback.get('warning') else "No warnings — looking good."
    suggestions = feedback.get('suggestions', []) if isinstance(feedback, dict) else feedback
    if isinstance(suggestions, list):
        suggestion_text = " ".join(suggestions) if suggestions else "No further suggestions."
    else:
        suggestion_text = str(suggestions) if suggestions else "No further suggestions."

    st.markdown('<div class="sx-h">Security <span class="hl">Intelligence</span></div>', unsafe_allow_html=True)
    st.markdown(f"""
<div class="sx-card">
    <div class="sx-insight"><span class="k">Warning</span><span class="v">{warning}</span></div>
    <div class="sx-insight"><span class="k">Suggestion</span><span class="v">{suggestion_text}</span></div>
    <div class="sx-insight"><span class="k">Crack time</span><span class="v">{crack_time} &nbsp;·&nbsp; offline attack at 10 billion guesses / second</span></div>
</div>
""", unsafe_allow_html=True)

    # Recommendation checklist
    checks = password_checklist(pwd)
    rows = "".join(
        f'<div class="sx-check {"pass" if ok else "fail"}">'
        f'<div class="dot">{ic("check", 16) if ok else ic("minus", 16)}</div>'
        f'<div class="ctext">{text}</div></div>'
        for text, ok in checks
    )
    st.markdown('<div class="sx-h">Password <span class="hl">Checklist</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sx-card">{rows}</div>', unsafe_allow_html=True)


# ---------- How it works ----------
st.markdown(f"""
<div id="how-it-works" class="sx-section sx-anim">
    <div class="sx-kicker">How it works</div>
    <div class="sx-sec-title">Three steps to a safer password</div>
    <div class="sx-steps">
        <div class="sx-step">
            <div class="badge">{ic('activity', 24)}</div>
            <h4>Analyze</h4>
            <p>Real entropy scoring with zxcvbn, plus an honest estimate of how long your password survives an offline attack.</p>
        </div>
        <div class="sx-step">
            <div class="badge">{ic('shield_check', 24)}</div>
            <h4>Verify</h4>
            <p>Cross-checked against billions of breached passwords via Have I Been Pwned — using k-anonymity, never your raw password.</p>
        </div>
        <div class="sx-step">
            <div class="badge">{ic('bolt', 24)}</div>
            <h4>Generate</h4>
            <p>Summon StrengthX AI to instantly craft a unique, breach-resistant password you can copy in one click.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------- Stats strip ----------
st.markdown("""
<div class="sx-stats sx-anim">
    <div class="sx-stat"><div class="num">100%</div><div class="lbl">Local evaluation</div></div>
    <div class="sx-stat"><div class="num">0</div><div class="lbl">Passwords stored</div></div>
    <div class="sx-stat"><div class="num">ASVS&nbsp;L1</div><div class="lbl">OWASP aligned</div></div>
</div>
""", unsafe_allow_html=True)


# ---------- Tips ----------
st.markdown('<div class="sx-h">Stay <span class="hl">Safe</span></div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="sx-tip">
    <span class="tic">{ic('alert', 24)}</span>
    <div>
        <h4>Avoid weak passwords</h4>
        <p>Passwords like <code>123456</code> or <code>qwerty</code> are trivial to guess and crumble under
           brute-force attacks. Favour long, unpredictable passphrases over short, complex ones.</p>
        <p><strong style="color:var(--ink);">Privacy:</strong> Your passwords are never stored, never shared,
           and never transmitted in plain text. Every evaluation happens securely.</p>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------- Footer ----------
st.markdown(f"""
<div class="sx-footer">
    <div class="sx-footer-grid">
        <div class="sx-footer-brand">
            <div class="b"><span class="logo">{ic('shield', 17)}</span> StrengthX</div>
            <p>A free, open-source password strength checker with an integrated AI password generator —
               built to help you create stronger passwords and stay breach-resistant.</p>
        </div>
        <div class="sx-fcol">
            <h5>Product</h5>
            <a href="https://stats.uptimerobot.com/kVpen34aKT/" target="_blank">Service Status</a>
        </div>
        <div class="sx-fcol">
            <h5>Connect</h5>
            <a href="mailto:hexra2025@gmail.com">hexra2025@gmail.com</a>
            <a href="https://github.com/haroontrailblazer" target="_blank">{ic('github', 15)} GitHub</a>
            <a href="https://www.instagram.com/hexra_?igsh=dGFqY2MzMjQ1aGJo" target="_blank">Instagram</a>
        </div>
    </div>
    <div class="sx-footer-bottom">
        <span>© StrengthX · Apache 2.0 Licensed</span>
        <span>Aligned with OWASP ASVS v4.0.3 · Level 1</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------- Floating StrengthX AI bot (tap to open the AI pop-up) ----------
_BOT_ICON = ("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white'>"
             "<path d='M11 3.5l1.9 5.1L18 10.5l-5.1 1.9L11 17.5l-1.9-5.1L4 10.5l5.1-1.9z'/>"
             "<path d='M18 13.5l.8 2.3 2.3.8-2.3.8-.8 2.3-.8-2.3-2.3-.8 2.3-.8z'/></svg>")
st.markdown(f"""
<style>
.st-key-sx-bot {{ position:fixed; bottom:28px; right:28px; left:auto; width:auto !important; min-width:0 !important; z-index:999; }}
.st-key-sx-bot [data-testid="stPopoverButton"] {{
    width:88px !important; height:88px !important; min-height:88px !important; border-radius:50% !important;
    border:3px solid #fff !important; padding:0 !important; font-size:0 !important; color:transparent !important;
    background:url("{_BOT_ICON}") center / 40px no-repeat, linear-gradient(96deg,#0bd97e 0%,#1cefbb 100%) !important;
    box-shadow:0 20px 44px -10px rgba(11,217,126,0.55), 0 6px 16px rgba(0,0,0,0.12) !important;
    transition:transform .25s ease !important; animation:botPulse 2.6s ease-out infinite;
}}
.st-key-sx-bot [data-testid="stPopoverButton"]:hover {{ transform:translateY(-4px) scale(1.05); }}
.st-key-sx-bot [data-testid="stPopoverButton"] > * {{ display:none !important; }}
@keyframes botPulse {{
    0%   {{ box-shadow:0 20px 44px -10px rgba(11,217,126,0.55), 0 0 0 0 rgba(11,217,126,0.42); }}
    70%  {{ box-shadow:0 20px 44px -10px rgba(11,217,126,0.55), 0 0 0 18px rgba(11,217,126,0); }}
    100% {{ box-shadow:0 20px 44px -10px rgba(11,217,126,0.55), 0 0 0 0 rgba(11,217,126,0); }}
}}
.sx-bot-head {{ display:flex; align-items:center; gap:11px; margin-bottom:6px; }}
.sx-bot-ava {{ width:40px; height:40px; border-radius:50%; flex:none; background:var(--grad); color:#fff; display:grid; place-items:center; }}
.sx-bot-ava svg {{ width:23px; height:23px; }}
.sx-bot-title {{ font-family:'Plus Jakarta Sans',sans-serif; font-weight:800; font-size:1rem; color:var(--ink); line-height:1.1; }}
.sx-bot-sub {{ font-size:0.78rem; color:var(--muted); margin-top:2px; }}
.small-emoji-btn {{ display:none; }}
@media (max-width:600px){{ .st-key-sx-bot {{ bottom:18px; right:18px; }} }}
</style>
""", unsafe_allow_html=True)

with st.container(key="sx-bot"):
    with st.popover("AI", use_container_width=False):
        st.markdown(f"""
        <div class="sx-bot-head">
            <div class="sx-bot-ava">{ic('sparkles', 23)}</div>
            <div>
                <div class="sx-bot-title">StrengthX AI</div>
                <div class="sx-bot-sub">Generate a strong password</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        bot_trigger = st.button("⚡ Generate Password", key="bot_trigger", use_container_width=True)
        if st.session_state.get("generated_password"):
            st.markdown('<p style="color:var(--muted); font-size:0.8rem; margin:12px 0 4px; font-weight:600;">Your password — click to copy:</p>', unsafe_allow_html=True)
            st.code(st.session_state.generated_password, language=None)
        elif st.session_state.get("gen_error"):
            st.error("Couldn't reach StrengthX AI. Please try again.")


# ---------- Mobile optimisation (kept last so it wins the cascade) ----------
st.markdown("""
<style>
@media (max-width: 640px) {
    .block-container { padding-top:0.7rem; padding-left:0.6rem; padding-right:0.6rem; }
    .sx-nav { padding:10px 15px; }
    .sx-brand { font-size:1.05rem; gap:9px; }
    .sx-brand .logo { width:31px; height:31px; }
    .sx-nav-links { gap:14px; font-size:0.85rem; }
    .sx-hero { padding:26px 4px 14px; }
    .sx-headline { font-size:2.05rem; line-height:1.08; margin:0.9rem 0 0.7rem; }
    .sx-eyebrow { font-size:0.62rem; letter-spacing:0.05em; padding:6px 12px; }
    .sx-stat { padding:15px 8px; }
    .sx-stat .num { font-size:1.45rem; }
    .sx-section { padding:24px 15px; border-radius:20px; margin:14px 0; }
    .sx-kicker { font-size:0.66rem; }
    .sx-sec-title { font-size:1.4rem; margin-bottom:18px; }
    .sx-step { padding:20px 17px; }
    .st-key-sx-scanner { padding:20px 17px !important; border-radius:20px; }
    .st-key-sx-ai { padding:20px 17px !important; }
    .sx-scan-title { font-size:1.12rem; gap:10px; }
    .sx-scan-title .ico { width:36px; height:36px; }
    .sx-scan-desc { padding-left:0; margin-top:8px; font-size:0.88rem; }
    .sx-card { padding:18px 16px; border-radius:16px; }
    .sx-h { font-size:1.28rem; margin:26px 0 2px; }
    .sx-meter-label { font-size:1.35rem; }
    .sx-status { padding:15px 16px; gap:12px; }
    .sx-status-txt strong { font-size:0.96rem; }
    .sx-insight { flex-direction:column; gap:3px; }
    .sx-insight .k { min-width:0; }
    .sx-tip { padding:18px 17px; gap:13px; }
    .sx-footer { padding:28px 20px 18px; border-radius:20px; margin-top:34px; }
    .sx-footer-grid { gap:22px; }
    .sx-footer-brand { max-width:none; }
    .st-key-sx-bot { bottom:16px !important; right:16px !important; }
    .st-key-sx-bot [data-testid="stPopoverButton"] {
        width:60px !important; height:60px !important; min-height:60px !important;
        background-size:26px 26px, cover !important;
    }
}
</style>
""", unsafe_allow_html=True)


# ---------- AI generation handler ----------
if bot_trigger:
    # AI complex password generator (haroontrailblazer/StrengthX-Dildo:V1)
    # Model reference: https://ollama.com/haroontrailblazer/StrengthX-Dildo
    try:
        response = client.chat(model='haroontrailblazer/StrengthX-Dildo:V1', messages=[{
            'role': 'user',
            'content': 'Generate a strong password and display only the password, no explanations, no extra text, and nothing else under any circumstances, Dont regenerate any password everytime generate a unique one and always generate minimum length of 16.'
        }])
        st.session_state.generated_password = response['message']['content']
        st.session_state.gen_error = False
        st.rerun()
    except Exception as e:
        st.session_state.generated_password = ""
        st.session_state.gen_error = True
        st.rerun()
