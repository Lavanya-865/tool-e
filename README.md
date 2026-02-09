# 🔧 Tool-E: Your AI Hardware Companion

> **"Hardware can be hard, but the help shouldn't be."**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://tool-e.streamlit.app)
[![Powered by Gemini](https://img.shields.io/badge/Powered%20by-Gemini%203%20Flash-blue)](https://deepmind.google/technologies/gemini/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-yellow)](https://www.python.org/)

**Tool-E** is an intelligent visual assistant that turns any confusing device—from lab equipment to washing machines—into a clear, step-by-step guide. It uses **Google Gemini 3 Flash** to "see" the device, detect safety hazards, and overlay interactive instructions.

## 🎥 Demo Video
[![Watch the Demo](https://img.youtube.com/vi/RZBE8wFieBA/0.jpg)](https://www.youtube.com/watch?v=RZBE8wFieBA)
*(Click the image above to watch the demo!)*

## 🚀 Live Demo
Try it out here: **[tool-e.streamlit.app](https://tool-e.streamlit.app)**

---

## 💡 Inspiration
We’ve all been there: staring at a washing machine with cryptic symbols, struggling to figure out a new coffee maker, or trying to help a grandparent use a TV remote over the phone.

The inspiration for **Tool-E** came from this simple observation: **Hardware can be hard, but the help shouldn't be.**

Whether it's a student facing complex lab equipment for the first time, a tourist trying to use a Japanese rice cooker, or someone with visual impairments needing audio guidance, the problem is universal. Manuals are often time-consuming, lost, confusing, or in the wrong language altogether. We wanted to build a bridge between humans and machines, an application that goes beyond simple translation to actually understand the device and guide you through it safely.

## 📱 What it does
Tool-E turns any confusing device into a clear, step-by-step guide.

1. **Snap & Analyze:** The user takes a photo of any device (kettle, microscope, fire extinguisher, etc.).
2. **Safety First Protocol:** Before giving any instructions, Tool-E scans the image for hazards (e.g., frayed cords, water damage, open valves) and warns the user immediately.
3. **AR-Style Visual Guides:** It overlays color-coded bounding boxes on the image (**Red** for hazards and **Green** for actionable steps) so users know exactly where to touch.
4. **Universal Translation:** It automatically detects the language of the device (e.g., Japanese labels) and translates the instructions into the user's preferred language.
5. **Accessibility Suite:**
    * **Audio Narration:** Converts written steps into speech for visually impaired users.
    * **Speed Control:** Allows users to speed up playback when in a rush.
    * **Offline Mode:** Users can download the audio instructions to save for later use without internet.

## 📸 Screenshots
![remote](https://github.com/user-attachments/assets/06cbedff-2ea6-4ed6-9665-9fb5dae74fb2)

![washing-machine](https://github.com/user-attachments/assets/9d428576-ad5f-4b65-ae7f-36a509e28490)

---

## 🧠 How It Works (Technical Deep Dive)

We built Tool-E using a modern, multimodal AI stack optimized for speed and accuracy.

### 1. The Brain: Google Gemini 3 Flash Preview
We utilized the multimodal capabilities of **Gemini 3 Flash** to send raw images and prompts simultaneously. The model returns a structured JSON response containing:
* Safety Ratings (PASS/FAIL)
* Detected Hazards
* Step-by-step instructions
* Precise coordinate data (`[ymin, xmin, ymax, xmax]`)

### 2. Coordinate Mapping & AR Overlay
Getting the AI to "point" at the right button was a key challenge. We refined our prompt to request specific bounding box coordinates on a normalized `0-1000` scale.
We then use **PIL (Python Imaging Library)** to map these to the user's image resolution ($W \times H$) using:
$$P_{pixel} = P_{norm} \times \frac{R_{dim}}{1000}$$

### 3. Audio & Accessibility
We integrated **gTTS (Google Text-to-Speech)** to dynamically generate audio files. To solve latency issues ($t > 3s$), we parallelized the text generation and audio conversion so visual steps appear instantly while audio loads in the background.

## 🛠️ Tech Stack

* **Core AI:** Google Gemini 3 Flash Preview
* **Frontend:** Streamlit (Python)
* **Image Processing:** Pillow (PIL)
* **Audio:** gTTS
* **Deployment:**
  
### 2. Install dependencies:
pip install -r requirements.txt

### 3. Set up API Keys: 
Create a .env file or use Streamlit secrets to add your Google Gemini API key:
GOOGLE_API_KEY="your_api_key_here"

### 4. Run the app:
streamlit run app.py

## 🚧 Challenges & Learnings
* **Hallucination vs. Safety:** Early on, the AI would suggest pressing non-existent buttons. We fixed this by implementing a "Strict Safety" system prompt.
* **Latency Matters:** Optimizing for **Gemini 3 Flash** was crucial to ensure users holding dangerous devices (like kettles) didn't have to wait 10+ seconds for an answer.
* **Empathy in Engineering:** Building for "Grandma" forced us to simplify the UI—if it takes more than 2 clicks, it's too complicated.

## 🔮 What's Next
* **Live AR Video Mode:** Moving from static photos to a live camera feed.
* **Haptic Feedback:** Adding vibration cues for blind users to help them locate buttons physically.
* **Community Guidebook:** Crowdsourcing successful scans into a public manual database.

---
### 🏆 Hackathon Project
Submitted for the **Gemini 3 Global Hackathon** (Feb 2026).
