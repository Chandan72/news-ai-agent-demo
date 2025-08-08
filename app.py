# app.py
import streamlit as st
from demo_agent import NewsAggregationAgentDemo  # Your existing demo class
import time

def main():
    st.title("AI Powered News Aggregation Demo")
    st.write("""
        Welcome! Select an industry below and watch the AI agent process news step-by-step.
        At the end, you'll see a top article analysis report — a perfect demo for your CEO.
    """)

    # Industry options
    industries = {
        "Technology": "technology",
        "Markets": "markets",
        "Economy": "economy",
        "Companies": "companies"
    }

    # Industry selection dropdown
    selected_industry = st.selectbox("Select Industry to Analyze", list(industries.keys()))

    if st.button("Run News Analysis"):
        industry_code = industries[selected_industry]

        st.info(f"Starting news aggregation for **{selected_industry}**...")
        agent = NewsAggregationAgentDemo()

        # Show progress section
        progress_text = st.empty()
        progress_bar = st.progress(0)

        # Step 1: News Collection
        progress_text.text("Step 1: Collecting news from multiple sources...")
        articles = agent.news_scraper.collect_news_by_industry(industry_code)
        progress_bar.progress(25)
        time.sleep(0.5)  # Small delay for demo effect

        if not articles:
            st.error("No articles found. Please try a different industry or check your sources.")
            return

        # Step 2: AI Analysis
        progress_text.text("Step 2: Analyzing articles with Google Gemini AI...")
        analysis_results = agent.ai_processor.analyze_news_articles(articles, industry_code)
        progress_bar.progress(60)
        time.sleep(0.5)

        # Step 3: Report Generation
        progress_text.text("Step 3: Generating executive report...")
        executive_report = agent.ai_processor.generate_executive_report(articles, analysis_results)
        progress_bar.progress(90)
        time.sleep(0.5)

        # Final step: Show results
        progress_text.text("Step 4: Complete! Here is the top article analysis report:")
        progress_bar.progress(100)
        
        # Display the report in a scrollable box
        st.text_area("Executive News Intelligence Report", executive_report, height=600)

        # Optionally save the report to a file for download or future reference
        # st.download_button allows CEO or users to download the report as a text file
        st.download_button(
            label="Download Report as TXT",
            data=executive_report,
            file_name=f'executive_report_{industry_code}.txt',
            mime='text/plain'
        )

if __name__ == "__main__":
    main()
