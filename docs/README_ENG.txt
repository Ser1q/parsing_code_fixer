# 🛠️ Parsing Code Fixer

This project is an intelligent system that automatically detects and fixes parsing errors in HTML scraping code, typically caused by structural changes in the webpage. It uses large language models (LLMs), agent-based workflows, and prompt engineering to make your scraping code robust and adaptive.

## 🚀 Features

- 🧠 AI agents (via `smolagents`) to manage the task pipeline
- 🤖 LLM-powered code regeneration (OpenAI, Gemini, and local models like CodeLlama or DeepSeek)
- 🕸️ Web scraping with `cloudscraper` and `BeautifulSoup`
- ⚙️ Environment-aware prompts using `.env` configuration
- 🎯 Minimal Streamlit app for testing/debugging

## 🧩 Project Structure
```
.
├── main.py                      # Entry point for agent-based fixer
├── scraper.py                  # Custom scraping and HTML cleaning tools
├── models/
│   ├── codellama.py            # CodeLlama-based diff & generation
│   └── deepseek.py             # DeepSeek-based code generation functions
├── agent_tools.py              # Tools for agents (scrape_website, extract, clean, etc.)
├── .env                        # API keys and environment variables
├── requirements.txt            # Core dependencies (editable)
├── requirements.lock           # Frozen environment (exact versions)
└── README.md                   # Project overview
```
## 🔧 Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/parsing-code-fixer.git
cd parsing-code-fixer
```
2. Install dependencies
```python
pip install -r requirements.txt
```
For exact versions (e.g. for production):
```python
pip install -r requirements.lock
```
3. Configure environment

Create a .env file:
```bash
cp .env.example .env
```
Add your API keys:
```
OPENAI_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
```
🧠 Usage

You can run the agent loop or individual model calls:
```bash
python main.py
```
You can also use the Streamlit interface (if available):
```bash
streamlit run main.py
```
🛠️ Models Supported
	•	OpenAI (gpt-4, gpt-3.5)
	•	Gemini (via google.generativeai)
	•	Local LLMs (e.g., CodeLlama, DeepSeek via Hugging Face Transformers)

✅ To Do
	•	Add retry logic for model timeouts
	•	Extend support for non-HTML parsing tasks
	•	Dockerize the project

🤝 Contributing

Feel free to fork, contribute, and open pull requests.