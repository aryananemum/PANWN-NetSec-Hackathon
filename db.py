import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import os

class DatabaseManager:
    def __init__(self, db_path: str = "database.db"):
        """Initialize database connection and create tables if they don't exist"""
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Create a new database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return conn
    
    def init_database(self):
        """Create tables if they don't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Journal entries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                content TEXT NOT NULL,
                prompt TEXT,
                word_count INTEGER,
                token_count INTEGER,
                unique_words INTEGER,
                sentiment_label TEXT,
                sentiment_score REAL,
                themes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS preferences (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_entry(self, content: str, prompt: str, analysis: Dict) -> int:
        """Add a new journal entry"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Extract analysis data
        sentiment = analysis.get('sentiment', {})
        themes = analysis.get('themes', [])
        
        cursor.execute('''
            INSERT INTO entries (
                timestamp, content, prompt, word_count, token_count, 
                unique_words, sentiment_label, sentiment_score, themes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            content,
            prompt,
            analysis.get('word_count', 0),
            analysis.get('token_count', 0),
            analysis.get('unique_words', 0),
            sentiment.get('label'),
            sentiment.get('score'),
            json.dumps(themes)
        ))
        
        entry_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return entry_id
    
    def get_all_entries(self, limit: Optional[int] = None) -> List[Dict]:
        """Retrieve all entries, optionally limited"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM entries ORDER BY timestamp DESC'
        if limit:
            query += f' LIMIT {limit}'
        
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        
        entries = []
        for row in rows:
            entry = dict(row)
            # Parse JSON themes back to list
            if entry['themes']:
                entry['themes'] = json.loads(entry['themes'])
            else:
                entry['themes'] = []
            entries.append(entry)
        
        return entries
    
    def get_entry_by_id(self, entry_id: int) -> Optional[Dict]:
        """Get a specific entry by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM entries WHERE id = ?', (entry_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            entry = dict(row)
            if entry['themes']:
                entry['themes'] = json.loads(entry['themes'])
            return entry
        return None
    
    def get_entries_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """Get entries within a date range"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM entries 
            WHERE timestamp BETWEEN ? AND ? 
            ORDER BY timestamp DESC
        ''', (start_date, end_date))
        
        rows = cursor.fetchall()
        conn.close()
        
        entries = []
        for row in rows:
            entry = dict(row)
            if entry['themes']:
                entry['themes'] = json.loads(entry['themes'])
            entries.append(entry)
        
        return entries
    
    def update_entry(self, entry_id: int, content: str, analysis: Dict) -> bool:
        """Update an existing entry"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        sentiment = analysis.get('sentiment', {})
        themes = analysis.get('themes', [])
        
        cursor.execute('''
            UPDATE entries 
            SET content = ?, word_count = ?, token_count = ?, 
                unique_words = ?, sentiment_label = ?, 
                sentiment_score = ?, themes = ?
            WHERE id = ?
        ''', (
            content,
            analysis.get('word_count', 0),
            analysis.get('token_count', 0),
            analysis.get('unique_words', 0),
            sentiment.get('label'),
            sentiment.get('score'),
            json.dumps(themes),
            entry_id
        ))
        
        updated = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return updated
    
    def delete_entry(self, entry_id: int) -> bool:
        """Delete an entry"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM entries WHERE id = ?', (entry_id,))
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return deleted
    
    def get_statistics(self) -> Dict:
        """Get overall statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total entries
        cursor.execute('SELECT COUNT(*) as count FROM entries')
        total_entries = cursor.fetchone()['count']
        
        # Total words
        cursor.execute('SELECT SUM(word_count) as total FROM entries')
        total_words = cursor.fetchone()['total'] or 0
        
        # Average sentiment
        cursor.execute('''
            SELECT AVG(CASE 
                WHEN sentiment_label = 'POSITIVE' THEN sentiment_score 
                ELSE -sentiment_score 
            END) as avg_sentiment
            FROM entries 
            WHERE sentiment_label IS NOT NULL
        ''')
        avg_sentiment = cursor.fetchone()['avg_sentiment']
        
        # Current streak
        cursor.execute('''
            SELECT DISTINCT DATE(timestamp) as date 
            FROM entries 
            ORDER BY date DESC
        ''')
        dates = [row['date'] for row in cursor.fetchall()]
        
        streak = 0
        if dates:
            streak = 1
            for i in range(len(dates) - 1):
                date1 = datetime.fromisoformat(dates[i])
                date2 = datetime.fromisoformat(dates[i + 1])
                if (date1 - date2).days == 1:
                    streak += 1
                else:
                    break
        
        conn.close()
        
        return {
            'total_entries': total_entries,
            'total_words': total_words,
            'avg_sentiment': avg_sentiment,
            'current_streak': streak
        }
    
    def clear_all_entries(self):
        """Delete all entries (use with caution!)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM entries')
        conn.commit()
        conn.close()
    
    def get_preference(self, key: str, default=None):
        """Get a user preference"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT value FROM preferences WHERE key = ?', (key,))
        row = cursor.fetchone()
        conn.close()
        
        return row['value'] if row else default
    
    def set_preference(self, key: str, value: str):
        """Set a user preference"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO preferences (key, value) 
            VALUES (?, ?)
        ''', (key, value))
        
        conn.commit()
        conn.close()