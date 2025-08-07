# news_scraper.py
"""
News Scraping Engine for Economic Times, Business Standard, and Mint
This module handles RSS feed collection and basic data processing
"""

import feedparser
import requests
from datetime import datetime
from typing import List, Dict
import time

class NewsScrapingEngine:
    """
    Handles news collection from multiple Indian business news sources
    
    Why this approach:
    - RSS feeds are reliable and structured
    - Multiple sources ensure comprehensive coverage  
    - Error handling prevents single source failures
    - Rate limiting respects website policies
    """
    
    def __init__(self):
        # Define RSS feeds for each source and category
        # These are the actual working RSS URLs as of 2025
        self.news_sources = {
            'Economic Times': {
                'base_url': 'https://economictimes.indiatimes.com',
                'feeds': {
                    'technology': 'https://economictimes.indiatimes.com/rssfeeds/13352306.cms',
                    'markets': 'https://economictimes.indiatimes.com/rssfeeds/1977021501.cms',
                    'industry': 'https://economictimes.indiatimes.com/rssfeeds/13358071.cms',
                    'economy': 'https://economictimes.indiatimes.com/rssfeeds/1898055174.cms'
                }
            },
            'Business Standard': {
                'base_url': 'https://www.business-standard.com',
                'feeds': {
                    'technology': 'https://www.business-standard.com/rss/technology.rss',
                    'economy': 'https://www.business-standard.com/rss/economy.rss',
                    'markets': 'https://www.business-standard.com/rss/markets.rss',
                    'companies': 'https://www.business-standard.com/rss/companies.rss'
                }
            },
            'Mint': {
                'base_url': 'https://www.livemint.com',
                'feeds': {
                    'technology': 'https://www.livemint.com/rss/technology',
                    'companies': 'https://www.livemint.com/rss/companies',
                    'markets': 'https://www.livemint.com/rss/market',
                    'economy': 'https://www.livemint.com/rss/politics'
                }
            }
        }
        
        # Headers to avoid being blocked by websites
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/rss+xml, application/xml, text/xml'
        }
    
    def scrape_single_feed(self, url: str, source_name: str) -> List[Dict]:
        """
        Scrape a single RSS feed and return structured article data
        
        Args:
            url: RSS feed URL
            source_name: Name of the news source
            
        Returns:
            List of article dictionaries
            
        Why this structure:
        - Consistent data format across all sources
        - Error handling prevents crashes
        - Metadata helps with later AI analysis
        """
        articles = []
        
        try:
            print(f"🔄 Scraping {source_name}...")
            
            # Special handling for Mint which sometimes blocks direct requests
            if 'livemint' in url.lower():
                response = requests.get(url, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    feed_data = feedparser.parse(response.content)
                else:
                    print(f"⚠️ {source_name}: HTTP {response.status_code}")
                    return articles
            else:
                # Direct parsing for other sources
                feed_data = feedparser.parse(url)
            
            # Extract articles from feed
            for entry in feed_data.entries[:8]:  # Limit to 8 articles per source
                try:
                    article = {
                        'title': entry.title.strip() if hasattr(entry, 'title') else 'No Title',
                        'link': entry.link if hasattr(entry, 'link') else '',
                        'published': getattr(entry, 'published', 'No Date'),
                        'summary': self._clean_summary(getattr(entry, 'summary', 'No Summary')),
                        'source': source_name,
                        'scraped_at': datetime.now().isoformat(),
                        'category': self._extract_category_from_url(url)
                    }
                    
                    # Only add if we have essential information
                    if article['title'] != 'No Title' and article['link']:
                        articles.append(article)
                        
                except Exception as e:
                    print(f"⚠️ Error processing article from {source_name}: {e}")
                    continue
            
            print(f"✅ {source_name}: Collected {len(articles)} articles")
            
            # Rate limiting - be respectful to websites
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Error scraping {source_name}: {e}")
            
        return articles
    
    def _clean_summary(self, summary: str) -> str:
        """Clean and truncate article summaries"""
        if not summary or summary == 'No Summary':
            return 'Summary not available'
        
        # Remove HTML tags if present
        import re
        clean_summary = re.sub(r'<[^>]+>', '', summary)
        
        # Truncate to reasonable length
        return clean_summary[:300] + '...' if len(clean_summary) > 300 else clean_summary
    
    def _extract_category_from_url(self, url: str) -> str:
        """Extract category from RSS URL for better organization"""
        url_lower = url.lower()
        if 'technology' in url_lower:
            return 'Technology'
        elif 'market' in url_lower:
            return 'Markets'
        elif 'economy' in url_lower:
            return 'Economy'
        elif 'companies' in url_lower or 'industry' in url_lower:
            return 'Industry'
        else:
            return 'General'
    
    def collect_news_by_industry(self, target_industry: str = 'technology') -> List[Dict]:
        """
        Collect news from all sources for a specific industry
        
        Args:
            target_industry: Industry focus (technology, markets, economy, etc.)
            
        Returns:
            Combined list of articles from all sources
            
        Why this approach:
        - Parallel collection from multiple sources
        - Industry-specific filtering
        - Comprehensive coverage
        """
        print(f"\n🎯 COLLECTING {target_industry.upper()} NEWS FROM ALL SOURCES")
        print("=" * 60)
        
        all_articles = []
        
        for source_name, source_config in self.news_sources.items():
            feeds = source_config['feeds']
            
            # Get the specific industry feed, or default to technology
            if target_industry in feeds:
                feed_url = feeds[target_industry]
            elif 'technology' in feeds:
                feed_url = feeds['technology']  # Fallback to technology
            else:
                # Use the first available feed
                feed_url = list(feeds.values())[0]
            
            articles = self.scrape_single_feed(feed_url, source_name)
            all_articles.extend(articles)
        
        print(f"\n📊 COLLECTION SUMMARY:")
        print(f"   Total Articles: {len(all_articles)}")
        print(f"   Sources: {len(self.news_sources)}")
        print(f"   Industry Focus: {target_industry.title()}")
        print("=" * 60)
        
        return all_articles

# Test the scraper independently
if __name__ == "__main__":
    print("🧪 TESTING NEWS SCRAPER")
    print("=" * 50)
    
    scraper = NewsScrapingEngine()
    test_articles = scraper.collect_news_by_industry('technology')
    
    print(f"\n📋 SAMPLE ARTICLES:")
    for i, article in enumerate(test_articles[:3]):
        print(f"\n{i+1}. {article['title'][:70]}...")
        print(f"   Source: {article['source']}")
        print(f"   Category: {article['category']}")
        print(f"   Summary: {article['summary'][:100]}...")
    
    print(f"\n✅ Scraper test completed! Collected {len(test_articles)} articles.")
