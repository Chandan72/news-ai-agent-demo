# AI-Powered News Analysis Agent

This project is an intelligent news aggregation and analysis system that collects news from major Indian business sources and processes them using AI to generate insights. The system focuses on industry-specific news collection (technology, healthcare, finance, education) and uses Google's Gemini AI for analysis.

## 🌟 Features

- Multi-source news collection from leading Indian business publications:
  - Economic Times
  - Business Standard
  - Mint (LiveMint)
- Industry-specific news filtering
- AI-powered news analysis using Google's Gemini
- Automated news summarization and trend analysis
- Clean data processing and structured output

## 🛠️ Technical Architecture

### Components:

1. **`news_scraper.py`**: News collection engine
   - Handles RSS feed parsing
   - Supports multiple news sources
   - Implements rate limiting and error handling
   - Cleans and structures article data

2. **`gemini_processor.py`**: AI analysis module
   - Integrates with Google's Gemini AI
   - Processes collected news articles
   - Generates insights and summaries

3. **`demo_agent.py`**: Main demo application
   - Orchestrates the news collection and analysis
   - Demonstrates the system's capabilities

4. **`quick_test.py`**: System testing utility
   - Verifies all components are working
   - Checks dependencies and connections
   - Validates API keys and RSS feeds

## 🚀 Getting Started

### Prerequisites

- Python 3.13+
- Virtual environment (recommended)

### Required Python Packages

```bash
pip install langchain_google_genai
pip install feedparser
pip install requests
pip install bs4
pip install python-dotenv
```

### Environment Setup

1. Create a `.env` file with the following:
```env
GOOGLE_API_KEY=your_gemini_api_key
TARGET_INDUSTRY=technology,healthcare,finance,education
EMAIL_ADDRESS=your_email@example.com
```

2. Run the system test:
```bash
python quick_test.py
```

3. Start the demo:
```bash
python demo_agent.py
```

## 📊 Data Sources

The system collects news from the following RSS feeds:

### Economic Times
- Technology: `/rssfeeds/13352306.cms`
- Markets: `/rssfeeds/1977021501.cms`
- Industry: `/rssfeeds/13358071.cms`
- Economy: `/rssfeeds/1898055174.cms`

### Business Standard
- Technology: `/rss/technology.rss`
- Economy: `/rss/economy.rss`
- Markets: `/rss/markets.rss`
- Companies: `/rss/companies.rss`

### Mint (LiveMint)
- Technology: `/rss/technology`
- Companies: `/rss/companies`
- Markets: `/rss/market`
- Economy: `/rss/politics`

## 🔄 Workflow

1. **News Collection**
   - Scrapes RSS feeds from configured sources
   - Filters by target industry
   - Cleans and structures article data
   - Implements rate limiting for respectful scraping

2. **AI Processing**
   - Analyzes collected articles using Gemini AI
   - Generates insights and summaries
   - Identifies trends and patterns

3. **Output Generation**
   - Creates structured reports
   - Provides industry-specific insights
   - Maintains historical data

## ⚠️ Rate Limiting

The system implements respectful rate limiting:
- 1-second delay between RSS feed requests
- Maximum of 8 articles per source
- Proper user agent headers

## 🤝 Contributing

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## 📝 License

This project is open source and available under the MIT License.

## 🔍 Troubleshooting

If you encounter any issues:

1. Run `quick_test.py` to verify system setup
2. Check your `.env` file configuration
3. Verify internet connectivity for RSS feeds
4. Ensure Gemini API key is valid
5. Check Python environment and package installations

For more help, please create an issue in the repository.
