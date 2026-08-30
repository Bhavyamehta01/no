import streamlit as st
import base64
import os

# Page config
st.set_page_config(
    page_title="💔",
    page_icon="💔",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS to completely style Streamlit elements
st.markdown("""
<style>
    /* Hide Streamlit default headers/footers */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Background and Layout settings */
    .stApp {
        background: linear-gradient(135deg, #FFD6E8 0%, #FFE8D6 30%, #F3E8FF 70%, #FFD6E8 100%);
        background-size: 300% 300%;
        animation: gradientShift 12s ease infinite;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }

    /* Style Streamlit Blocks */
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    /* Style Login Card Container */
    .login-container {
        max-width: 450px;
        margin: 8vh auto 2vh auto;
        padding: 2.5rem 2rem;
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 182, 211, 0.35);
        border-radius: 32px;
        box-shadow: 0 12px 48px rgba(232, 131, 158, 0.2);
        text-align: center;
    }

    .lock-icon {
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
        animation: floatIcon 3s ease-in-out infinite;
    }

    @keyframes floatIcon {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }

    .login-title {
        font-family: 'Dancing Script', cursive, sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #D4687E;
        margin-bottom: 0.5rem;
    }

    .login-subtitle {
        font-size: 0.95rem;
        color: #8E7080;
        margin-bottom: 2rem;
    }

    /* Style Streamlit Input Box */
    div[data-testid="stTextInput"] {
        margin-bottom: 1.5rem;
    }
    div[data-testid="stTextInput"] label {
        display: none !important;
    }
    div[data-testid="stTextInput"] input {
        border-radius: 16px !important;
        border: 2px solid rgba(255, 182, 211, 0.4) !important;
        background-color: rgba(255, 255, 255, 0.8) !important;
        color: #4A3040 !important;
        font-size: 1.1rem !important;
        text-align: center !important;
        padding: 0.8rem 1.2rem !important;
        letter-spacing: 4px !important;
        transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #E8839E !important;
        box-shadow: 0 0 0 4px rgba(232, 131, 158, 0.15) !important;
    }

    /* Style Streamlit Buttons */
    div[data-testid="stButton"] button {
        width: 100% !important;
        background: linear-gradient(135deg, #FFB6D3, #E8D5F5) !important;
        border: none !important;
        color: white !important;
        border-radius: 16px !important;
        padding: 0.8rem !important;
        font-family: 'Dancing Script', cursive !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 16px rgba(232, 131, 158, 0.3) !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease !important;
    }
    div[data-testid="stButton"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(232, 131, 158, 0.4) !important;
        color: white !important;
        border: none !important;
    }
    div[data-testid="stButton"] button:active {
        transform: translateY(0) !important;
        border: none !important;
    }

    /* Hint Box Style */
    .hint-box {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        padding: 0.8rem 1.2rem;
        background: linear-gradient(135deg, rgba(255, 214, 232, 0.3), rgba(232, 213, 245, 0.3));
        border-radius: 14px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 182, 211, 0.2);
    }

    .hint-text {
        font-size: 0.85rem;
        color: #6B4F5E;
        font-style: italic;
    }

    .bottom-deco {
        margin-top: 2rem;
        font-size: 0.82rem;
        color: #B8A0AD;
    }
</style>
""", unsafe_allow_html=True)

# Google fonts connection
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;500;600;700&family=Poppins:wght@300;400;500;600&family=Great+Vibes&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ===========================
# Session State for Login
# ===========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Background Floating Hearts Iframe (Runs in background of whole page)
BG_HEARTS_HTML = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            overflow: hidden;
            background: transparent;
        }
        .bg-hearts {
            position: fixed;
            top: 0; left: 0;
            width: 100vw; height: 100vh;
            pointer-events: none;
            overflow: hidden;
        }
        .bg-heart {
            position: absolute;
            opacity: 0;
            animation: floatUp var(--dur, 8s) var(--del, 0s) infinite ease-in;
        }
        @keyframes floatUp {
            0% { opacity: 0; transform: translateY(100vh) rotate(0deg) scale(0.5); }
            10% { opacity: 0.5; }
            90% { opacity: 0.4; }
            100% { opacity: 0; transform: translateY(-10vh) rotate(360deg) scale(1); }
        }
    </style>
</head>
<body>
    <div class="bg-hearts" id="bgHearts"></div>
    <script>
        const container = document.getElementById('bgHearts');
        const hearts = ['💕', '💗', '💖', '💓', '💘', '💝', '🩷', '♥'];
        for (let i = 0; i < 30; i++) {
            const el = document.createElement('div');
            el.classList.add('bg-heart');
            el.textContent = hearts[Math.floor(Math.random() * hearts.length)];
            el.style.left = Math.random() * 100 + '%';
            el.style.fontSize = (0.8 + Math.random() * 1.5) + 'rem';
            el.style.setProperty('--dur', (6 + Math.random() * 10) + 's');
            el.style.setProperty('--del', (Math.random() * 12) + 's');
            container.appendChild(el);
        }
    </script>
