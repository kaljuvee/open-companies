"""
Estonia (EE) Company Registry Analytics
Interactive dashboard for exploring Estonian business registry data.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.estonia_api import EstoniaAPI, parse_company_data
from utils.db_utils import get_companies, insert_company, execute_sql, test_connection
from utils.xai_utils import XAIAnalyzer

# Page configuration
st.set_page_config(
    page_title="Estonia Analytics - Open Companies",
    page_icon="🇪🇪",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.875rem;
        font-weight: bold;
    }
    .status-lik {
        background-color: #ff6b6b;
        color: white;
    }
    .status-maa {
        background-color: #ee5a6f;
        color: white;
    }
    .status-active {
        background-color: #51cf66;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🇪🇪 Estonia Company Registry Analytics")
st.markdown("Explore data from the Estonian Business Registry (Äriregister)")

# Initialize API client
@st.cache_resource
def get_api_client():
    """Initialize and cache the Estonia API client."""
    return EstoniaAPI()

@st.cache_resource
def get_xai_analyzer():
    """Initialize and cache the XAI analyzer."""
    try:
        return XAIAnalyzer()
    except Exception as e:
        st.warning(f"XAI API not configured: {str(e)}")
        return None

api_client = get_api_client()
xai_analyzer = get_xai_analyzer()

# Sidebar controls
with st.sidebar:
    st.header("🔧 Data Controls")
    
    # Data source selection
    data_source = st.radio(
        "Data Source",
        ["Live API", "Database"],
        help="Choose whether to fetch live data from the API or use cached database data"
    )
    
    # Status filter
    status_filter = st.selectbox(
        "Company Status",
        ["All", "Liquidation (LIK)", "Bankruptcy (MAA)", "Active"],
        help="Filter companies by their current status"
    )
    
    # Limit for API calls
    if data_source == "Live API":
        result_limit = st.slider("Result Limit", 10, 500, 100, step=10)
    
    # Action buttons
    st.markdown("---")
    
    if st.button("🔄 Refresh Data from API", type="primary"):
        st.session_state['refresh_data'] = True
    
    if st.button("💾 Save to Database"):
        st.session_state['save_to_db'] = True
    
    # Connection status
    st.markdown("---")
    st.subheader("Connection Status")
    
    db_status = test_connection()
    st.write(f"{'✅' if db_status else '❌'} Database")
    
    try:
        api_test = api_client.get_legal_persons(limit=1)
        api_status = True
    except:
        api_status = False
    st.write(f"{'✅' if api_status else '❌'} Estonia API")

# Main content area
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🔍 Company Search", "📈 Statistics", "🤖 AI Analysis"])

# Tab 1: Overview
with tab1:
    st.header("Registry Overview")
    
    # Fetch data based on source
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def fetch_data(source, status, limit=100):
        """Fetch company data from API or database."""
        if source == "Live API":
            status_map = {
                "Liquidation (LIK)": "LIK",
                "Bankruptcy (MAA)": "MAA",
                "All": None
            }
            api_status = status_map.get(status)
            
            try:
                response = api_client.get_legal_persons(
                    status=api_status,
                    fields=['name', 'registryCode', 'address', 'status'],
                    limit=limit
                )
                data = response.get('data', [])
                if data:
                    df = pd.DataFrame(data)
                    # Rename columns to match database schema
                    df = df.rename(columns={
                        'registryCode': 'registry_code'
                    })
                    return df
                return pd.DataFrame()
            except Exception as e:
                st.error(f"Error fetching data from API: {str(e)}")
                return pd.DataFrame()
        else:
            # Fetch from database
            status_map = {
                "Liquidation (LIK)": "LIK",
                "Bankruptcy (MAA)": "MAA",
                "All": None
            }
            db_status = status_map.get(status)
            try:
                return get_companies(status=db_status, country_code='EE')
            except Exception as e:
                st.error(f"Error fetching data from database: {str(e)}")
                return pd.DataFrame()
    
    # Handle refresh
    if st.session_state.get('refresh_data', False):
        st.cache_data.clear()
        st.session_state['refresh_data'] = False
        st.success("Data refreshed!")
    
    # Fetch data
    limit_val = result_limit if data_source == "Live API" else 1000
    df = fetch_data(data_source, status_filter, limit_val)
    
    # Display metrics
    if not df.empty:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Companies", len(df))
        
        with col2:
            if 'status' in df.columns:
                lik_count = len(df[df['status'] == 'LIK'])
                st.metric("In Liquidation", lik_count)
        
        with col3:
            if 'status' in df.columns:
                maa_count = len(df[df['status'] == 'MAA'])
                st.metric("In Bankruptcy", maa_count)
        
        with col4:
            st.metric("Data Source", data_source)
        
        # Status distribution chart
        if 'status' in df.columns:
            st.subheader("Status Distribution")
            status_counts = df['status'].value_counts()
            fig = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                title="Companies by Status",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Data table
        st.subheader("Company Data")
        
        # Display options
        col1, col2 = st.columns([3, 1])
        with col1:
            search_term = st.text_input("🔍 Search companies", "")
        with col2:
            show_rows = st.number_input("Rows to display", 10, 100, 25)
        
        # Filter by search term
        display_df = df.copy()
        if search_term:
            display_df = display_df[
                display_df.apply(lambda row: search_term.lower() in str(row).lower(), axis=1)
            ]
        
        # Display table
        st.dataframe(
            display_df.head(show_rows),
            use_container_width=True,
            hide_index=True
        )
        
        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"estonia_companies_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
        
        # Save to database
        if st.session_state.get('save_to_db', False) and data_source == "Live API":
            with st.spinner("Saving to database..."):
                saved_count = 0
                for _, row in df.iterrows():
                    try:
                        company_data = {
                            'registry_code': row.get('registry_code', ''),
                            'name': row.get('name', ''),
                            'status': row.get('status', ''),
                            'country_code': 'EE',
                            'address': row.get('address', ''),
                            'registration_date': None,
                            'liquidation_date': None,
                            'bankruptcy_date': None
                        }
                        insert_company(company_data)
                        saved_count += 1
                    except Exception as e:
                        st.error(f"Error saving company {row.get('registry_code')}: {str(e)}")
                
                st.success(f"Saved {saved_count} companies to database!")
                st.session_state['save_to_db'] = False
    else:
        st.info("No data available. Try refreshing or changing filters.")

# Tab 2: Company Search
with tab2:
    st.header("Company Search")
    
    search_name = st.text_input("Enter company name to search", "")
    
    if st.button("Search", type="primary") and search_name:
        with st.spinner("Searching..."):
            try:
                results = api_client.search_companies(search_name, limit=50)
                
                if results:
                    st.success(f"Found {len(results)} companies")
                    results_df = pd.DataFrame(results)
                    st.dataframe(results_df, use_container_width=True)
                    
                    # Company details
                    if 'registryCode' in results_df.columns or 'registry_code' in results_df.columns:
                        code_col = 'registryCode' if 'registryCode' in results_df.columns else 'registry_code'
                        selected_code = st.selectbox(
                            "Select a company to view details",
                            results_df[code_col].tolist()
                        )
                        
                        if st.button("Get Details"):
                            with st.spinner("Fetching details..."):
                                try:
                                    details = api_client.get_company_details(selected_code)
                                    st.json(details)
                                except Exception as e:
                                    st.error(f"Error fetching details: {str(e)}")
                else:
                    st.warning("No companies found")
            except Exception as e:
                st.error(f"Search error: {str(e)}")

# Tab 3: Statistics
with tab3:
    st.header("Deletion Statistics")
    
    col1, col2 = st.columns(2)
    with col1:
        year = st.number_input("Year", 2020, datetime.now().year, datetime.now().year)
    with col2:
        month = st.number_input("Month (optional, 0 for all)", 0, 12, 0)
    
    if st.button("Fetch Statistics", type="primary"):
        with st.spinner("Fetching statistics..."):
            try:
                stats = api_client.get_deletion_statistics(
                    year=year,
                    month=month if month > 0 else None
                )
                
                if stats:
                    st.json(stats)
                    
                    # Visualize if data is available
                    if isinstance(stats, dict) and 'data' in stats:
                        stats_df = pd.DataFrame(stats['data'])
                        if not stats_df.empty:
                            fig = px.bar(
                                stats_df,
                                x='month' if 'month' in stats_df.columns else stats_df.index,
                                y='count' if 'count' in stats_df.columns else stats_df.columns[0],
                                title=f"Company Deletions - {year}"
                            )
                            st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No statistics available for the selected period")
            except Exception as e:
                st.error(f"Error fetching statistics: {str(e)}")

# Tab 4: AI Analysis
with tab4:
    st.header("🤖 AI-Powered Analysis")
    
    if xai_analyzer is None:
        st.warning("XAI API is not configured. Please add XAI_API_KEY to your .env file.")
    else:
        analysis_type = st.selectbox(
            "Select Analysis Type",
            ["Company Analysis", "Statistics Summary", "Data Insights"]
        )
        
        if analysis_type == "Company Analysis":
            st.subheader("Analyze Company Data")
            
            if not df.empty:
                # Select a company
                if 'registry_code' in df.columns and 'name' in df.columns:
                    company_options = df.apply(
                        lambda x: f"{x['name']} ({x['registry_code']})", axis=1
                    ).tolist()
                    selected = st.selectbox("Select a company", company_options)
                    
                    if st.button("Analyze", type="primary"):
                        # Get the selected company data
                        idx = company_options.index(selected)
                        company_data = df.iloc[idx].to_dict()
                        
                        with st.spinner("Analyzing with AI..."):
                            try:
                                analysis = xai_analyzer.analyze_company_data(company_data)
                                st.markdown("### Analysis Results")
                                st.write(analysis)
                            except Exception as e:
                                st.error(f"Analysis error: {str(e)}")
            else:
                st.info("Load company data first to perform analysis")
        
        elif analysis_type == "Statistics Summary":
            st.subheader("Generate Statistics Summary")
            
            if st.button("Generate Summary", type="primary"):
                with st.spinner("Generating AI summary..."):
                    try:
                        # Get some statistics data
                        stats_data = df.to_dict('records')[:10] if not df.empty else []
                        
                        if stats_data:
                            summary = xai_analyzer.summarize_statistics(stats_data)
                            st.markdown("### AI Summary")
                            st.write(summary)
                        else:
                            st.info("No data available for summary")
                    except Exception as e:
                        st.error(f"Summary error: {str(e)}")
        
        else:  # Data Insights
            st.subheader("Generate Data Insights")
            
            context = st.text_area(
                "Provide context for the analysis (optional)",
                "Analyze Estonian company registry data and provide insights on business trends."
            )
            
            if st.button("Generate Insights", type="primary"):
                with st.spinner("Generating insights..."):
                    try:
                        data_sample = df.head(20).to_dict('records') if not df.empty else {}
                        insights = xai_analyzer.generate_insights(data_sample, context)
                        st.markdown("### AI Insights")
                        st.write(insights)
                    except Exception as e:
                        st.error(f"Insights error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    Estonia Analytics | Data from Äriregister API | Rate limit: 100 req/min
</div>
""", unsafe_allow_html=True)
