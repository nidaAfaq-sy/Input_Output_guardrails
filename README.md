# 🐍 Python-Only Chatbot with Guardrails (Chainlit + Agents)

This is an AI-powered chatbot built using **Chainlit** and a custom **Agents framework**. It only allows Python-related interactions by applying **input and output guardrails** to validate both the user’s question and the assistant’s response.

---

## 🔧 Features

- ✅ Accepts only **Python-related** input
- 🚫 Rejects irrelevant queries using **input guardrails**
- 🛡 Ensures safe and on-topic output using **output guardrails**
- 🤖 Uses `gpt-4o-mini` for guardrail agents and main agent logic
- 💬 Web chat interface powered by **Chainlit**
- 🔐 Secure API key management via `.env`

---

## 📦 Requirements

- Python 3.10+
- `chainlit`
- `openai`
- `pydantic`
- `python-dotenv`
- `agents` (custom module or package)

---

## 📁 Project Structure

.
├── main.py # Main chatbot logic with guardrails
├── .env # Stores your API key
├── README.md # Project documentation

yaml
Copy
Edit

---

## 🔑 Environment Setup

Create a `.env` file in the root of your project:

```env
GEMINI_API_KEY=your_gemini_api_key_here
⚠️ Note: OpenAIChatCompletionsModel is designed for OpenAI models. If you're using Gemini, proper setup with Google’s SDK is required. See section below.

🚀 How to Run
Install all dependencies:

bash
Copy
Edit
pip install chainlit openai python-dotenv pydantic
Then start the chatbot:

bash
Copy
Edit
chainlit run main.py
Chainlit will launch a local web server. Open it in your browser to begin chatting.

🧠 How Guardrails Work
✅ Input Guardrail
Verifies the user question is related to Python.

If not, it blocks the question with a warning.

✅ Output Guardrail
Ensures the bot's response is also Python-related.

Blocks outputs that are off-topic.

💬 Example
text
Copy
Edit
User: What is the capital of France?
→ ❌ Rejected by Input Guardrail

User: How do I create a list in Python?
→ ✅ Allowed by Input Guardrail
→ ✅ Output also passes Output Guardrail
→ ✅ Response sent to user
⚠️ Using Gemini Models Properly
In your code, you have:

python
Copy
Edit
OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
This assumes Gemini works with OpenAI’s interface — which is incorrect.

✅ If using Gemini, switch to the official SDK:

bash
Copy
Edit
pip install google-generativeai
python
Copy
Edit
import google.generativeai as genai
genai.configure(api_key="your-gemini-api-key")
Use Gemini models with proper configuration, not with OpenAIChatCompletionsModel.

✅ Otherwise, use OpenAI models (gpt-4o, gpt-3.5-turbo, etc.) for best compatibility.

🛠 Customization Ideas
Change the main agent to support multiple languages (e.g., JavaScript, C++).

Add logging to explain why a query was blocked.

Customize agent instructions for stricter rules.

🙏 Acknowledgements
Chainlit

OpenAI

Google Gemini

Your custom agents package