</body>
</html>
"""

PASSWORD = "no"

# ===========================
# LOGIN PAGE
# ===========================
if not st.session_state.logged_in:
    # Render Background Hearts Iframe ONLY on Login Page
    st.components.v1.html(BG_HEARTS_HTML, height=0, scrolling=False)
    st.markdown("""
    <style>
        iframe[title="st.components.v1.html"] {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: -1;
            pointer-events: none;
        }
    </style>
    """, unsafe_allow_html=True)

    # Spacer
    st.write("")
    
    # Custom HTML Card Structure
    st.markdown("""
    <div class="login-container">
        <div class="lock-icon">🔒</div>
        <div class="login-title">Yeh Sirf Tumhare Liye Hai...</div>
        <div class="login-subtitle">Andar jaane ke liye password daalo</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Text input and button in Streamlit
    col1, col2, col3 = st.columns([1, 2.2, 1])
    with col2:
        pwd = st.text_input(
            "Password",
            type="password",
            placeholder="Password enter karo...",
            key="pwd_input"
        )
        
        # Display Hint Box below input
        st.markdown("""
        <div class="hint-box">
            <span style="font-size:1.1rem;">💡</span>
            <span class="hint-text">Hint: Apka nickname hi password hai 😊</span>
        </div>
        """, unsafe_allow_html=True)
        
        submit = st.button("Kholein 💕")
        
        if submit or (pwd and pwd.strip().lower() == PASSWORD):
            if pwd.strip().lower() == PASSWORD:
                st.session_state.logged_in = True
                st.rerun()
            elif pwd:
                st.error("Galat password! Sochke dobara try karo 🥺")
                
    st.markdown("""
    <div style="text-align:center;">
        <p class="bottom-deco">💗 kuch khaas hai andar 💗</p>
    </div>
    """, unsafe_allow_html=True)

