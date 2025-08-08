# database_manager.py

"""
Database manager for storing and retrieving news articles by industry.
Uses SQLite (built into Python) for persistent storage.
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any

class NewsDatabase:
    """Manages SQLite database for storing news articles by industry."""
    
    def __init__(self, db_path: str = "news_database.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create 'articles' table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                industry TEXT NOT NULL,
                title TEXT NOT NULL,
                summary TEXT,
                link TEXT,
                source TEXT,
                category TEXT,
                published TEXT,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                relevance_score INTEGER DEFAULT 5,
                ai_insights TEXT
            )
        """)
        
        # Create 'industry_stats' table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS industry_stats (
                industry TEXT PRIMARY KEY,
                total_articles INTEGER DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                top_sources TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def store_articles(
        self,
        articles: List[Dict[str, Any]],
        industry: str,
        ai_analysis: Dict[str, Any] = None
    ) -> int:
        """
        Store a batch of articles for a given industry.
        Clears existing articles for that industry first.
        
        Returns:
            Number of articles stored.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Delete old articles for this industry
        cursor.execute("DELETE FROM articles WHERE industry = ?", (industry,))
        
        stored_count = 0
        for idx, article in enumerate(articles, start=1):
            # Determine AI insight for this article if available
            ai_insight = ""
            if ai_analysis and ai_analysis.get("top_stories"):
                for story in ai_analysis["top_stories"]:
                    if story.get("article_id") == idx:
                        ai_insight = story.get("key_insights", "")
                        break
            
            cursor.execute("""
                INSERT INTO articles (
                    industry, title, summary, link,
                    source, category, published,
                    relevance_score, ai_insights
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                industry,
                article.get("title", ""),
                article.get("summary", ""),
                article.get("link", ""),
                article.get("source", ""),
                article.get("category", ""),
                article.get("published", ""),
                article.get("relevance_score", 5),
                ai_insight
            ))
            stored_count += 1
        
        # Update industry_stats
        sources = list({a.get("source", "") for a in articles})
        cursor.execute("""
            INSERT INTO industry_stats (
                industry, total_articles, last_updated, top_sources
            ) VALUES (?, ?, ?, ?)
            ON CONFLICT(industry) DO UPDATE SET
                total_articles=excluded.total_articles,
                last_updated=excluded.last_updated,
                top_sources=excluded.top_sources
        """, (
            industry,
            stored_count,
            datetime.now().isoformat(),
            json.dumps(sources)
        ))
        
        conn.commit()
        conn.close()
        return stored_count
    
    def get_articles_by_industry(self, industry: str) -> List[Dict[str, Any]]:
        """
        Retrieve all articles stored for a given industry,
        ordered by most recent scrape time.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT
                title, summary, link,
                source, category, published,
                relevance_score, ai_insights, scraped_at
            FROM articles
            WHERE industry = ?
            ORDER BY scraped_at DESC
        """, (industry,))
        
        rows = cursor.fetchall()
        conn.close()
        
        articles = []
        for row in rows:
            articles.append({
                "title": row[0],
                "summary": row[1],
                "link": row[2],
                "source": row[3],
                "category": row[4],
                "published": row[5],
                "relevance_score": row[6],
                "ai_insights": row[7],
                "scraped_at": row[8]
            })
        return articles
    
    def get_industry_stats(self) -> Dict[str, Dict[str, Any]]:
        """
        Retrieve stats for all industries: total articles,
        last updated timestamp, and top sources list.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT industry, total_articles, last_updated, top_sources
            FROM industry_stats
            ORDER BY total_articles DESC
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        stats = {}
        for industry, total, last_updated, sources_json in rows:
            try:
                sources = json.loads(sources_json)
            except:
                sources = []
            stats[industry] = {
                "total_articles": total,
                "last_updated": last_updated,
                "top_sources": sources
            }
        return stats
    
    def get_all_industries(self) -> List[str]:
        """
        Return a list of all industries that have records
        in the articles table.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT DISTINCT industry FROM articles ORDER BY industry")
        rows = cursor.fetchall()
        conn.close()
        
        return [row[0] for row in rows]
