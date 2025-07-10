# Thoughtful AI Customer Support Agent

**Live Demo on replit:**  
[Click here to try it out!](https://818c3569-c155-4acd-9762-45a8b388aaa3-00-23p79b5mhhad4.janeway.replit.dev)


A simple customer support chatbot for Thoughtful AI using hardcoded Q&A and OpenAI GPT fallback.

## Features
- Matches user questions to a predefined Q&A set 
- Falls back to OpenAI GPT (gpt-3.5-turbo) version if no close match is found
- Conversational web UI (Streamlit)
- Caches LLM responses for repeated questions

## Setup
1. Clone this repo
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Get an OpenAI API key from https://platform.openai.com/
   Add to .env for future use
4. Set your API key in the environment:
   ```bash
   export OPENAI_API_KEY=sk-your-api-key
   ```

## Run the App
```bash
streamlit run app.py
```

## Usage
- Ask questions about Thoughtful AI's agents in the input box.
- If your question is not recognized, the bot will use GPT to generate a helpful answer.

## Notes
- No data is stored or logged.
- For local demo/testing only. 
