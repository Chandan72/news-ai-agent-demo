# updater.py

"""
Background updater for periodically fetching and processing news.
Runs independently of the Streamlit UI.
"""

import os
import time
import schedule
from datetime import datetime
from demo_agent import NewsAggregationAgentDemo
from database_manager import NewsDatabase

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def update_industry(industry_key: str):
    """
    #Run the AI agent for a single industry and store results.
    """
    db = NewsDatabase()
    agent = NewsAggregationAgentDemo()
    
    # Collect and analyze news
    articles = agent.news_scraper.collect_news_by_industry(industry_key)
    if not articles:
        print(f"[{datetime.now()}] No articles for {industry_key}")
        return
    
    analysis = agent.ai_processor.analyze_news_articles(articles, industry_key)
    stored = db.store_articles(articles, industry_key, analysis)
    print(f"[{datetime.now()}] Stored {stored} articles for {industry_key}")

def run_all_updates():
    """
    Update all industries defined in the dashboard.
    """
    # Mirror the dashboards industry keys
    industries = [
        "construction", "media", "manufacturing", "electronics",
        "energy", "mining", "finance", "healthcare",
        "telecom", "realestate", "fmcg", "retail", "transport",
        # add any additional keys as needed...
    ]
    
    for key in industries:
        update_industry(key)
        time.sleep(5)  # brief pause to respect source servers

def schedule_updates():
    """
    #Schedule updates at regular intervals using schedule.
    """
    # For example, update every hour
    schedule.every().hour.at(":00").do(run_all_updates)
    print(f"[{datetime.now()}] Scheduled hourly updates for all industries")
    
    # Run once at startup
    run_all_updates()
    
    # Continuously run pending jobs
    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    schedule_updates()
