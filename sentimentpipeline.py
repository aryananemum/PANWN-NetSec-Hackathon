import streamlit as st
from transformers import pipeline, DistilBertTokenizer
from typing import Dict, List, Tuple
import random
import pandas as pd

# Define theme categories
THEME_CATEGORIES = [
    "work stress", "relationships", "family", "health", 
    "creativity", "personal growth", "anxiety", "gratitude",
    "accomplishments", "challenges", "hobbies", "social life"
]

@st.cache_resource

def load_sentiment_analyzer():
    """Load sentiment analysis model"""
    try:
        return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    except Exception as e:
        st.error(f"Error loading sentiment model: {e}")
        return None
    
@st.cache_resource
def load_tokenizer():
    """Load DistilBERT tokenizer for advanced text analysis"""
    try:
        return DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    except Exception as e:
        st.error(f"Error loading tokenizer: {e}")
        return None
