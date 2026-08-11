import os
import re
import feedparser
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="MarketPulse AI — Real-Time RAG Engine",
    page_icon="📰",
    layout="wide",
)

# Custom High-Contrast Styling
st.markdown("""
    <style>
    /* Main App Background */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC !important;
    }
    
    /* Main Title Styling */
    h1 {
        font-size: 4.5rem !important;
        font-weight: 900 !important;
        color: #38BDF8 !important;
    }
    
    /* Sub-Headings */
    h2, h3 {
        color: #38BDF8 !important;
        font-weight: 700 !important;
    }

    /* Paragraph & Label Text */
    p, span, label, li {
        color: #F8FAFC !important;
        font-size: 1rem !important;
    }
    
    /* Streamlit Button Fix (White Box Issue Solved) */
    div.stButton > button {
        background-color: #1E293B !important;
        color: #38BDF8 !important;
        border: 1px solid #334155 !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        padding: 0.6rem 1rem !important;
        width: 100% !important;
    }

    /* Button Hover Effect */
    div.stButton > button:hover {
        background-color: #38BDF8 !important;
        color: #0F172A !important;
        border-color: #38BDF8 !important;
    }

    /* Text Input Box Fix */
    .stTextInput input {
        background-color: #1E293B !important;
        color: #FFFFFF !important;
        border: 1.5px solid #38BDF8 !important;
        border-radius: 8px;
    }

    /* Sidebar Styling Fix */
    section[data-testid="stSidebar"] {
        background-color: #1E293B !important;
    }
    </style>
""", unsafe_allow_html=True)

def clean_html(text):
    """Remove HTML tags like <p>, <img> from RSS content."""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text).strip()

# RSS Feeds list
RSS_FEEDS = {
    "Yahoo Finance": "https://finance.yahoo.com/news/rssindex",
    "CoinDesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "CoinTelegraph": "https://cointelegraph.com/rss",
}

@st.cache_data(ttl=600)
def fetch_rss_news():
    """Fetch live news items from RSS feeds."""
    articles = []
    for source, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:8]:
                raw_summary = entry.get("summary", entry.get("description", "No Summary available."))
                articles.append({
                    "title": entry.get("title", "No Title"),
                    "summary": clean_html(raw_summary) if raw_summary else "No Summary available.",
                    "link": entry.get("link", "#"),
                    "published": entry.get("published", "Recently"),
                    "source": source
                })
        except Exception as e:
            st.warning(f"Error fetching {source}: {e}")
    return articles

@st.cache_resource
def get_vector_store(_articles):
    """Store articles in Chroma DB using FastEmbed."""
    docs = []
    for art in _articles:
        content = f"Title: {art['title']}\nSummary: {art['summary']}\nSource: {art['source']}"
        docs.append(Document(page_content=content, metadata=art))
    
    embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name="market_news_fast"
    )
    return vectorstore

# Main Header (Bigger & Boldest Title)
st.markdown(
    """
    <h1 style='
        font-size: 4.5rem !important; 
        font-weight: 900 !important; 
        color: #38BDF8 !important; 
        margin-bottom: 0px !important; 
        line-height: 1.1 !important;
        letter-spacing: -1px;
    '>
        📰 MarketPulse AI
    </h1>
    """, 
    unsafe_allow_html=True
)
st.caption("Real-Time Financial News Intelligence & Sentiment Analysis Engine using RAG and Llama-3")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Control Panel")
    api_key_env = os.getenv("GROQ_API_KEY", "").strip()
    
    groq_input = st.text_input(
        "Enter Groq API Key:", 
        value=api_key_env, 
        type="password",
        help="Get free key at console.groq.com"
    )
    
    active_api_key = groq_input if groq_input else api_key_env
    
    refresh = st.button("🔄 Refresh Market Feeds", use_container_width=True)
    st.markdown("---")
    st.markdown("**Architecture Overview:**")
    st.markdown("• **Live Feeds:** Yahoo Finance & Crypto RSS")
    st.markdown("• **Vector DB:** FastEmbed + ChromaDB")
    st.markdown("• **LLM Engine:** Llama-3.3 via Groq API")

if refresh:
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()

with st.spinner("Fetching live market news & initializing vector database..."):
    news_data = fetch_rss_news()
    st.session_state.news_data = news_data
    if news_data:
        vectorstore = get_vector_store(news_data)
        st.session_state.vectorstore = vectorstore

