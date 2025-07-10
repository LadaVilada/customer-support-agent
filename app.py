import streamlit as st
from qa_data import qa_data
from matcher import find_best_match
from llm_fallback import get_llm_response, LLMError

st.set_page_config(page_title="Thoughtful AI Customer Support Agent", page_icon="🤖")
st.title("Thoughtful AI Customer Support Agent")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # List of (user, bot)

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask a question about Thoughtful AI's agents:", "", key="input")
    submitted = st.form_submit_button("Send")
    if submitted:
        if not user_input.strip():
            st.warning("Please enter a question.")
        else:
            answer, score = find_best_match(user_input, qa_data)
            if answer:
                bot_reply = answer
            else:
                try:
                    bot_reply = get_llm_response(user_input)
                except LLMError as e:
                    bot_reply = f"[LLM Error] {e}"
            # Prevent duplicate consecutive entries
            if not st.session_state.chat_history or st.session_state.chat_history[-1][0] != user_input:
                st.session_state.chat_history.append((user_input, bot_reply))

st.markdown("---")
st.subheader("Conversation")
for i, (user, bot) in enumerate(st.session_state.chat_history):
    st.markdown(f"**You:** {user}")
    st.markdown(f"**Bot:** {bot}")
    st.markdown("---") 