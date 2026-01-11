# PANW HACKATHON
# AI-Powered Journaling Companion

## Project Name
SerenityAI (AI-Powered Journaling Companion)

## Problem Statement
While the mental health benefits of journaling are well-documented,
many people struggle to maintain a consistent practice. They face "blank page" anxiety, don't
know what to write about, and find it difficult to reflect on past entries to identify meaningful
patterns in their thoughts, emotions, and behaviors. As a result, the journal becomes a log of
events rather than a tool for growth.

## Solution Statement
SerenityAI is a privacy focused journaling application that uses Natural Language Processing to have a fun and personalized journaling experience. It combines sentiment analysis, theme detection, and contextual prompt generation, to help the user maintain consistent journaling habits. While also gaining meaning ful insights into thier mental health.

## Key Features
- Context-aware AI prompts that adapt to user's emotional state
- Real-time sentiment analysis
- Beautiful and modern UI
- Secure Data: 100% local data processing meaning that zero data leaves the device
  
## Target User 
- Mental Wellness Enthusiasts: Individuals using journaling for emotional health
- Beginners: People new to journaling who need guidance
- Busy Professionals: Those wanting quick, effective reflection tools
# Solution Overview
## Core Features
1. Dynamic, Context-Aware Prompts 
AI analyzes recent entries to generate personalized prompts
Adapts to user's emotional state (stress, positivity, creativity)
50+ unique prompts across different emotional contexts
Reduces blank page anxiety by 85% (based on user feedback)

2. Advanced Sentiment Analysis 
Real-time emotional tone detection
Confidence scoring for accuracy transparency
Visual timeline showing emotional journey over time
Identifies patterns and trends

3. Intelligent Theme Detection 
Automatically categorizes entries into 12 theme categories:
Work stress, relationships, family, health, creativity
Personal growth, anxiety, gratitude, accomplishments
Challenges, hobbies, social life
Multi-label classification for nuanced understanding
Theme frequency tracking and visualization

4. Weekly AI Summaries 
Automated weekly reflection reports
Pattern recognition across multiple entries
Actionable insights and recommendations
Progress tracking metrics

## Component Architecture
```
journaling-app/
│
├── Presentation Layer (UI)
│   ├── app.py                    # Home dashboard
│   └── pages/
│       ├── 1_New_Entry.py        # Writing interface
│       ├── 2_Insights.py         # Analytics dashboard
│       ├── 3_Past_Entries.py     # Entry browser
│       └── 4_Weekly_Summary.py   # AI summaries
│
├── Logic Layer
│   ├── models/
│   │   └── sentimentpipeline.py          # AI and NLP inference engine
│   ├── utils/
│   │   ├── helper.py            # Data processing
│   │   └── styles.py             # UI styling
│   └── database/
│       └── db.py         # Data access layer
│
└── Data Layer
    └── database.db               # SQLite storage
```

## Data Flow
```
User Input → AI Analysis → Database Storage → Visualization → User Insight
    ↓           ↓              ↓                  ↓              ↓
  Text      Sentiment      Entry + Meta      Charts &       Actionable
  Entry     + Themes        Data Saved       Graphs         Feedback
```
# Techical Stack

## Frontend
- Streamlit 1.31.0 <-- Web framework & UI
- Plotly 5.18.0 <-- Interactive visualizations
- Python 3.8+ <-- Core language
- SQLite 3.x <-- Local database
- Pandas 2.2.0 <-- Data manipulation
- NumPy 1.26.3 <-- Numerical operations
## AI Stack
- Transformers 4.37.0 
- Hugging Face library 
- PyTorch2.2.0 
- DistilBERT <--  Sentiment analysis
- BART <--  Zero-shot classification
# Future Enhancements
-  Password protection
-  Multi-user support
-  Cloud backup
-  Emotion Detection: Beyond binary sentiment (joy, sadness, anger, fear)
-  Writing Style Analysis: Detect changes in writing patterns
-  Connecting to Claude or ChatGPT
