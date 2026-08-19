"""
GlucoSense RAG (Retrieval-Augmented Generation) Pipeline - Groq Version

Pipeline:
1. User kirim pertanyaan (Indonesia/Inggris)
2. Pertanyaan di-embed pakai model multilingual
3. Cari dokumen paling relevan dari ChromaDB
4. Kirim konteks + pertanyaan ke LLM (Groq - LLaMA 3)
5. LLM jawab berdasarkan konteks saja
"""

import os
import logging
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

# Setup logging — untuk debugging, bisa lihat apa yang di-retrieve
logger = logging.getLogger(__name__)

# --- Konfigurasi ---
_BASE_DIR = Path(__file__).parent
_CHROMA_PATH = str(_BASE_DIR / 'data' / 'chroma_db')
_COLLECTION_NAME = 'glucosense_kb'
_TOP_K = 5  # Jumlah dokumen yang di-retrieve per pertanyaan

# --- Load components sekali saat import ---
_embedder = None
_collection = None

def _init():
    """Lazy initialization — load model & DB saat pertama kali dipanggil."""
    global _embedder, _collection
    
    if _embedder is None:
        logger.info("Loading embedding model...")
        _embedder = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
        logger.info("Embedding model loaded")
    
    if _collection is None:
        logger.info("Connecting to ChromaDB...")
        client = chromadb.PersistentClient(path=_CHROMA_PATH)
        _collection = client.get_collection(_COLLECTION_NAME)
        logger.info(f"ChromaDB connected — {_collection.count()} documents")


def retrieve(query: str, top_k: int = _TOP_K) -> list[dict]:
    """
    Retrieve dokumen paling relevan dari knowledge base.
    """
    _init()
    
    # Embed pertanyaan
    query_embedding = _embedder.encode(query).tolist()
    
    # Cari di ChromaDB
    results = _collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    
    # Format hasil
    documents = []
    if results and results['documents'] and results['documents'][0]:
        for i in range(len(results['documents'][0])):
            documents.append({
                'text': results['documents'][0][i],
                'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                'distance': results['distances'][0][i] if results['distances'] else None
            })
    
    # Log untuk debugging
    logger.info(f"Query: {query[:80]}...")
    logger.info(f"Retrieved {len(documents)} documents")
    
    return documents


def build_prompt(query: str, retrieved_docs: list[dict]) -> tuple[str, str]:
    """
    Bangun system prompt dan user prompt untuk LLM.
    """
    # System prompt — ini yang mengontrol perilaku chatbot
    system_prompt = """You are GlucoSense AI, a diabetes health information assistant.

STRICT RULES:
1. ONLY answer based on the CONTEXT provided below. Do NOT use outside knowledge.
2. If the context does NOT contain enough information to answer, say: "I don't have enough information about that topic. Please consult a healthcare professional."
3. NEVER provide specific medication dosages or prescriptions. For medication questions, say: "For medication advice, please consult your doctor or pharmacist."
4. REJECT off-topic questions politely. If the question is NOT about diabetes, health, or nutrition, say: "I can only help with questions related to diabetes and health."
5. Reply in the SAME LANGUAGE as the user's question. If they ask in Indonesian, reply in Indonesian. If in English, reply in English.
6. Always be informational, NOT prescriptive. Use phrases like "generally", "according to medical literature", "consult your doctor for personalized advice".
7. When citing information, mention the source if available in the context metadata.

IMPORTANT: You are NOT a doctor. You provide general health information only."""

    # Bangun konteks dari retrieved docs
    context_parts = []
    for i, doc in enumerate(retrieved_docs):
        source = doc['metadata'].get('source', 'Unknown')
        context_parts.append(f"[Source {i+1}: {source}]\n{doc['text']}")
    
    context = "\n\n---\n\n".join(context_parts)
    
    user_prompt = f"""CONTEXT:
{context}

---

USER QUESTION: {query}

Please answer the question based ONLY on the context above."""

    return system_prompt, user_prompt


def call_llm(system_prompt: str, user_prompt: str) -> str:
    """
    Panggil LLM untuk generate jawaban menggunakan GROQ API (LLaMA 3).
    """
    try:
        from groq import Groq
        from dotenv import load_dotenv
        
        load_dotenv()
        api_key = os.getenv('GROQ_API_KEY')
        
        if not api_key:
            return "Error: API key not configured. Please set GROQ_API_KEY in .env file."
        
        client = Groq(api_key=api_key)
        
        # Menggunakan model LLaMA 3 dari Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                }
            ],
            model="openai/gpt-oss-120b", 
            temperature=0.2, # Dibuat rendah (0.2) agar lebih faktual sesuai konteks RAG
        )
        
        return chat_completion.choices[0].message.content
        
    except ImportError:
        return "Error: groq package not installed. Run in terminal: pip install groq"
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        return f"Sorry, I encountered an error while processing your question. Please try again later."


def get_response(user_message: str) -> dict:
    """
    Main function — terima pertanyaan user, return jawaban.
    """
    # 1. Retrieve dokumen relevan
    retrieved_docs = retrieve(user_message)
    
    # 2. Bangun prompt
    system_prompt, user_prompt = build_prompt(user_message, retrieved_docs)
    
    # 3. Panggil LLM
    answer = call_llm(system_prompt, user_prompt)
    
    # 4. Siapkan info sumber
    sources = []
    for doc in retrieved_docs:
        sources.append({
            'source': doc['metadata'].get('source', 'Unknown'),
            'relevance': round(1 - doc['distance'], 3) if doc['distance'] else None,
            'preview': doc['text'][:100] + '...'
        })
    
    return {
        'answer': answer,
        'sources': sources,
        'query': user_message
    }