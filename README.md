# AI Website Chatbot

## Project Overview

This project implements an AI-powered chatbot that answers questions **strictly based on the content of a user-provided website**.  
The system crawls a website, extracts meaningful textual content, converts it into embeddings, stores those embeddings persistently, and enables grounded question answering through semantic retrieval.

The chatbot is explicitly designed to **avoid hallucinations**.  
If a question cannot be answered using the website content, it responds exactly with:

> **“The answer is not available on the provided website.”**

The solution follows a retrieval-augmented generation (RAG) architecture with multiple safeguards to ensure correctness, relevance, and grounding.

---

## Architecture Explanation

The system is divided into **two main phases**:

### 1. Website Indexing Pipeline

This phase runs once per website (or during re-indexing):

1. **URL Validation**
   - Ensures the input URL is valid and reachable
   - Handles empty, blocked, or unsupported websites gracefully

2. **Website Crawling**
   - Crawls HTML pages starting from the provided URL
   - Avoids duplicate URLs
   - Respects domain boundaries
   - Supports both single-page and multi-page websites

3. **Content Extraction**
   - Extracts meaningful textual content only
   - Removes:
     - Headers
     - Footers
     - Navigation menus
     - Advertisements

4. **Text Processing and Chunking**
   - Cleans and normalizes extracted text
   - Splits text into overlapping semantic chunks
   - Chunk size and overlap are configurable
   - Each chunk retains metadata:
     - Source URL
     - Page title
     - Crawl depth

5. **Embedding Generation**
   - Converts each text chunk into a dense vector embedding
   - Embeddings are generated once and reused

6. **Vector Storage**
   - Stores embeddings persistently in a vector database
   - Each website has its own isolated vector store identified by a deterministic site ID

---

### 2. Question Answering Pipeline

This phase runs for every user query:

1. **Query Embedding**
   - The user question is embedded using the same embedding model

2. **Semantic Retrieval**
   - Relevant chunks are retrieved using cosine similarity
   - Distance thresholds filter weak or irrelevant matches

3. **Context Assembly**
   - Multiple relevant chunks are combined to form a site-wide context
   - Prevents answers being limited to a single page

4. **Grounding Validation**
   - Ensures the retrieved context actually supports the question
   - If not supported, a fallback response is returned

5. **LLM Answer Generation**
   - A local LLM generates an answer using only the retrieved context
   - A strict system prompt prevents use of external knowledge

6. **Post-Generation Validation**
   - Validates that the generated answer does not introduce:
     - External facts
     - Unsupported entities
     - Numeric hallucinations

---

## Frameworks Used

### AI Orchestration Frameworks

- **LangChain / LangGraph**: Not used

**Reasoning:**  
The project avoids heavy orchestration frameworks to keep logic explicit, auditable, and transparent.  
All retrieval, grounding, and validation logic is implemented manually to demonstrate full control over hallucination prevention.

---

## LLM Model Used

### Model
- **TinyLLaMA (via Ollama)**

### Justification
- Fully local inference (no external API dependency)
- Deterministic and reproducible behavior
- Suitable for extractive, context-grounded QA
- No rate limits or API costs
- Works in CPU-only environments

The LLM is used strictly as a **language generator**, not as a knowledge source.

---

## Vector Database Used

### Database
- **ChromaDB (persistent mode)**

### Justification
- Lightweight and easy to run locally
- Supports cosine similarity search
- Persistent embedding storage
- Per-website vector store isolation
- No external service dependency

Embeddings are generated once and reused across sessions.

---

## Embedding Strategy

- **Model**: SentenceTransformers
- **Approach**:
  - Convert each semantic chunk into a dense vector
  - Use cosine similarity for retrieval
- **Why SentenceTransformers**:
  - Strong semantic similarity performance
  - Open-source and locally runnable
  - Well-supported and widely adopted

The same embedding model is used for both documents and queries to ensure consistency.

---

## Setup and Run Instructions

### 1. Create a virtual environment
```bash
python -m venv .venv


### 2. Activate the environment

```Windows

.venv\Scripts\activate


```macOS / Linux

source .venv/bin/activate

### 3. Install dependencies
pip install -r requirements.txt

###4. Install and start Ollama
ollama pull tinyllama


Ensure the Ollama service is running.

### 5. Run the Streamlit application
streamlit run app.py

## User Interface

The Streamlit interface allows users to:
- Enter a website URL
- Index or re-index the website
- Ask questions via a chat interface
- View previous conversation history
- Receive clear fallback responses when answers are unavailable
- Re-indexing is automatically skipped if embeddings already exist, unless explicitly requested.

## Assumptions

- Websites primarily contain HTML-based textual content
- JavaScript-rendered content may be partially unsupported
- The quality of answers depends on the quality of extracted text
- The system is designed for factual, informational websites

## Limitations

- No support for PDFs or image-based text
- Crawling speed depends on website size and network conditions
- Local LLM performance depends on available system memory
- No multilingual support in the current version

## Future Improvements

- Asynchronous crawling for faster indexing
- Improved boilerplate removal for complex websites
- Source citation display for each answer
- Docker-based deployment
- FastAPI backend for scalability
- Optional hybrid keyword + semantic retrieval
- Advanced re-ranking models for improved precision

## Summary

This project demonstrates a carefully engineered retrieval-augmented chatbot with a strong emphasis on:

Grounded answers

Reusable embeddings

Explicit hallucination prevention

Clean modular architecture

Clear separation of concerns
