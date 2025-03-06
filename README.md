# 🎯 BriefMe Brilliantly

An AI-powered meeting preparation assistant built with Streamlit that helps you get comprehensive briefings on people and companies before your meetings.

## 📋 Description

BriefMe Brilliantly is your pre-meeting intelligence partner designed to make you the most prepared person in the room. The application connects to an AI backend via API to generate detailed briefings about companies and individuals you're meeting with, saving you time on research and helping you make better impressions.

## ✨ Features

- **Company Deep Dives**: Get quick insights on any organization
- **People Intelligence**: Learn about who you're meeting with before you shake hands
- **LinkedIn Reconnaissance**: Find professional backgrounds without endless scrolling
- **Meeting Prep Made Easy**: Comprehensive briefings delivered through a chat interface
- **Secure Authentication**: API key-based authentication system
- **Session Persistence**: Option to remember login credentials between sessions
- **Responsive UI**: Clean, intuitive interface built with Streamlit

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/briefme-brilliantly.git
cd briefme-brilliantly
```

2. Set up a Python 12 virtual environment:
```bash
# For macOS/Linux
python3.12 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

> **Note**: This application is optimized for Python 12. Using earlier versions may result in compatibility issues.

## 🔧 Configuration

You'll need:
- An API URL endpoint that accepts the briefing requests
- A bearer token for authentication

These credentials are entered directly in the application's login screen.

## 💻 Usage

1. Start the Streamlit application:
```bash
streamlit run BriefMe.py
```

2. Open your browser and navigate to the provided URL (typically http://localhost:8501)

3. Enter your API URL and bearer token on the login screen

4. Once logged in, simply type who you're meeting with and their company, for example:
   > "I'm meeting with Sarah Johnson and Michael Lee from Acme Corporation tomorrow."

5. The application will generate a comprehensive briefing about the people and company

## 📸 Screenshots

<img width="1539" alt="Screenshot 2025-03-05 at 5 23 11 PM" src="https://github.com/user-attachments/assets/e16e27e5-642b-4089-a5c8-29880d58c101" />

## 🔗 Dependencies

- Streamlit
- Requests
- JSON
- Base64
- Logging

## 👥 Contributing

Contributions, issues, and feature requests are welcome!
