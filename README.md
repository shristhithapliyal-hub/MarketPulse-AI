
<img width="1908" height="665" alt="Screenshot 2026-08-11 134958" src="https://github.com/user-attachments/assets/cec70f77-21af-4ef6-a8b5-c3f58a778d75" />
<img width="1918" height="459" alt="Screenshot 2026-08-11 134907" src="https://github.com/user-attachments/assets/74f5aac7-974c-4caf-acfb-1c0bd27e15cc" />


https://github.com/user-attachments/assets/520dda0f-09b0-4043-b9ea-ea1b948ad27b

# 📰 MarketPulse AI — Real-Time Financial News Intelligence Engine

MarketPulse AI is an advanced **Retrieval-Augmented Generation (RAG)** engine designed to fetch, vectorize, index, and analyze live financial and cryptocurrency news in real time. Powered by **FastEmbed**, **ChromaDB**, and **Llama-3.3 (via Groq API)**, it delivers instant market summaries, sentiment breakdowns, and direct source attribution.

---

## ✨ Features

- ⚡ **Real-Time Feed Ingestion**: Automatically pulls feeds from Yahoo Finance, CoinDesk, and CoinTelegraph.
- 🎯 **Fast Vector Embeddings**: Uses `BAAI/bge-small-en-v1.5` embeddings via FastEmbed for ultra-low latency.
- 📦 **In-Memory Vector DB**: ChromaDB indexes live news snippets for precise context retrieval.
- 🤖 **Llama-3.3 Intelligence**: Generates structured reports with Executive Summary, Market Impact (Bullish/Bearish), and Key Highlights.
- 📊 **Analytics Dashboard**: Interactive Plotly pie charts for news source distribution and real-time market sentiment gauge meter.
- 📥 **Report Export**: Download generated intelligence reports as Markdown (`.md`) files.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **LLM Engine**: Llama-3.3-70B via Groq API
- **RAG Orchestration**: LangChain
- **Embeddings**: FastEmbed (`bge-small-en-v1.5`)
- **Vector Database**: ChromaDB
- **Data Visualization**: Plotly Express & Graph Objects

---

## 🚀 Quick Setup & Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/MarketPulse-AI.git](https://git@github.com:shristhithapliyal-hub/MarketPulse-AI.git)
cd MarketPulse-AI
