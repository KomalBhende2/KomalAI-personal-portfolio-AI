# AI Customer Support Chatbot (RAG System)

This project is a customer support chatbot built using Retrieval-Augmented Generation (RAG). It answers user questions based on a company knowledge base and uses either a cloud-based or local language model.

The system supports two LLM options:
- Groq (online, fast inference)
- Ollama (offline, local inference)

## Company Information

Name: ABC Technologies Pvt. Ltd.  
CEO: Komal Bhende  
Domain: AI-powered software solutions and customer support systems

The chatbot is designed to answer queries related to the company using only the provided knowledge base.

## Features

- Retrieval-Augmented Generation (RAG) based question answering
- Context-based responses using vector search
- Support for both online and offline language models
- Strict grounding to prevent hallucinated answers
- Handles greetings and general user queries

## Tech Stack

- Python
- LangChain
- Groq API
- Ollama
- Vector database (FAISS or similar)

## Installation

Clone the repository:

git clone https://github.com/KomalBhende2/customer-rag-chatbot.git

cd repository-name

Create and activate virtual environment:

python -m venv venv

venv\Scripts\activate   (Windows)

source venv/bin/activate   (Linux/Mac)

Install dependencies:

pip install -r requirements.txt

## Environment Setup

Create a .env file and add:

GROQ_API_KEY=your_api_key

## Running the Project

Using Groq (Online Model)

Using Ollama (Offline Model)

Install Ollama from https://ollama.com and run:

ollama run llama3

Then configure the project to use the local model.

## Start the Application

python app.py

or if using Streamlit:

streamlit run app.py

## Example Questions

- What does ABC Technologies Pvt. Ltd. do?
- Who is the CEO of the company?
- What services do you provide?
- Hello

## Project Structure

app.py
chains/
retriever/
vectorstore/
prompts/
requirements.txt
README.md

## Important Note

The chatbot only answers using the provided context. If the information is not available, it will respond that it could not find the information in the knowledge base.
