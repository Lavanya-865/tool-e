import streamlit as st
from google import genai
from google.genai import types
from PIL import Image, ImageDraw, ImageFont
import json
import os
from gtts import gTTS
import io
import base64

# ==========================================
# 🎨 1. UI CONFIGURATION (MUST BE FIRST)
# ==========================================
st.set_page_config(
    page_title="Tool-E",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="auto"  # Changed to 'auto' for better mobile behavior
)

# Helper to load image for the header
def get_img_as_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except: return None

# Load the robot image
img_b64 = get_img_as_base64("toole.png")
img_html = f'<img src="data:image/png;base64,{img_b64}" width="85" style="vertical-align: middle; margin-right: 15px;">' if img_b64 else "🤖"

# ==========================================
# ⚙️ CONFIGURATION
# ==========================================

# 1. API KEY SETUP
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.warning("⚠️ Secrets not found. Using placeholder key.")
    API_KEY = "PASTE_YOUR_KEY_HERE"

MODEL_ID = "gemini-3-flash-preview"
client = genai.Client(api_key=API_KEY)

# ==========================================
# 🧠 AI LOGIC
# ==========================================

def get_ai_instruction(image, user_goal, language="English"):
    prompt_text = f"""
    You are Tool-E, a helpful robot assistant.
    User Goal: "{user_goal}"
    Target Language: "{language}"
    
    Look at the image. 
    1. IDENTIFY the device.
    2. CHECK for IMMEDIATE physical hazards (fire, shock, gas).
       * IGNORE general health advice (volume, posture).
    3. Identify the EXACT controls/buttons needed.
    
    CRITICAL: Return pure JSON.
    
    JSON Structure:
    {{
        "device_name": "Name of the object (Translated to {language})",
        "risk_alert": "Warning text (Translated to {language}) or null",
        "steps": [
            {{
                "order": 1,
                "text": "Instruction (Translated to {language})",
                "action_type": "tap", 
                "box_2d": [ymin, xmin, ymax, xmax] 
            }}
        ]
    }}
    
    RULES:
    * "action_type": "tap", "hold", "rotate", "swipe".
    * box_2d: 0-1000 scale.
    """
    import time
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=[image, prompt_text],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            data = json.loads(response.text)
            if isinstance(data, list): data = data[0]
            return data
        except Exception as e:
            time.sleep(1)
            continue
    return {"error": "Server busy"}

def text_to_speech(text, lang_code='en'):
    try:
        tts = gTTS(text=text, lang=lang_code)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return audio_fp
    except: return None

# ==========================================
# 🎨 UI & CSS
# ==========================================

