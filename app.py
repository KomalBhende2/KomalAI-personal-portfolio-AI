from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from utils.retriever import get_retriever
from utils.chatbot import get_chatbot_chain

st.set_page_config(page_title="ABC Tech Support Bot", page_icon="🤖")
st.title("🤖 ABC Tech Support Bot")

# Cache the chain so it doesn't reload on every message
@st.cache_resource
def load_chain():
    retriever = get_retriever()
    return get_chatbot_chain(retriever)

qa_chain = load_chain()

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Invoke the chain
        response = qa_chain.invoke({"input": prompt})
        answer = response["answer"]
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
