# AI Website Chatbot

## Project Overview

This project implements an AI-powered chatbot that answers questions **strictly based on the content of a user-provided website**. The system crawls a website, extracts meaningful textual content, converts it into embeddings, stores those embeddings persistently, and enables grounded question answering through semantic retrieval.

The chatbot is explicitly designed to **avoid hallucinations**. If a question cannot be answered using the website content, it responds exactly with:

> **"The answer is not available on the provided website."**

The solution follows a retrieval-augmented generation (RAG) architecture with multiple safeguards to ensure correctness, relevance, and grounding.

---

## Architecture Explanation

The system is divided into **two main phases**:

### 1. Website Indexing Pipeline

This phase runs once per website (or during re-indexing):

1. **URL Validation** - Ensures the input URL is valid and reachable; handles empty, blocked, or unsupported websites gracefully
2. **Website Crawling** - Crawls HTML pages starting from the provided URL; avoids duplicates; respects domain boundaries
3. **Content Extraction** - Extracts meaningful textual content only; removes headers, footers, navigation menus, and advertisements
4. **Text Processing and Chunking** - Cleans and normalizes text; splits into overlapping semantic chunks with configurable size and overlap; retains metadata (source URL, page title, crawl depth)
5. **Embedding Generation** - Converts each text chunk into a dense vector embedding for reuse
6. **Vector Storage** - Stores embeddings persistently in a vector database; each website has its own isolated vector store

### 2. Question Answering Pipeline

This phase runs for every user query:

1. **Query Embedding** - The user question is embedded using the same embedding model
2. **Semantic Retrieval** - Relevant chunks are retrieved using cosine similarity with distance thresholds
3. **Context Assembly** - Multiple relevant chunks are combined to form site-wide context
4. **Grounding Validation** - Ensures retrieved context supports the question; returns fallback if not
5. **LLM Answer Generation** - A local LLM generates answers using only retrieved context
6. **Post-Generation Validation** - Validates that answers don't introduce external facts, unsupported entities, or numeric hallucinations

---

## Frameworks Used

- **LangChain / LangGraph**: Not used
    - *Reasoning*: The project avoids heavy orchestration frameworks to keep logic explicit, auditable, and transparent

---

## LLM Model Used

- **TinyLLaMA (via Ollama)** - Fully local inference with deterministic behavior; suitable for context-grounded QA

---

## Vector Database Used

- **ChromaDB (persistent mode)** - Lightweight, supports cosine similarity search, persistent storage, per-website isolation

---

## Embedding Strategy

- **Model**: SentenceTransformers
- **Approach**: Converts semantic chunks into dense vectors; uses cosine similarity for retrieval
- **Advantage**: Strong semantic performance, open-source, locally runnable

---

## Setup and Run Instructions

### 1. Create a virtual environment
```bash
python -m venv .venv
```

### 2. Activate the environment

**Windows**
```bash
.venv\Scripts\activate
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install and start Ollama
```bash
ollama pull tinyllama
```

Ensure the Ollama service is running.

### 5. Run the Streamlit application
```bash
streamlit run app.py
```

---

## User Interface

The Streamlit interface allows users to:
- Enter a website URL
- Index or re-index the website
- Ask questions via a chat interface
- View conversation history
- Receive clear fallback responses when answers are unavailable

Re-indexing is automatically skipped if embeddings exist, unless explicitly requested.

---

## Assumptions

- Websites primarily contain HTML-based textual content
- JavaScript-rendered content may be partially unsupported
- Answer quality depends on extracted text quality
- Designed for factual, informational websites

---

## Limitations

- No support for PDFs or image-based text
- Crawling speed depends on website size and network conditions
- Local LLM performance depends on available system memory
- No multilingual support in current version

---

## Future Improvements

- Asynchronous crawling for faster indexing
- Improved boilerplate removal for complex websites
- Source citation display for each answer
- Docker-based deployment
- FastAPI backend for scalability
- Optional hybrid keyword + semantic retrieval
- Advanced re-ranking models for improved precision

---

## Summary

This project demonstrates a carefully engineered retrieval-augmented chatbot with emphasis on:
- Grounded answers
- Reusable embeddings
- Explicit hallucination prevention
- Clean modular architecture
- Clear separation of concerns