st.markdown("""
    <style>
    /* Import Google Font: Outfit */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* REMOVED THE HEADER HIDING CODE TO FIX SIDEBAR */
    /* #MainMenu {visibility: hidden;} */
    /* header {visibility: hidden;} */
    
    /* Header Container */
    .header-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding-bottom: 10px;
    }
    
    .title-text {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        background: -webkit-linear-gradient(45deg, #007BFF, #00E5FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .subtitle-text {
        font-size: 1.2rem;
        color: #888;
        text-align: center;
        margin-top: -5px;
        margin-bottom: 20px;
        letter-spacing: 1px;
    }
    
    /* 📸 CAMERA FIX: HARD FORCE HEIGHT */
    /* This targets the inner video element specifically */
    div[data-testid="stCameraInput"] video {
        object-fit: cover !important;
        height: 450px !important; /* Force tall height */
        width: 100% !important;
        border-radius: 20px !important;
    }
    
    /* Bigger "Take Photo" Button */
    button[kind="primary"] {
        background-color: #007BFF !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 15px 30px !important;
        font-size: 1.2rem !important;
        width: 100% !important;
    }

    /* 🟩 STEP CARDS */
    .step-card {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
        border-left: 5px solid #00E5FF;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# HEADER
st.markdown(f"""
<div class="header-container">
    {img_html}
    <h1 class="title-text">Tool-E</h1>
</div>
<p class="subtitle-text">Your Everything Guide 🌍</p>
""", unsafe_allow_html=True)

# ==========================================
# ⚙️ SIDEBAR
# ==========================================
with st.sidebar:
    st.header("⚙️ Settings")
    
    # 1. LANGUAGE MAPPING
    lang_map = {
        "English": "en",
        "Hindi": "hi", 
        "Tamil": "ta",
        "Telugu": "te",
        "French": "fr",
        "Russian": "ru",
        "Japanese": "ja",
        "Chinese": "zh-CN"
    }
    selected_lang = st.selectbox("Language", list(lang_map.keys()))
    lang_code = lang_map[selected_lang]
    
    st.divider()
    
    # 2. INPUT MODE
    input_mode = st.radio("Input Mode", ["Live Scanner", "Native Camera 📸"])
    
    st.success(f"✅ Mode: {selected_lang}")
    st.caption("🛡️ Safety Guard Active")

# ==========================================
# 📱 MAIN UI
# ==========================================

col1, col2 = st.columns(2)
with col1:
    goal = st.text_input("Goal", "How do I use this?")
with col2:
    if input_mode == "Live Scanner":
        st.info("📸 Point camera at device")
    else:
        st.info("⬆️ Tap to use Phone Camera")

# HANDLE INPUT
img_file = None
if input_mode == "Live Scanner":
    img_file = st.camera_input("Scanner", label_visibility="collapsed")
else:
    img_file = st.file_uploader("Take a photo", type=['jpg', 'png', 'jpeg'], label_visibility="collapsed")

# ==========================================
# 🚀 PROCESSING
# ==========================================
if img_file and goal:
    image = Image.open(img_file)
    
    with st.spinner("Analyzing & Translating..."):
        data = get_ai_instruction(image, goal, selected_lang)
        
        if "error" in data:
            st.error(f"Error: {data['error']}")
        else:
            risk = data.get("risk_alert")
            device_name = data.get("device_name", "Device")
            steps = data.get("steps", [])
            
            # 1. DISPLAY STATUS
            if risk:
                st.error(f"⚠️ {risk}")
            else:
                st.success(f"📱 {device_name}")

            # 2. GENERATE AUDIO
            full_audio_text = f"{device_name}. "
            if risk:
                full_audio_text += f"Warning: {risk}. "
            
            full_audio_text += "Instructions: "
            for step in steps:
                full_audio_text += f"Step {step['order']}: {step['text']}. "

            # 3. PLAY AUDIO
            audio_bytes = text_to_speech(full_audio_text, lang_code)
            if audio_bytes:
                st.audio(audio_bytes, format='audio/mp3', start_time=0)

            # 4. DRAWING BOXES
            draw = ImageDraw.Draw(image)
            width, height = image.size
            try: font = ImageFont.truetype("arial.ttf", 20)
            except: font = ImageFont.load_default()

            for step in steps:
                ymin, xmin, ymax, xmax = step["box_2d"]
                action = step.get("action_type", "tap").lower()
                
                # Colors
                if risk: color = "#FF0000"
                elif "hold" in action: color = "#FFFF00"
                elif "rotate" in action: color = "#00FFFF"
                else: color = "#00FF00"

                # Box
                box = [xmin/1000 * width, ymin/1000 * height, xmax/1000 * width, ymax/1000 * height]
                draw.rectangle(box, outline=color, width=5)
                
                # Label
                label = str(step['order'])
                if "hold" in action: label += " ✋"
                
                # Text Background
                text_bbox = draw.textbbox((0, 0), label, font=font)
                text_w = text_bbox[2] - text_bbox[0]
                text_h = text_bbox[3] - text_bbox[1]
                text_pos = [box[0], max(0, box[1] - text_h - 10)]
                draw.rectangle([text_pos[0], text_pos[1], text_pos[0]+text_w+10, text_pos[1]+text_h+10], fill=color)
                draw.text((text_pos[0]+5, text_pos[1]), label, fill="black", font=font)

            # 5. SHOW IMAGE
            st.image(image, use_container_width=True)
            
            # 6. SHOW STEPS IN CARDS
            st.markdown("### 📝 Steps")
            for step in steps:
                st.markdown(f"""
                <div class="step-card">
                    <strong style='font-size:1.1rem;'>Step {step['order']}</strong><br>
                    {step['text']}
                </div>
                """, unsafe_allow_html=True)
