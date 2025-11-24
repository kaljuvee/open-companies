# Project TODO

## Setup & Infrastructure
- [x] Create Streamlit application structure (Home.py and pages/)
- [x] Create requirements.txt with all dependencies
- [x] Create .env.sample for environment variables
- [x] Set up PostgreSQL connection utilities
- [x] Create SQL schema in sql/ folder

## Estonia Company Registry Integration
- [x] Implement Estonia API integration (XML/SOAP)
- [x] Add support for company details lookup
- [x] Implement API authentication handling
- [x] Create data fetching and parsing utilities
- [ ] Note: Bulk queries require downloadable files, not API

## Database & Data Management
- [x] Design company schema in PostgreSQL
- [x] Create DDL scripts for database tables
- [x] Implement data persistence layer
- [x] Add data validation and error handling

## Streamlit Pages
- [x] Create Home.py (main entry point)
- [x] Create pages/0_EE_Analytics.py for Estonia analytics
- [x] Add sidebar navigation
- [x] Implement data visualization components
- [x] Add filtering and search capabilities

## XAI API Integration
- [x] Set up LangChain with XAI API
- [x] Add LLM-powered field extraction
- [x] Create intelligent data analysis features
- [ ] Implement LangGraph workflows (optional enhancement)

## Testing & Validation
- [x] Create test scripts in tests/ folder
- [x] Implement component tests with JSON output
- [x] Test Estonia API integration
- [x] Test database operations
- [x] Test XAI API integration
- [x] Manual browser testing of all pages

## GitHub Integration
- [x] Configure GitHub repository connection
- [x] Push code to main branch
- [x] Verify deployment

## Bug Fixes
- [x] Fix Estonia API status check to use correct environment variables
- [x] Add plotly to requirements.txt
- [x] Fix EE Analytics page API method calls
- [x] All services now show correct status (green checkmarks)

## Future Enhancements
- [ ] Add support for other EU countries
- [ ] Implement real-time gazette RSS monitoring
- [ ] Add bulk data export features

## Current Issues
- [x] Fix database data display in EE Analytics page - data not showing when Database mode selected

## Real Data Integration
- [x] Create utils/data_ingestor.py to download real company data via API
- [x] Download CSV files from Estonian open data portal
- [x] Import CSV data into database using SQLAlchemy
- [x] Verify real data is displaying correctly (109 companies loaded)
- [ ] Fix company search functionality in EE Analytics page

## Testing
- [x] Create tests/test_search_functionality.py to verify search filters

## Data Import
- [x] Import 1000+ companies to make database meaningful for analytics
- [x] Created scripts/quick_import.py for fast bulk imports
- [x] Database now has 1,009 companies (981 Active, 27 LIK, 1 MAA)
