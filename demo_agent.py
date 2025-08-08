# demo_agent.py
"""
Main AI News Aggregation Agent Demo
This is the primary application that coordinates news scraping and AI analysis
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from news_scraper import NewsScrapingEngine
from gemini_processor import GeminiNewsProcessor

load_dotenv()

class NewsAggregationAgentDemo:
    """
    Complete AI News Aggregation Agent Demo
    
    This class orchestrates the entire news aggregation workflow:
    1. Multi-source news collection
    2. AI-powered analysis using Gemini
    3. Executive report generation
    4. Professional output formatting
    """
    
    def __init__(self):
        print("""
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║  🤖 AI NEWS AGGREGATION AGENT -  CHANDAN                       ║
║                                                                ║
║  Powered by: Google Gemini AI + Multi-Source Scraping         ║
║  Sources: Economic Times | Business Standard | Mint           ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
        """)
        
        print("🚀 INITIALIZING SYSTEM COMPONENTS...")
        print("-" * 60)
        
        try:
            # Initialize news scraping engine
            print("1️⃣  Initializing News Scraping Engine...")
            self.news_scraper = NewsScrapingEngine()
            print("   ✅ News scraper ready - 3 sources configured")
            
            # Initialize AI processor
            print("2️⃣  Initializing Gemini AI Processor...")
            self.ai_processor = GeminiNewsProcessor()
            print("   ✅ Gemini AI ready - analysis engine online")
            
            print("\n🎯 SYSTEM STATUS: ALL COMPONENTS READY")
            print("=" * 60)
            
        except Exception as e:
            print(f"❌ Initialization failed: {e}")
            print("\n💡 Please check:")
            print("   • Internet connection")
            print("   • GOOGLE_API_KEY in .env file")
            print("   • Required packages installed")
            sys.exit(1)
    
    def run_complete_demo(self, industry='technology', save_report=True):
        """
        Execute the complete news aggregation demo workflow
        
        Args:
            industry: Target industry for news collection
            save_report: Whether to save the report to file
            
        Returns:
            Dict containing all results and metrics
        """
        
        demo_start_time = datetime.now()
        print(f"\n🎬 STARTING COMPLETE DEMO: {industry.upper()} NEWS INTELLIGENCE")
        print(f"⏰ Demo initiated: {demo_start_time.strftime('%Y-%m-%d %H:%M:%S IST')}")
        print("=" * 70)
        
        try:
            # PHASE 1: NEWS COLLECTION
            print("\n📰 PHASE 1: MULTI-SOURCE NEWS COLLECTION")
            print("-" * 50)
            
            collection_start = datetime.now()
            articles = self.news_scraper.collect_news_by_industry(industry)
            collection_time = (datetime.now() - collection_start).total_seconds()
            
            if not articles:
                print("❌ No articles collected. Demo cannot continue.")
                return {'status': 'failed', 'reason': 'no_articles'}
            
            print(f"✅ Collection completed in {collection_time:.1f} seconds")
            
            # PHASE 2: AI ANALYSIS  
            print(f"\n🤖 PHASE 2: GEMINI AI ANALYSIS & PROCESSING")
            print("-" * 50)
            
            analysis_start = datetime.now()
            analysis_results = self.ai_processor.analyze_news_articles(articles, industry)
            analysis_time = (datetime.now() - analysis_start).total_seconds()
            
            print(f"✅ AI analysis completed in {analysis_time:.1f} seconds")
            
            # PHASE 3: REPORT GENERATION
            print(f"\n📊 PHASE 3: EXECUTIVE REPORT GENERATION")
            print("-" * 50)
            
            report_start = datetime.now()
            executive_report = self.ai_processor.generate_executive_report(articles, analysis_results)
            report_time = (datetime.now() - report_start).total_seconds()
            
            print(f"✅ Report generated in {report_time:.1f} seconds")
            
            # PHASE 4: OUTPUT & RESULTS
            print(f"\n📋 PHASE 4: FINAL RESULTS")
            print("-" * 50)
            
            # Display the complete report
            print(executive_report)
            
            # Save report if requested
            report_filename = None
            if save_report:
                report_filename = f"ai_news_report_{industry}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
                try:
                    with open(report_filename, 'w', encoding='utf-8') as f:
                        f.write(executive_report)
                    print(f"💾 Report saved: {report_filename}")
                except Exception as e:
                    print(f"⚠️  Could not save report: {e}")
            
            # Calculate total demo time
            total_time = (datetime.now() - demo_start_time).total_seconds()
            
            # Compile results
            demo_results = {
                'status': 'success',
                'industry_focus': industry,
                'performance_metrics': {
                    'total_demo_time': f"{total_time:.1f} seconds",
                    'articles_collected': len(articles),
                    'sources_used': len(set([a['source'] for a in articles])),
                    'collection_time': f"{collection_time:.1f}s",
                    'analysis_time': f"{analysis_time:.1f}s", 
                    'report_generation_time': f"{report_time:.1f}s"
                },
                'data_summary': {
                    'articles': articles[:3],  # Sample articles
                    'sources': list(set([a['source'] for a in articles])),
                    'categories': list(set([a.get('category', 'General') for a in articles]))
                },
                'ai_analysis': analysis_results,
                'report_file': report_filename,
                'demo_timestamp': demo_start_time.isoformat()
            }
            
            # Success summary
            print(f"\n🎉  COMPLETED SUCCESSFULLY!")
            print("=" * 70)
            print(f"📊 Performance Summary:")
            print(f"   • Total Time: {total_time:.1f} seconds")
            print(f"   • Articles Processed: {len(articles)}")
            print(f"   • AI Analysis: ✅ Completed") 
            print(f"   • Executive Report: ✅ Generated")
            print(f"   • Sources Covered: {', '.join(demo_results['data_summary']['sources'])}")
            
            if report_filename:
                print(f"   • Report File: {report_filename}")
            
            return demo_results
            
        except Exception as e:
            print(f"\n❌ DEMO FAILED: {e}")
            return {
                'status': 'failed', 
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

def run_interactive_demo():
    """
    Interactive demo runner with user choices
    Perfect for presenting to executives
    """
    
    # Available industry options
    industries = {
        '1': 'technology',
        '2': 'markets', 
        '3': 'economy',
        '4': 'companies'
    }
    
    print("\n🎯 SELECT INDUSTRY FOR NEWS ANALYSIS:")
    print("   1. Technology (AI, Tech Companies, Innovation)")
    print("   2. Markets (Stock Market, Trading, Finance)")
    print("   3. Economy (Economic Policy, Growth, GDP)")
    print("   4. Companies (Corporate News, Business Strategies)")
    
    try:
        choice = input(f"\n👉 Enter your choice (1-4) or press Enter for Technology: ").strip()
        
        if choice == '':
            selected_industry = 'technology'
            print("   🎯 Selected: Technology (Default)")
        elif choice in industries:
            selected_industry = industries[choice]
            print(f"   🎯 Selected: {selected_industry.title()}")
        else:
            print("   ⚠️  Invalid choice, using Technology as default")
            selected_industry = 'technology'
        
        # Run the demo
        print(f"\n🚀 Launching AI News Agent for {selected_industry.upper()} industry...")
        print("⏳ Please wait while the system collects and analyzes news...")
        
        agent = NewsAggregationAgentDemo()
        results = agent.run_complete_demo(selected_industry)
        
        if results['status'] == 'success':
            print(f"\n🏆  READY!")
            print("=" * 50)
            #print("Key Points for CEO Presentation:")
            print(f"✅ Processed {results['performance_metrics']['articles_collected']} articles automatically")
            print(f"✅ Analyzed content from {results['performance_metrics']['sources_used']} major news sources")
            print(f"✅ Generated executive intelligence report in {results['performance_metrics']['total_demo_time']}")
            print(f"✅ AI-powered insights delivered in professional format")
            print(f"✅ Demonstrated real business value and time savings")
            
            if results['report_file']:
                print(f"✅ Complete report saved for presentation: {results['report_file']}")
        
        else:
            print(f"❌ Demo encountered issues: {results.get('error', 'Unknown error')}")
    
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user. Thank you for testing!")
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("\n💡 Troubleshooting checklist:")
        print("   • Verify GOOGLE_API_KEY in .env file")
        print("   • Check internet connection") 
        print("   • Ensure all packages are installed")

# Main execution
if __name__ == "__main__":
    print("🎬 STARTING AI NEWS AGGREGATION AGENT DEMO")
    print("=" * 60)
    
    # Check environment setup
    if not os.getenv('GOOGLE_API_KEY'):
        print("❌ Setup incomplete!")
        print("\n📋 Required setup:")
        print("1. Get free Gemini API key from: https://aistudio.google.com")
        print("2. Create .env file with: GOOGLE_API_KEY=your_key_here")
        print("3. Run this demo again")
        sys.exit(1)
    
    # Run interactive demo
    run_interactive_demo()
