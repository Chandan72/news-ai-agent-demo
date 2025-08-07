# quick_test.py
"""
Quick system test to verify all components work correctly
Run this before your demo to ensure everything is set up properly
"""

import os
import sys
from dotenv import load_dotenv

def test_environment_setup():
    """Test basic environment configuration"""
    print("🔍 TESTING ENVIRONMENT SETUP...")
    
    load_dotenv()
    
    # Check API key
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in .env file")
        return False
    elif not api_key.startswith('AIza'):
        print("❌ Invalid Gemini API key format (should start with 'AIza')")
        return False
    else:
        print(f"✅ API Key found: {api_key[:10]}...")
        return True

def test_package_imports():
    """Test that all required packages can be imported"""
    print("\n🔍 TESTING PACKAGE IMPORTS...")
    
    required_packages = [
        ('langchain_google_genai', 'LangChain Google GenAI'),
        ('feedparser', 'RSS Feed Parser'),
        ('requests', 'HTTP Requests'),
        ('bs4', 'BeautifulSoup (Web Scraping)'),
        ('dotenv', 'Environment Variables')
    ]
    
    all_good = True
    for package, name in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} - Run: pip install {package}")
            all_good = False
    
    return all_good

def test_gemini_connection():
    """Test Gemini API connectivity"""
    print("\n🔍 TESTING GEMINI API CONNECTION...")
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        api_key = os.getenv('GOOGLE_API_KEY')
        llm = ChatGoogleGenerativeAI(
            google_api_key=api_key,
            model="gemini-2.5-pro",
            temperature=0
        )
        
        # Test with a simple prompt
        response = llm.invoke("Hello! Can you confirm the AI connection is working?")
        print(f"✅ Gemini API connected successfully")
        print(f"   Response: {response.content[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Gemini API connection failed: {e}")
        return False

def test_news_sources():
    """Test RSS feed connectivity"""
    print("\n🔍 TESTING NEWS SOURCE CONNECTIVITY...")
    
    import feedparser
    import requests
    
    test_feeds = [
        ('Economic Times Tech', 'https://economictimes.indiatimes.com/rssfeeds/13352306.cms'),
        ('Business Standard Tech', 'https://www.business-standard.com/rss/technology.rss')
    ]
    
    all_working = True
    for name, url in test_feeds:
        try:
            feed = feedparser.parse(url)
            if feed.entries and len(feed.entries) > 0:
                print(f"✅ {name}: {len(feed.entries)} articles available")
            else:
                print(f"⚠️  {name}: Connected but no articles found")
        except Exception as e:
            print(f"❌ {name}: {e}")
            all_working = False
    
    return all_working

def run_complete_system_test():
    """Run comprehensive system test"""
    print("🧪 COMPREHENSIVE SYSTEM TEST")
    print("=" * 50)
    
    tests = [
        ("Environment Setup", test_environment_setup),
        ("Package Imports", test_package_imports), 
        ("Gemini API Connection", test_gemini_connection),
        ("News Sources", test_news_sources)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 50)
    print("🏁 SYSTEM TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! System ready for demo.")
        print("👉 Run your demo with: python demo_agent.py")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix issues before demo.")
        return False

if __name__ == "__main__":
    success = run_complete_system_test()
    sys.exit(0 if success else 1)
