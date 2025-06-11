# 🧠 MentalHealth-GPT

**MentalHealth-GPT** is a conversational AI chatbot designed to assist users with mental health-related queries. It uses **LangChain** and **Google's Gemini-Pro** via the `langchain-google-genai` library. The bot is friendly, non-abusive, and keeps track of past conversations for contextual responses.

---

## 🚀 Features

- 🗣️ Conversational memory with `ConversationBufferMemory`
- 🤖 Powered by Google’s `gemini-pro` model
- 🧘 Focused on mental health discussions
- ❌ Redirects off-topic questions politely
- 🔐 Secure API key handling using `.env`

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/mentalhealth-gpt.git
cd mentalhealth-gpt
```
### 2. Create a Virtual Environment
# Windows
```bash
python -m venv venv
venv\Scripts\activate
```
# Linux/Mac
```bash
python3 -m venv venv
source venv/bin/activate
```
### 3. Install Dependencies 
```bash
pip install -r requirements.txt
```
### 4. Create a .env File
```bash
Your api key=your_google_generative_ai_api_key
```
### 5. 📁 File Structure
```bash
mentalhealth-gpt/
│
├── mental_health_bot.py       # Core bot logic
├── VectorStoreManger.py       # Handles vector store operations (e.g., saving/loading embeddings)
├── .env                       # Environment variables (API key)
├── requirements.txt           # Python dependencies
├── run_bot.bat                # Windows launch script
└── README.md                  # Project documentation
```


