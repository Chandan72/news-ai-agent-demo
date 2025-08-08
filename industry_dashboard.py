# industry_dashboard.py

"""
Complete Industry News Dashboard
CEO-Ready dashboard showing news articles for all industries with real-time updates
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
from database_manager import NewsDatabase  # updated import after renaming database_manager.py to db_manager.py
from demo_agent import NewsAggregationAgentDemo
import time

# Page configuration
st.set_page_config(
    page_title="AI News Intelligence Dashboard",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for visible text and styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .industry-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        border: 2px solid #e0e0e0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        cursor: pointer;
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .industry-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .industry-card h4 {
        color: #ffffff !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
        margin: 0 0 0.5rem 0 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        line-height: 1.2;
    }
    .industry-card p {
        color: #f0f0f0 !important;
        margin: 0.2rem 0 !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }
    .industry-card .metric-value {
        color: #ffffff !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }
    .metric-card {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 3px 6px rgba(0,0,0,0.1);
    }
    .metric-card h3 {
        color: white !important;
        font-size: 2rem !important;
        margin: 0 !important;
    }
    .metric-card p {
        color: #e8f5e8 !important;
        margin: 0.5rem 0 0 0 !important;
        font-weight: 500 !important;
    }
    .update-status {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        color: #155724;
        padding: 0.8rem;
        border-radius: 8px;
        text-align: center;
        margin: 1rem 0;
        border: 1px solid #c3e6cb;
        font-weight: 500;
    }
    .stSelectbox > div > div > div {
        background-color: white;
        color: #333333;
    }
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }
    div[data-testid="stSidebar"] * {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

class IndustryDashboard:
    """Main dashboard class for industry news management"""
    
    def __init__(self):
        self.db = NewsDatabase()
        self.agent = None
        self.industries = {
            "Building Materials": "construction",
            "Media & Entertainment": "media",
            "Paper and Pulp": "manufacturing",
            "Consumer Electrical": "electronics",
            "Construction Infrastructure": "construction",
            "Battery Manufacturing": "energy",
            "Mining and Minerals": "mining",
            "Ship Building": "manufacturing",
            "Cement": "manufacturing",
            "Pharmaceutical": "pharmaceutical",
            "MSW Management": "environment",
            "NBFC": "finance",
            "Healthcare": "healthcare",
            "Aluminium": "metals",
            "Paint": "chemicals",
            "Telecommunications": "telecom",
            "Oil and Gas": "energy",
            "Renewable Energy": "energy",
            "Explosives": "chemicals",
            "Financial Services": "finance",
            "Automobiles": "automotive",
            "Textiles": "manufacturing",
            "Travel and Tourism": "services",
            "Auto Ancillaries": "automotive",
            "Recruitment and Human Resources": "services",
            "Power Transmission & Equipment": "energy",
            "Real Estate & Construction": "realestate",
            "Electronic Manufacturing Services": "electronics",
            "Fast Moving Consumer Goods": "fmcg",
            "Contract Development and Manufacturing Organisation": "pharmaceutical",
            "Fashion & Apparels": "retail",
            "Aviation": "transport"
        }
    
    def render_main_dashboard(self):
        st.markdown('<h1 class="main-header">🤖 AI News Intelligence Dashboard</h1>', unsafe_allow_html=True)
        st.markdown("---")
        
        with st.sidebar:
            st.header("📊 Industry Selection")
            st.metric("Total Industries", len(self.industries))
            selected = st.selectbox(
                "Choose Industry to View:",
                ["📋 Overview"] + list(self.industries.keys())
            )
            st.markdown("---")
            stats = self.db.get_industry_stats()
            if stats:
                st.subheader("📈 Quick Stats")
                st.metric("Total Articles", sum(s["total_articles"] for s in stats.values()))
                st.metric("Active Industries", len(stats))
            st.markdown("---")
            st.subheader("🔄 Data Management")
            if selected != "📋 Overview":
                key = self.industries[selected]
                if st.button("🚀 Update News"):
                    with st.spinner("Updating..."):
                        self.update_industry_news(key)
                        st.success("Updated!")
                        st.rerun()
            if st.button("🔄 Update All"):
                self.bulk_update_industries()
        
        if selected == "📋 Overview":
            self.render_overview()
        else:
            self.render_details(selected, self.industries[selected])
    
    def render_overview(self):
        st.subheader("🏭 Industries We Monitor")
        stats = self.db.get_industry_stats()
        cols = st.columns(4)
        for idx, (name, key) in enumerate(self.industries.items()):
            with cols[idx % 4]:
                count = stats.get(key, {}).get("total_articles", 0)
                updated = stats.get(key, {}).get("last_updated", "Never")[:10]
                status = "🟢 Active" if count>0 else "🔴 Inactive"
                st.markdown(f"""
                <div class="industry-card">
                  <h4>{name}</h4>
                  <p><strong>Articles:</strong> {count}</p>
                  <p><strong>Updated:</strong> {updated}</p>
                  <p><strong>Status:</strong> {status}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("📊 Overall Stats")
        total = sum(s["total_articles"] for s in stats.values()) if stats else 0
        active = len(stats)
        coverage = (active/len(self.industries))*100 if self.industries else 0
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Articles", total)
        c2.metric("Active Industries", active)
        c3.metric("Coverage", f"{coverage:.1f}%")
        c4.metric("AI Status", "Online")
        
        if stats:
            st.markdown("---")
            df = pd.DataFrame([
                {"Industry": n, "Articles": stats.get(k, {}).get("total_articles",0)}
                for n,k in self.industries.items()
            ])
            fig = px.bar(df, x="Industry", y="Articles", color="Articles",
                         color_continuous_scale="Viridis")
            fig.update_layout(xaxis_tickangle=-45, height=500)
            st.plotly_chart(fig, use_container_width=True)
    
    def render_details(self, name, key):
        st.subheader(f"📰 {name} - Latest News")
        articles = self.db.get_articles_by_industry(key)
        if not articles:
            st.markdown('<div class="update-status">No articles. Click Update.</div>', unsafe_allow_html=True)
            return
        c1, c2, c3, c4 = st.columns(4)
        sources = list({a["source"] for a in articles})
        avg = sum(a.get("relevance_score",5) for a in articles)/len(articles)
        insights = sum(bool(a.get("ai_insights")) for a in articles)
        c1.metric("Articles", len(articles))
        c2.metric("Sources", len(sources))
        c3.metric("Avg Relevance", f"{avg:.1f}/10")
        c4.metric("AI Insights", insights)
        st.markdown(f'<div class="update-status"><strong>Last Updated:</strong> {articles[0]["scraped_at"]}</div>', unsafe_allow_html=True)
        st.markdown("---")
        for art in articles:
            with st.expander(f"{art['title']} | {art['source']}"):
                st.markdown(f"**Summary:** {art['summary']}")
                if art["ai_insights"]:
                    st.markdown(f"**🤖 Insight:** {art['ai_insights']}")
                st.markdown(f"🔗 [Read More]({art['link']})")
    
    def update_industry_news(self, key):
        if not self.agent:
            self.agent = NewsAggregationAgentDemo()
        arts = self.agent.news_scraper.collect_news_by_industry(key)
        analysis = self.agent.ai_processor.analyze_news_articles(arts, key)
        return self.db.store_articles(arts, key, analysis)
    
    def bulk_update_industries(self):
        for k in self.industries.values():
            self.update_industry_news(k)
    
def main():
    dash = IndustryDashboard()
    dash.render_main_dashboard()
    if st.sidebar.checkbox("🔄 Auto-refresh (30s)"):
        time.sleep(30)
        st.experimental_rerun()

if __name__ == "__main__":
    main()
