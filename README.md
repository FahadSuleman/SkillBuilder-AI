# 🚀 SkillBuilder AI

**SkillBuilder AI** is a desktop app that helps users (especially beginners) create personalized learning roadmaps and get real-time help from an AI coach. It uses **Google Gemini AI** and is built with **Python** and **PyQt5**.

---

## 🔍 What It Does

- ✍️ **Creates personalized learning plans** for any topic (like Python, C++, etc.)
- 🧠 **AI Coach tab** for asking questions and getting helpful answers
- 🌐 **Supports multiple languages**
- 📄 **Nicely formatted output** (with headings, bullet points, arrows, and bold text)
- 💡 **Responsive design** (doesn’t freeze while loading AI responses)

---

## 🖥️ Technologies Used

- **Frontend**: PyQt5 (Python GUI)
- **Backend**: Google Gemini API
- **Language**: Python 3.10+
- **Other Tools**: markdown, requests

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/FahadSuleman/SkillBuilder-AI.git
cd skillbuilder-ai

```

### 2. Create and Activate Virtual Environment (Recommended)

```bash
# For Windows:
python -m venv venv
venv\Scripts\activate

# For macOS/Linux:
python3 -m venv venv
source venv/bin/activate

```

### 3. Install Required Packages

```bash
pip install -r requirements.txt

```

### 4. Add Your API Key

```bash
GEMINI_API_KEY=your_google_gemini_api_key

```

### 5. Run the App

```bash
python main.py

```
