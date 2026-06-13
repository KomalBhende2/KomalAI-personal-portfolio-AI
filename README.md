# KomalAI Portfolio Assistant

## Overview

KomalAI Portfolio Assistant is a Retrieval-Augmented Generation (RAG) based AI system designed to answer questions strictly based on Komal Bhende’s resume, projects, experience, certifications, education, and provided links.

The system is built as a personal portfolio chatbot that provides accurate, context-grounded responses without hallucination or external assumptions.

---

## Key Features

- Retrieval-Augmented Generation (RAG) based question answering system
- Context-aware responses using vector database search
- Strict grounding to resume and portfolio data only
- Hallucination prevention through prompt-level constraints
- Handles portfolio-specific queries (skills, projects, experience, education, certifications)
- Support for greeting and general interaction within portfolio scope
- Link-aware responses for GitHub and LinkedIn

---

## System Description

The chatbot is designed to act as a personal AI assistant representing Komal Bhende’s professional profile. It does not function as a general-purpose chatbot and is restricted to answering only portfolio-related queries.

If a question is outside the available context, the system responds that the information is not available in the provided knowledge base.

---

## Tech Stack

- Python
- LangChain
- Large Language Models (Groq / Ollama support)
- FAISS or similar vector database
- OpenAI-compatible embeddings (if used)
- Streamlit (optional UI layer)

---

## Architecture

The system follows a RAG pipeline:

1. Resume and portfolio data is loaded and chunked
2. Embeddings are generated for each chunk
3. Stored in a vector database
4. User query is embedded and matched against stored chunks
5. Relevant context is retrieved
6. LLM generates response strictly based on retrieved context

---

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

---

## Environment Setup

Create a .env file and add:

GROQ_API_KEY=your_api_key

---

## Running the Project

Using Groq (Online Model)

Using Ollama (Offline Model)

Install Ollama from https://ollama.com and run:

ollama run llama3

Then configure the project to use the local model.

---

## Start the Application

python app.py

or if using Streamlit:

streamlit run app.py

---

## Example Questions

- What are the skills of Komal Bhende?
- Describe AI projects in the portfolio
- What experience does she have in full-stack development?
- Show certifications
- Share GitHub and LinkedIn links

## Project Structure

app.py
chains/
retriever/
vectorstore/
prompts/
requirements.txt
README.md

## Important Note

The KomalAI only answers using the provided context. If the information is not available, it will respond that it could not find the information in the knowledge base.
