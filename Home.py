"""
Open Companies Registry - Main Application
A Streamlit MVP for exploring European company registries.
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Open Companies Registry",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .feature-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<div class="main-header">🏢 Open Companies Registry</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Explore European Public Company and Business Registry Data</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📋 Navigation")
    st.info("Use the pages menu above to explore different country registries.")
    
    st.header("⚙️ Configuration")
    
    # Check environment variables
    db_configured = bool(os.getenv('MAIN_DB_URL'))
    estonia_api_configured = bool(os.getenv('ESTONIA_API_USERNAME') and os.getenv('ESTONIA_API_PASSWORD'))
    xai_configured = bool(os.getenv('XAI_API_KEY'))
    
    st.write("**System Status:**")
    st.write(f"{'✅' if db_configured else '❌'} Database Connection")
    st.write(f"{'✅' if estonia_api_configured else '❌'} Estonia API")
    st.write(f"{'✅' if xai_configured else '❌'} XAI API")
    
    if not all([db_configured, estonia_api_configured, xai_configured]):
        st.warning("⚠️ Some services are not configured. Please check your .env file.")

# Main content
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("🇪🇪 Estonia Registry")
    st.write("""
    Access the Estonian Business Registry (Äriregister) to explore:
    - Companies in liquidation
    - Bankruptcy proceedings
    - Company formations and deletions
    - Ultimate Beneficial Owners (UBOs)
    - Real-time statistics
    """)
    st.info("Navigate to **EE Analytics** in the sidebar to get started.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("🤖 AI-Powered Analysis")
    st.write("""
    Leverage XAI's advanced language models to:
    - Analyze company data
    - Extract relevant fields automatically
    - Generate insights from statistics
    - Compare multiple companies
    - Identify trends and patterns
    """)
    st.info("AI features are integrated into all analytics pages.")
    st.markdown('</div>', unsafe_allow_html=True)

# Information section
st.markdown("---")
st.header("📖 About This Application")

st.markdown('<div class="info-box">', unsafe_allow_html=True)
st.write("""
This application provides access to European public company and business registry data, starting with Estonia. 
The system integrates with official government APIs to retrieve real-time information about company formations, 
liquidations, bankruptcies, and ownership structures.

**Key Features:**
- **Real-time Data Access**: Connect directly to official registry APIs
- **Database Storage**: Persist data in PostgreSQL for historical analysis
- **AI-Powered Insights**: Use XAI's language models for intelligent data analysis
- **Interactive Visualizations**: Explore data through charts and tables
- **Multi-Country Support**: Designed to scale to other EU countries

**Data Sources:**
- Estonia: [Äriregister API](https://ariregister.rik.ee/api) - Rate limit: 100 req/min
- Database: PostgreSQL with dedicated `company` schema
- AI: XAI API via LangChain and LangGraph
""")
st.markdown('</div>', unsafe_allow_html=True)

# API Documentation section
st.header("🔌 API Endpoints")

with st.expander("Estonia API Endpoints"):
    st.code("""
# Get companies in liquidation
GET /api/v2/legal-persons?status=LIK&fields=name,registryCode,address

# Get companies in bankruptcy
GET /api/v2/legal-persons?status=MAA&fields=name,registryCode,address

# Get deletion statistics
GET /api/v2/statistics/deletions

# Get company details
GET /api/v2/legal-persons/{registryCode}
    """, language="bash")

# Setup instructions
st.header("🚀 Getting Started")

with st.expander("Setup Instructions"):
    st.markdown("""
    1. **Configure Environment Variables**
       - Copy `.env.sample` to `.env`
       - Add your database URL, API keys, and credentials
    
    2. **Initialize Database**
       - Run the SQL scripts in the `sql/` folder
       - Ensure the `company` schema is created
    
    3. **Install Dependencies**
       ```bash
       pip install -r requirements.txt
       ```
    
    4. **Run the Application**
       ```bash
       streamlit run Home.py
       ```
    
    5. **Navigate to Analytics Pages**
       - Use the sidebar to access country-specific analytics
       - Start with Estonia (EE Analytics)
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    Open Companies Registry | Built with Streamlit, PostgreSQL, and XAI
</div>
""", unsafe_allow_html=True)
