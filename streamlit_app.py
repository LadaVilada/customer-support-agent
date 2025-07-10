#!/usr/bin/env python3
"""
Streamlit entry point for the Thoughtful AI Customer Support Agent.
This file should be run with: streamlit run streamlit_app.py
"""

import streamlit as st
import requests
import json
from typing import Optional

# Import from app package
from app.config import FASTAPI_BASE_URL

def call_fastapi_chat(message: str) -> Optional[str]:
    """
    Call the FastAPI /chat endpoint to get a response.
    
    Args:
        message: User's input message
        
    Returns:
        Bot's response string, or None if error
    """
    try:
        response = requests.post(
            f"{FASTAPI_BASE_URL}/chat",
            json={"message": message},
            timeout=30
        )
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to FastAPI backend: {e}")
        return None
    except (KeyError, json.JSONDecodeError) as e:
        st.error(f"Error parsing response from backend: {e}")
        return None

def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Thoughtful AI Customer Support Agent",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("Thoughtful AI Customer Support Agent 🤖")
    
    # Check if FastAPI backend is running
    try:
        health_check = requests.get(f"{FASTAPI_BASE_URL}/health", timeout=5)
        if health_check.status_code != 200:
            st.error("⚠️ FastAPI backend is not responding properly. Please ensure it's running on port 8000.")
    except requests.exceptions.RequestException:
        st.error("⚠️ Cannot connect to FastAPI backend. Please start it with: `uvicorn main:app --reload`")
        st.stop()
    
    # Initialize chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Chat input form
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "Ask a question about Thoughtful AI's agents:",
            placeholder="e.g., What does CAM do?",
            key="input"
        )
        submitted = st.form_submit_button("Send", type="primary")
        
        if submitted and user_input.strip():
            # Show loading spinner
            with st.spinner("Getting response..."):
                bot_response = call_fastapi_chat(user_input.strip())
                
                if bot_response:
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "user": user_input.strip(),
                        "bot": bot_response
                    })
                else:
                    st.error("Failed to get response from backend.")
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("---")
        st.subheader("Conversation History")
        
        for i, chat in enumerate(st.session_state.chat_history):
            # User message
            with st.chat_message("user"):
                st.write(chat["user"])
            
            # Bot message
            with st.chat_message("assistant"):
                st.write(chat["bot"])
        
        # Clear chat button
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Sidebar with information
    with st.sidebar:
        st.header("About")
        st.markdown("""
        This chatbot helps with questions about Thoughtful AI's products and services.
        
        **How it works:**
        1. Your question is sent to the FastAPI backend
        2. The backend matches it against our FAQ database
        3. If no match is found, it uses AI to generate a response
        4. The response is returned to this Streamlit frontend
        
        **Backend:** FastAPI on port 8000
        **Frontend:** Streamlit on port 8501
        """)

if __name__ == "__main__":
    main() 