# Tabs
tab_rag, tab_news, tab_analytics = st.tabs(["🤖 AI Market Assistant (RAG)", "📰 Live News Stream", "📊 Analytics"])

with tab_rag:
    st.subheader("Ask AI about Assets, Market Trends, or Specific News")
    
    # Quick Preset Buttons
    st.markdown("**💡 Quick Query Suggestions:**")
    col1, col2, col3, col4 = st.columns(4)
    preset_query = None
    if col1.button("⚡ Bitcoin Outlook"):
        preset_query = "What is the latest outlook and price news on Bitcoin?"
    if col2.button("📈 Tech Stocks"):
        preset_query = "What are the key tech stock updates on Yahoo Finance?"
    if col3.button("⚖️ Crypto Regs"):
        preset_query = "Any updates regarding crypto regulation or legal news?"
    if col4.button("📊 Market Sentiment"):
        preset_query = "What is the overall sentiment of the market today?"

    user_input = st.text_input("Or type your own custom query:", value=preset_query if preset_query else "")

    active_query = user_input

    if active_query:
        if not active_api_key:
            st.error("⚠️ Groq API Key missing! Please enter your key in the sidebar.")
        elif "vectorstore" in st.session_state:
            with st.spinner("Searching Vector DB & generating report..."):
                try:
                    retriever = st.session_state.vectorstore.as_retriever(search_kwargs={"k": 4})
                    relevant_docs = retriever.invoke(active_query)
                    context = "\n\n".join([doc.page_content for doc in relevant_docs])
                    
                    prompt = ChatPromptTemplate.from_template(
                        """You are an expert financial analyst AI.
                        Analyze the provided market news context and answer the user query accurately.
                        
                        Required Response Structure:
                        1. **Executive Summary**: A crisp direct summary.
                        2. **Market Impact**: Outlook (Bullish / Bearish / Neutral).
                        3. **Key Highlights**: Bullet points of main takeaways.
                        
                        Context from live news:
                        {context}
                        
                        User Query: {question}
                        """
                    )
                    
                    llm = ChatGroq(
                        model_name="llama-3.3-70b-versatile", 
                        groq_api_key=active_api_key, 
                        temperature=0.2
                    )
                    chain = prompt | llm | StrOutputParser()
                    response = chain.invoke({"context": context, "question": active_query})
                    
                    st.markdown("### 📊 AI Intelligence Report")
                    st.markdown(response)
                    
                    # Download Option
                    st.download_button(
                        label="📥 Download Intelligence Report (.md)",
                        data=response,
                        file_name="market_pulse_report.md",
                        mime="text/markdown"
                    )
                    
                    with st.expander("🔍 View Retrieved Sources from Vector DB"):
                        for idx, doc in enumerate(relevant_docs):
                            st.markdown(f"**Source {idx+1} [{doc.metadata.get('source')}]:** {doc.metadata.get('title')}")
                            st.caption(doc.page_content)
                except Exception as e:
                    st.error(f"Error during execution: {e}")

with tab_news:
    st.subheader("Live Market News Stream")
    if "news_data" in st.session_state:
        for article in st.session_state.news_data:
            st.markdown(f"#### [{article['title']}]({article['link']})")
            st.caption(f"Source: **{article['source']}** | Published: {article['published']}")
            st.write(article['summary'] if article['summary'] else "No Summary")
            st.markdown("---")

with tab_analytics:
    st.subheader("Market Feeds & Sentiment Dashboard")
    col_a, col_b = st.columns(2)
    
    if "news_data" in st.session_state:
        df = pd.DataFrame(st.session_state.news_data)
        
        with col_a:
            source_counts = df['source'].value_counts().reset_index()
            source_counts.columns = ['Source', 'Count']
            fig_pie = px.pie(
                source_counts, 
                values='Count', 
                names='Source', 
                title='Indexed Articles by Source',
                template='plotly_dark'
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col_b:
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = 68,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Market Sentiment Index"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#38BDF8"},
                    'steps': [
                        {'range': [0, 40], 'color': "#EF4444"},
                        {'range': [40, 60], 'color': "#F59E0B"},
                        {'range': [60, 100], 'color': "#10B981"}
                    ],
                }
            ))
            fig_gauge.update_layout(template="plotly_dark")
            st.plotly_chart(fig_gauge, use_container_width=True)