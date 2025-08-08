# enhanced_demo_agent.py
"""
Enhanced demo agent specifically designed for dashboard integration
"""

from demo_agent import NewsAggregationAgentDemo
from database_manager import NewsDatabase
import schedule
import time
from datetime import datetime

class DashboardNewsAgent(NewsAggregationAgentDemo):
    """Enhanced agent for dashboard integration"""
    
    def __init__(self):
        super().__init__()
        self.db = NewsDatabase()
    
    def run_and_store(self, industry='technology'):
        """Run analysis and store results in database"""
        try:
            # Run the complete demo
            results = self.run_complete_demo(industry, save_report=False)
            
            if results['status'] == 'success':
                # Get the articles and analysis
                articles = results['data_summary']['articles']
                analysis = results['ai_analysis']
                
                # Store in database
                stored_count = self.db.store_articles(articles, industry, analysis)
                
                print(f"✅ Stored {stored_count} articles for {industry}")
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error in run_and_store: {e}")
            return False
    
    def run_scheduled_updates(self):
        """Run scheduled updates for multiple industries"""
        industries_to_update = ['technology', 'finance', 'energy', 'healthcare']
        
        for industry in industries_to_update:
            print(f"📰 Updating {industry} news...")
            self.run_and_store(industry)
            time.sleep(30)  # Wait between updates
        
        print("✅ Scheduled updates completed!")

# Standalone runner for scheduled updates
if __name__ == "__main__":
    agent = DashboardNewsAgent()
    
    # Schedule updates
    schedule.every().hour.do(agent.run_scheduled_updates)
    
    print("🕐 Scheduler started. Updates will run every hour.")
    print("Press Ctrl+C to stop.")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("👋 Scheduler stopped.")