# ===========================
# MAIN PAGE (after login)
# ===========================
else:

    MAIN_HTML = """
    <!DOCTYPE html>
    <html lang="hi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;500;600;700&family=Poppins:wght@300;400;500;600&family=Great+Vibes&display=swap" rel="stylesheet">
        <style>
            :root {
                --pink-lightest: #FFF0F5;
                --pink-light: #FFD6E8;
                --pink: #FFB6D3;
                --pink-medium: #FF8FB8;
                --rose: #E8839E;
                --rose-dark: #D4687E;
                --peach: #FFDAB9;
                --peach-light: #FFE8D6;
                --lavender: #E8D5F5;
                --lavender-light: #F3E8FF;
                --cream: #FFF8F0;
                --warm-white: #FFFAF5;
                --text-dark: #4A3040;
                --text-medium: #6B4F5E;
                --text-light: #8E7080;
                --text-muted: #B8A0AD;
                --white: #FFFFFF;
                --shadow-soft: 0 4px 24px rgba(232, 131, 158, 0.15);
                --shadow-medium: 0 8px 32px rgba(232, 131, 158, 0.2);
                --shadow-heavy: 0 12px 48px rgba(232, 131, 158, 0.25);
                --gradient-hero: linear-gradient(135deg, #FFD6E8 0%, #FFE8D6 30%, #F3E8FF 70%, #FFD6E8 100%);
                --gradient-card: linear-gradient(145deg, rgba(255, 255, 255, 0.9), rgba(255, 240, 245, 0.7));
                --gradient-accent: linear-gradient(135deg, #FFB6D3, #E8D5F5);
                --radius-sm: 12px;
                --radius-md: 20px;
                --radius-lg: 32px;
                --font-display: 'Great Vibes', cursive;
                --font-heading: 'Dancing Script', cursive;
                --font-body: 'Poppins', sans-serif;
            }

            *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
            html { scroll-behavior: smooth; font-size: 16px; }

            body {
                font-family: var(--font-body);
                background-color: var(--warm-white);
                color: var(--text-dark);
                overflow-x: hidden;
                line-height: 1.7;
            }


            /* Floating Hearts */
            .floating-hearts {
                position: fixed; top: 0; left: 0;
                width: 100%; height: 100%;
                pointer-events: none; z-index: 1; overflow: hidden;
            }
            .floating-heart {
                position: absolute; font-size: 1.2rem; opacity: 0;
                animation: floatHeart var(--duration, 8s) var(--delay, 0s) infinite ease-in;
            }

            /* Hero */
            .hero {
                position: relative; min-height: 55vh;
                display: flex; align-items: center; justify-content: center;
                background: var(--gradient-hero);
                background-size: 300% 300%;
                animation: gradientShift 12s ease infinite;
                overflow: hidden;
            }
            .hero-overlay {
                position: absolute; inset: 0;
                background: radial-gradient(circle at 30% 50%, rgba(255,255,255,0.4) 0%, transparent 60%),
                            radial-gradient(circle at 70% 30%, rgba(243,232,255,0.3) 0%, transparent 50%);
            }
            .hero-content {
                position: relative; z-index: 2;
                text-align: center; padding: 2rem; max-width: 700px;
            }
            .hero-heart-icon {
                width: 100px; height: 100px;
                margin: 0 auto 2rem;
                animation: gentleFloat 4s ease-in-out infinite;
            }
            .broken-heart-svg {
                width: 100%; height: 100%;
                filter: drop-shadow(0 4px 12px rgba(232, 131, 158, 0.4));
            }
            .heart-left { animation: heartCrackLeft 3s ease-in-out infinite; transform-origin: right center; }
            .heart-right { animation: heartCrackRight 3s ease-in-out infinite; transform-origin: left center; }
            .hero-title { margin-bottom: 1.5rem; }
            .title-line-1 {
                display: block; font-family: var(--font-body);
                font-size: 1.2rem; font-weight: 300;
                color: var(--text-medium); letter-spacing: 3px;
                text-transform: uppercase; margin-bottom: 0.5rem;
                animation: fadeInUp 1s ease 0.5s both;
            }
            .title-line-2 {
                display: block; font-family: var(--font-heading);
                font-size: clamp(2.5rem, 6vw, 4rem); font-weight: 700;
                color: var(--rose-dark); line-height: 1.2;
                animation: fadeInUp 1s ease 0.8s both;
            }
            .hero-subtitle {
                font-family: var(--font-heading);
                font-size: clamp(1.3rem, 3vw, 1.8rem);
                color: var(--text-light); margin-bottom: 1.5rem;
                animation: fadeInUp 1s ease 1.1s both;
            }
            .scroll-indicator {
                animation: fadeInUp 1s ease 1.5s both;
                display: flex; flex-direction: column; align-items: center; gap: 0.5rem;
            }
            .scroll-indicator span {
                font-size: 0.85rem; color: var(--text-muted);
                letter-spacing: 2px; text-transform: uppercase;
            }
            .scroll-arrow {
                width: 24px; height: 24px; color: var(--rose);
                animation: bounceDown 2s ease-in-out infinite;
            }
            .scroll-arrow svg { width: 100%; height: 100%; }

            /* Section Shared */
            .section-container { max-width: 800px; margin: 0 auto; padding: 2.2rem 1.5rem; }
            .section-badge {
                display: inline-block; padding: 0.5rem 1.2rem;
                background: var(--gradient-accent); border-radius: 50px;
                font-size: 0.85rem; font-weight: 500;
                color: var(--white); margin-bottom: 1rem;
                box-shadow: var(--shadow-soft);
            }
            .section-title {
                font-family: var(--font-heading);
                font-size: clamp(2rem, 5vw, 3rem);
                color: var(--rose-dark); margin-bottom: 1.2rem;
                position: relative;
            }
            .section-title::after {
                content: ''; display: block; width: 60px; height: 3px;
                background: var(--gradient-accent); border-radius: 2px; margin-top: 0.8rem;
            }

            /* Sorry Section */
            .sorry-section { background: var(--warm-white); position: relative; }
            .sorry-section::before {
                content: ''; position: absolute;
                top: 0; left: 0; right: 0; height: 120px;
                background: linear-gradient(to bottom, var(--pink-lightest), transparent);
            }
            .sorry-card {
                background: var(--gradient-card);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 182, 211, 0.3);
                border-radius: var(--radius-lg);
                padding: 2rem 1.8rem;
                box-shadow: var(--shadow-medium);
                position: relative; overflow: hidden;
            }
            .sorry-card::before {
                content: ''; position: absolute;
                top: -50%; right: -50%; width: 200%; height: 200%;
                background: radial-gradient(circle, rgba(255, 214, 232, 0.2) 0%, transparent 60%);
                animation: cardGlow 6s ease-in-out infinite;
            }
            .sorry-icon { font-size: 3rem; margin-bottom: 1.5rem; animation: gentleFloat 3s ease-in-out infinite; }
            .sorry-text {
                font-size: 1.05rem; color: var(--text-medium);
                margin-bottom: 1.5rem; line-height: 1.9;
                position: relative; z-index: 1;
            }
            .sorry-text:last-child { margin-bottom: 0; }
            .highlight-text {
                background: linear-gradient(to bottom, transparent 60%, rgba(255, 182, 211, 0.3) 60%);
                display: inline; padding: 0 4px;
            }
            .highlight-text strong { color: var(--rose-dark); }

            /* Name Highlight */
            .name-glow {
                font-family: var(--font-display);
                font-size: 1.3em;
                color: var(--rose-dark);
                text-shadow: 0 0 20px rgba(232, 131, 158, 0.3);
            }

            /* Realize Section */
            .realize-section { background: linear-gradient(180deg, var(--warm-white) 0%, var(--pink-lightest) 100%); }
            .realize-cards { display: grid; gap: 1.5rem; }
            .realize-card {
                background: var(--white);
                border: 1px solid rgba(255, 182, 211, 0.2);
                border-radius: var(--radius-md);
                padding: 2rem 2rem 2rem 5rem;
                position: relative;
                box-shadow: var(--shadow-soft);
                transition: transform 0.4s ease, box-shadow 0.4s ease;
                opacity: 0; transform: translateX(-30px);
            }
            .realize-card.visible {
                opacity: 1; transform: translateX(0);
                transition: opacity 0.6s ease, transform 0.6s ease;
            }
            .realize-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-heavy); }
            .realize-number {
                position: absolute; left: 1.5rem; top: 2rem;
                font-family: var(--font-heading); font-size: 1.8rem;
                font-weight: 700; color: var(--pink); opacity: 0.6;
            }
            .realize-card h3 {
                font-family: var(--font-heading); font-size: 1.5rem;
                color: var(--rose-dark); margin-bottom: 0.5rem;
            }
            .realize-card p { font-size: 0.95rem; color: var(--text-medium); line-height: 1.8; }

            /* Promise Section */
            .promise-section { background: var(--pink-lightest); position: relative; }
            .promise-timeline { position: relative; padding-left: 2rem; }
            .promise-timeline::before {
                content: ''; position: absolute;
                left: 0; top: 0; bottom: 0; width: 3px;
                background: var(--gradient-accent); border-radius: 2px;
            }
            .promise-item {
                position: relative; margin-bottom: 1.5rem;
                opacity: 0; transform: translateY(20px);
            }
            .promise-item.visible {
                opacity: 1; transform: translateY(0);
                transition: opacity 0.6s ease, transform 0.6s ease;
            }
            .promise-item:last-child { margin-bottom: 0; }
            .promise-dot {
                position: absolute; left: -2rem; top: 0.5rem;
                width: 14px; height: 14px; border-radius: 50%;
                background: var(--rose); border: 3px solid var(--white);
                box-shadow: 0 0 0 3px rgba(232, 131, 158, 0.3);
                transform: translateX(-50%); z-index: 1;
            }
            .promise-content {
                background: var(--white); border-radius: var(--radius-md);
                padding: 1.8rem 2rem; box-shadow: var(--shadow-soft);
                margin-left: 1rem;
                border: 1px solid rgba(255, 182, 211, 0.15);
                transition: transform 0.3s ease;
            }
            .promise-content:hover { transform: translateX(8px); }
            .promise-content h3 {
                font-family: var(--font-heading); font-size: 1.4rem;
                color: var(--rose-dark); margin-bottom: 0.4rem;
            }
            .promise-content p { font-size: 0.95rem; color: var(--text-medium); line-height: 1.8; }

            /* Letter Section */
            .letter-section {
                background: linear-gradient(180deg, var(--pink-lightest) 0%, var(--lavender-light) 50%, var(--warm-white) 100%);
            }
            .letter-card {
                position: relative; background: var(--white);
                border-radius: var(--radius-lg); padding: 3rem;
                box-shadow: var(--shadow-heavy);
                border: 1px solid rgba(255, 182, 211, 0.2);
                min-height: 300px;
                display: flex; align-items: center; justify-content: center;
            }
            .letter-decoration {
                position: absolute; font-size: 4rem;
                color: var(--pink-light);
                font-family: var(--font-display);
                line-height: 1; opacity: 0.5;
            }
            .letter-decoration.top-left { top: 1rem; left: 1.5rem; }
            .letter-decoration.bottom-right { bottom: 1rem; right: 1.5rem; }
            .letter-body { width: 100%; text-align: center; position: relative; z-index: 1; }
            .letter-placeholder { padding: 2rem; }
            .placeholder-icon { font-size: 3.5rem; margin-bottom: 1rem; animation: gentleFloat 3s ease-in-out infinite; }
            .placeholder-text { font-family: var(--font-heading); font-size: 1.3rem; color: var(--text-muted); }
            .letter-image {
                width: 100%; max-width: 600px;
                border-radius: var(--radius-md);
                box-shadow: var(--shadow-soft);
            }

            /* Final Section */
            .final-section {
                background: var(--gradient-hero);
                background-size: 300% 300%;
                animation: gradientShift 12s ease infinite;
                position: relative; overflow: hidden;
            }
            .final-section::before {
                content: ''; position: absolute; inset: 0;
                background: radial-gradient(circle at 50% 100%, rgba(255,255,255,0.5) 0%, transparent 60%);
            }
            .final-content { text-align: center; position: relative; z-index: 2; }
            .final-emoji { font-size: 4rem; margin-bottom: 1.5rem; animation: gentleFloat 3s ease-in-out infinite; }
            .final-title {
                font-family: var(--font-heading);
                font-size: clamp(2.5rem, 6vw, 3.5rem);
                color: var(--rose-dark); margin-bottom: 2rem;
            }
            .final-text {
                font-size: 1.1rem; color: var(--text-medium);
                max-width: 600px; margin: 0 auto 1.5rem; line-height: 1.9;
            }
            .final-text strong { color: var(--rose-dark); font-weight: 600; }
            .final-highlight {
                background: rgba(255, 255, 255, 0.7);
                backdrop-filter: blur(10px);
                border-radius: var(--radius-md);
                padding: 2rem 2.5rem; margin: 2rem auto;
                max-width: 600px;
                border: 1px solid rgba(255, 182, 211, 0.3);
                box-shadow: var(--shadow-soft);
            }
            .final-highlight p {
                font-family: var(--font-heading);
                font-size: 1.4rem; color: var(--rose-dark); line-height: 1.6;
            }
            .final-signature { margin-top: 3rem; padding-top: 2rem; border-top: 1px solid rgba(232, 131, 158, 0.2); }
            .signature-from { font-family: var(--font-heading); font-size: 1.2rem; color: var(--text-light); }
            .signature-name { font-family: var(--font-display); font-size: 2.5rem; color: var(--rose-dark); margin-top: 0.3rem; }
            .final-hearts { margin-top: 2rem; display: flex; justify-content: center; gap: 1rem; font-size: 1.5rem; }
            .final-hearts span { animation: heartPulse 1.5s ease-in-out infinite; }
            .final-hearts span:nth-child(2) { animation-delay: 0.3s; }
            .final-hearts span:nth-child(3) { animation-delay: 0.6s; }

            /* Footer */
            .footer {
                text-align: center; padding: 2rem;
                background: var(--pink-lightest);
                border-top: 1px solid rgba(255, 182, 211, 0.2);
            }
            .footer p { font-size: 0.85rem; color: var(--text-muted); font-style: italic; }

            /* Keyframes */
            @keyframes gradientShift { 0%, 100% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } }
            @keyframes heartPulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.2); } }
            @keyframes gentleFloat { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
            @keyframes fadeInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
            @keyframes bounceDown { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(8px); } }
            @keyframes floatHeart {
                0% { opacity: 0; transform: translateY(100vh) rotate(0deg); }
                10% { opacity: 0.6; } 90% { opacity: 0.6; }
                100% { opacity: 0; transform: translateY(-10vh) rotate(360deg); }
            }
            @keyframes heartCrackLeft {
                0%, 40%, 100% { transform: translateX(0) rotate(0deg); }
                50% { transform: translateX(-2px) rotate(-3deg); }
                60% { transform: translateX(0) rotate(0deg); }
            }
            @keyframes heartCrackRight {
                0%, 40%, 100% { transform: translateX(0) rotate(0deg); }
                50% { transform: translateX(2px) rotate(3deg); }
                60% { transform: translateX(0) rotate(0deg); }
            }
            @keyframes cardGlow {
                0%, 100% { transform: translate(-10%, -10%) rotate(0deg); }
                50% { transform: translate(10%, 10%) rotate(180deg); }
            }

            .reveal { opacity: 0; transform: translateY(40px); transition: opacity 0.8s ease, transform 0.8s ease; }
            .reveal.visible { opacity: 1; transform: translateY(0); }

            @media (max-width: 768px) {
                .section-container { padding: 3.5rem 1.2rem; }
                .sorry-card { padding: 2rem 1.5rem; }
                .realize-card { padding: 1.5rem 1.5rem 1.5rem 4rem; }
                .realize-number { left: 1rem; font-size: 1.5rem; }
                .promise-content { padding: 1.5rem; }
                .letter-card { padding: 2rem 1.5rem; }
                .letter-decoration { font-size: 3rem; }
                .final-highlight { padding: 1.5rem; }
                .signature-name { font-size: 2rem; }
                .hero-heart-icon { width: 80px; height: 80px; }
            }
            @media (max-width: 480px) {
                html { font-size: 14px; }
                .section-container { padding: 3rem 1rem; }
                .sorry-card { padding: 1.5rem 1.2rem; }
                .promise-timeline { padding-left: 1.5rem; }
                .promise-dot { left: -1.5rem; width: 12px; height: 12px; }
                .promise-content { margin-left: 0.5rem; }
                .letter-card { padding: 1.5rem 1rem; }
            }

            ::selection { background: rgba(255, 182, 211, 0.4); color: var(--text-dark); }
            ::-webkit-scrollbar { width: 8px; }
            ::-webkit-scrollbar-track { background: var(--pink-lightest); }
            ::-webkit-scrollbar-thumb { background: var(--pink); border-radius: 4px; }
            ::-webkit-scrollbar-thumb:hover { background: var(--rose); }

            /* Gallery Styles */
            .gallery-container {
                width: 100%;
                background: var(--white);
                border-radius: var(--radius-lg);
                padding: 1.2rem;
                box-shadow: var(--shadow-heavy);
                border: 1px solid rgba(255, 182, 211, 0.2);
            }
            .gallery-tabs {
                display: flex;
                justify-content: center;
                gap: 0.8rem;
                margin-bottom: 2rem;
                flex-wrap: wrap;
            }
            .tab-btn {
                background: var(--pink-lightest);
                border: 1px solid rgba(255, 182, 211, 0.4);
                color: var(--text-medium);
                padding: 0.6rem 1.2rem;
                border-radius: 50px;
                font-family: var(--font-body);
                font-size: 0.9rem;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            .tab-btn:hover, .tab-btn.active {
                background: linear-gradient(135deg, #FFB6D3, #E8D5F5);
                color: white;
                box-shadow: var(--shadow-soft);
                border-color: transparent;
            }
            .gallery-content {
                position: relative;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 450px;
            }
            .gallery-item {
                display: none;
                width: 100%;
                max-width: 550px;
                text-align: center;
                animation: fadeIn 0.5s ease;
            }
            .gallery-item.active {
                display: block;
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .polaroid {
                background: white;
                padding: 1.2rem 1.2rem 2.5rem 1.2rem;
                border-radius: 8px;
                box-shadow: 0 8px 30px rgba(0,0,0,0.1);
                border: 1px solid #f0f0f0;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .image-wrapper {
                width: 100%;
                overflow: hidden;
                border-radius: 4px;
                background: #fafafa;
                display: flex;
                justify-content: center;
                align-items: center;
                max-height: 600px;
                margin-bottom: 1rem;
            }
            .gallery-img {
                max-width: 100%;
                max-height: 500px;
                object-fit: contain;
                border-radius: 2px;
                transition: transform 0.3s ease;
            }
            /* Default rotated for Page 2 */
            .rotated-default {
                transform: rotate(90deg);
            }
            .polaroid-caption {
                font-family: var(--font-heading);
                font-size: 1.5rem;
                color: var(--rose-dark);
                margin-top: 1rem;
                font-weight: 600;
            }
            .controls {
                display: flex;
                gap: 1rem;
                margin-top: 0.5rem;
                margin-bottom: 0.5rem;
            }
            .control-btn {
                background: rgba(232, 131, 158, 0.1);
                color: var(--rose-dark);
                border: 1px solid rgba(232, 131, 158, 0.3);
                padding: 0.4rem 1rem;
                border-radius: 8px;
                font-size: 0.85rem;
                cursor: pointer;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                gap: 0.3rem;
            }
            .control-btn:hover {
                background: var(--rose);
                color: white;
            }
            .zoomable {
                cursor: zoom-in;
            }
            .zoomable.zoomed {
                cursor: zoom-out;
                max-height: none;
                max-width: 150%;
            }

            /* Side scroll indicator */
            .side-scroll-indicator {
                position: fixed;
                right: 25px;
                top: 50%;
                transform: translateY(-50%) rotate(90deg);
                transform-origin: right center;
                font-family: var(--font-body);
                font-size: 0.8rem;
                font-weight: 600;
                letter-spacing: 2px;
                color: var(--rose-dark);
                z-index: 9999;
                display: flex;
                align-items: center;
                gap: 0.5rem;
                background: rgba(255, 255, 255, 0.85);
                padding: 0.5rem 1.2rem;
                border-radius: 20px;
                border: 1.5px solid rgba(255, 182, 211, 0.5);
                backdrop-filter: blur(10px);
                box-shadow: var(--shadow-medium);
                animation: sidePulse 2s ease-in-out infinite;
                white-space: nowrap;
                text-transform: uppercase;
            }

            @keyframes sidePulse {
                0%, 100% { transform: translateY(-50%) rotate(90deg) scale(1); }
                50% { transform: translateY(-50%) rotate(90deg) scale(1.08); }
            }
        </style>
    </head>
    <body>
        <!-- Floating Scroll Down Side Indicator -->
        <div class="side-scroll-indicator">Scroll Down 👇</div>

        <!-- Floating Hearts -->
        <div class="floating-hearts" id="floatingHearts"></div>


        <!-- Hero Section -->
        <section class="hero" id="hero">
            <div class="hero-overlay"></div>
            <div class="hero-content">
                <div class="hero-heart-icon">
                    <svg viewBox="0 0 100 100" class="broken-heart-svg">
                        <path d="M50 88 C25 65, 5 50, 5 30 C5 15, 18 5, 30 5 C38 5, 45 10, 50 18" fill="var(--rose-dark)" class="heart-left"/>
                        <path d="M50 88 C75 65, 95 50, 95 30 C95 15, 82 5, 70 5 C62 5, 55 10, 50 18" fill="var(--rose)" class="heart-right"/>
                    </svg>
                </div>
                <h1 class="hero-title">
                    <span class="title-line-1">Mujhe Pata Hai</span>
                    <span class="title-line-2">Maine Galti Ki Hai...</span>
                </h1>
                <p class="hero-subtitle">Par kya tum mujhe ek aur chance dogi, <span class="name-glow">No</span>?</p>
                <div class="scroll-indicator">
                    <span>Neeche scroll karo</span>
                    <div class="scroll-arrow">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 5v14M5 12l7 7 7-7"/>
                        </svg>
                    </div>
                </div>
            </div>
        </section>

        <!-- Sorry Section -->
        <section class="sorry-section" id="sorry">
            <div class="section-container">
                <div class="section-badge reveal">💔 Dil se...</div>
                <h2 class="section-title reveal">I'm Sorry, No</h2>
                <div class="sorry-card reveal">
                    <div class="sorry-icon">🥺</div>
                    <p class="sorry-text">
                        Main jaanta hoon ki maine bohot galat kiya hai. Tumhe hurt karna meri
                        zindagi ka sabse bada regret hai. Har din bina tumhare ek saza jaisi lagti hai.
                    </p>
                    <p class="sorry-text">
                        Tumhari har baat yaad aati hai — tumhara hasna, tumhara gussa karna,
                        tumhara mere upar trust karna... aur maine wo trust tod diya.
                    </p>
                    <p class="sorry-text highlight-text">
                        I know maafi maangne se sab theek nahi hota, par yeh dil se keh raha hoon —
                        <strong>I'm genuinely, deeply sorry.</strong>
                    </p>
                </div>
            </div>
        </section>

        <!-- Realize Section -->
        <section class="realize-section" id="realize">
            <div class="section-container">
                <div class="section-badge reveal">💭 Ab samajh aaya...</div>
                <h2 class="section-title reveal">Jo Maine Realize Kiya</h2>
                <div class="realize-cards">
                    <div class="realize-card" data-delay="0">
                        <div class="realize-number">01</div>
                        <h3>Tumhari Value</h3>
                        <p>Tumhe khokar samajh aaya ki tum mere liye kitni important ho.
                        Tum sirf meri GF nahi thi — tum meri best friend, meri support, meri duniya thi.</p>
                    </div>
                    <div class="realize-card" data-delay="200">
                        <div class="realize-number">02</div>
                        <h3>Meri Galtiyan</h3>
                        <p>Maine tumhe take for granted kiya. Tumhare feelings ko seriously nahi liya.
                        Yeh meri sabse badi galti thi aur main isko accept karta hoon.</p>
                    </div>
                    <div class="realize-card" data-delay="400">
                        <div class="realize-number">03</div>
                        <h3>Bina Tumhare Zindagi</h3>
                        <p>Bina tumhare sab kuch adhoora lagta hai. Woh subah ka pehla message,
                        raat ki lambi calls... sab kuch miss karta hoon.</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- Promise Section -->
        <section class="promise-section" id="promise">
            <div class="section-container">
                <div class="section-badge reveal">🤞 Waada...</div>
                <h2 class="section-title reveal">Agar Tum Ek Chance Do, No</h2>
                <div class="promise-timeline">
                    <div class="promise-item" data-delay="0">
                        <div class="promise-dot"></div>
                        <div class="promise-content">
                            <h3>Trust Wapas Banaunga</h3>
                            <p>Har din, har pal — actions se, sirf words se nahi. Tumhara trust
                            meri sabse badi zimmedari hogi.</p>
                        </div>
                    </div>
                    <div class="promise-item" data-delay="200">
                        <div class="promise-dot"></div>
                        <div class="promise-content">
                            <h3>Tumhe Priority Rakhunga</h3>
                            <p>Tum pehle, baaki sab baad mein. Tumhare feelings, tumhari needs —
                            sab kuch matter karega.</p>
                        </div>
                    </div>
                    <div class="promise-item" data-delay="400">
                        <div class="promise-dot"></div>
                        <div class="promise-content">
                            <h3>Better Insaan Banunga</h3>
                            <p>Sirf tumhare liye nahi, apne liye bhi. Main genuinely change hona chahta hoon
                            kyunki tum deserve karti ho ek better version of me.</p>
                        </div>
                    </div>
                    <div class="promise-item" data-delay="600">
                        <div class="promise-dot"></div>
                        <div class="promise-content">
                            <h3>Kabhi Phir Se Nahi</h3>
                            <p>Yeh galti dobara nahi hogi. Yeh waada nahi — yeh mera commitment hai
                            tumse aur khud se.</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Letter Section (Interactive Gallery) -->
        <section class="letter-section" id="letter">
            <div class="section-container">
                <div class="section-badge reveal">✉️ Tumhare liye...</div>
                <h2 class="section-title reveal">Dil Ki Baat</h2>
                <div class="gallery-container reveal">
                    <div class="gallery-tabs">
                        <button class="tab-btn active" onclick="switchGalleryTab(0)">🌸 Humare Moments</button>
                        <button class="tab-btn" onclick="switchGalleryTab(1)">📄 Letter Page 1</button>
                        <button class="tab-btn" onclick="switchGalleryTab(2)">📄 Letter Page 2</button>
                        <button class="tab-btn" onclick="switchGalleryTab(3)">📄 Letter Page 3</button>
                    </div>
                    
                    <div class="gallery-content">
                        <!-- Tab 0: Hands holding -->
                        <div class="gallery-item active">
                            <div class="polaroid">
                                <div class="image-wrapper">
                                    <img src="HANDS_IMAGE_PLACEHOLDER" alt="Moments" class="gallery-img">
                                </div>
                                <div class="polaroid-caption">Love Story (Fast Piano Ver.) 🎵</div>
                            </div>
                        </div>
                        
                        <!-- Tab 1: Letter page 1 -->
                        <div class="gallery-item">
                            <div class="polaroid">
                                <div class="image-wrapper">
                                    <img src="PAGE1_IMAGE_PLACEHOLDER" alt="Letter Page 1" class="gallery-img zoomable" id="img-page1" onclick="zoomImage('img-page1')">
                                </div>
                                <div class="controls">
                                    <button class="control-btn" onclick="rotateImage('img-page1', 90)">🔄 Rotate</button>
                                    <button class="control-btn" onclick="zoomImage('img-page1')">🔍 Zoom</button>
                                </div>
                                <div class="polaroid-caption">Sorry Nidhi ❤️ (Page 1)</div>
                            </div>
                        </div>
                        
                        <!-- Tab 2: Letter page 2 -->
                        <div class="gallery-item">
                            <div class="polaroid">
                                <div class="image-wrapper">
                                    <!-- Rotating by default by 90deg since it is sideways -->
                                    <img src="PAGE2_IMAGE_PLACEHOLDER" alt="Letter Page 2" class="gallery-img rotated-default zoomable" id="img-page2" onclick="zoomImage('img-page2')">
                                </div>
                                <div class="controls">
                                    <button class="control-btn" onclick="rotateImage('img-page2', 90)">🔄 Rotate</button>
                                    <button class="control-btn" onclick="zoomImage('img-page2')">🔍 Zoom</button>
                                </div>
                                <div class="polaroid-caption">Effort and Promises 🤞 (Page 2)</div>
                            </div>
                        </div>
                        
                        <!-- Tab 3: Letter page 3 -->
                        <div class="gallery-item">
                            <div class="polaroid">
                                <div class="image-wrapper">
                                    <img src="PAGE3_IMAGE_PLACEHOLDER" alt="Letter Page 3" class="gallery-img zoomable" id="img-page3" onclick="zoomImage('img-page3')">
                                </div>
                                <div class="controls">
                                    <button class="control-btn" onclick="rotateImage('img-page3', 90)">🔄 Rotate</button>
                                    <button class="control-btn" onclick="zoomImage('img-page3')">🔍 Zoom</button>
                                </div>
                                <div class="polaroid-caption">Someone who loves you lifetime ❤️ (Page 3)</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Final Section -->
        <section class="final-section" id="final">
            <div class="section-container">
                <div class="final-content">
                    <div class="final-emoji reveal">🙏</div>
                    <h2 class="final-title reveal">Bas Ek Aur Chance, No...</h2>
                    <p class="final-text reveal">
                        Main nahi jaanta ki tum yeh padhogi ya nahi. Main nahi jaanta ki tum
                        mujhe maaf karogi ya nahi. Par yeh sach hai ki —
                    </p>
                    <div class="final-highlight reveal">
                        <p>Tum meri zindagi ki sabse khoobsurat cheez ho, aur maine apni
                        stupidity se usse kho diya.</p>
                    </div>
                    <p class="final-text reveal">
                        Agar tumhare dil mein thodi si bhi jagah bachi hai mere liye,
                        toh please — <strong>ek aur chance de do.</strong>
                    </p>
                    <p class="final-text reveal">
                        Is baar main prove karunga. Sirf baaton se nahi, apne har action se.
                    </p>
                    <div class="final-signature reveal">
                        <p class="signature-from">— Tumhara hamesha,</p>
                        <p class="signature-name">Sorry 💔</p>
                    </div>
                </div>
                <div class="final-hearts">
                    <span>💗</span><span>💗</span><span>💗</span>
                </div>
            </div>
        </section>

        <!-- Footer -->
        <footer class="footer">
            <p>Made with a broken heart 💔 hoping it heals with your love 💗</p>
        </footer>

        <script>

            // Floating Hearts
            (function() {
                const container = document.getElementById('floatingHearts');
                const hearts = ['💕', '💗', '💖', '💓', '💘', '💝', '🩷', '♥'];
                for (let i = 0; i < 20; i++) {
                    const heart = document.createElement('div');
                    heart.classList.add('floating-heart');
                    heart.textContent = hearts[Math.floor(Math.random() * hearts.length)];
                    heart.style.left = Math.random() * 100 + '%';
                    heart.style.setProperty('--duration', (6 + Math.random() * 8) + 's');
                    heart.style.setProperty('--delay', (Math.random() * 10) + 's');
                    heart.style.fontSize = (0.8 + Math.random() * 1.2) + 'rem';
                    container.appendChild(heart);
                }
            })();

            // Scroll Reveal
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const delay = entry.target.getAttribute('data-delay') || 0;
                        setTimeout(() => { entry.target.classList.add('visible'); }, parseInt(delay));
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.15, rootMargin: '0px 0px -50px 0px' });

            document.querySelectorAll('.reveal, .realize-card, .promise-item').forEach(el => {
                observer.observe(el);
            });

            // Gallery Interactions (Rotate, Zoom, Tab Switch)
            let rotations = {};
            window.rotateImage = function(imgId, degrees) {
                const img = document.getElementById(imgId);
                if (!rotations[imgId]) {
                    rotations[imgId] = img.classList.contains('rotated-default') ? 90 : 0;
                }
                rotations[imgId] = (rotations[imgId] + degrees) % 360;
                updateImageStyle(img, imgId);
            };

            window.zoomImage = function(imgId) {
                const img = document.getElementById(imgId);
                img.classList.toggle('zoomed');
                updateImageStyle(img, imgId);
            };

            function updateImageStyle(img, imgId) {
                let rotation = rotations[imgId] !== undefined ? rotations[imgId] : (img.classList.contains('rotated-default') ? 90 : 0);
                let transform = `rotate(${rotation}deg)`;
                if (img.classList.contains('zoomed')) {
                    transform += " scale(1.5)";
                }
                img.style.transform = transform;
            }

            window.switchGalleryTab = function(index) {
                const items = document.querySelectorAll('.gallery-item');
                const tabs = document.querySelectorAll('.tab-btn');
                
                items.forEach((item, idx) => {
                    if (idx === index) {
                        item.classList.add('active');
                        tabs[idx].classList.add('active');
                    } else {
                        item.classList.remove('active');
                        tabs[idx].classList.remove('active');
                    }
                });
            };
        </script>
    </body>
    </html>
    """

    # Load and encode images to Base64
    def get_base64_image(file_name):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "images", file_name)
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                return f"data:image/png;base64,{base64.b64encode(img_file.read()).decode()}"
        return ""

    hands_base64 = get_base64_image("hands.png")
    page1_base64 = get_base64_image("page1.png")
    page2_base64 = get_base64_image("page2.png")
    page3_base64 = get_base64_image("page3.png")

    rendered_html = MAIN_HTML.replace("HANDS_IMAGE_PLACEHOLDER", hands_base64) \
                             .replace("PAGE1_IMAGE_PLACEHOLDER", page1_base64) \
                             .replace("PAGE2_IMAGE_PLACEHOLDER", page2_base64) \
                             .replace("PAGE3_IMAGE_PLACEHOLDER", page3_base64)

    st.components.v1.html(rendered_html, height=3800, scrolling=True)
