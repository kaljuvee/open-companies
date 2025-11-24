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
- [ ] Manual browser testing of all pages

## GitHub Integration
- [ ] Configure GitHub repository connection
- [ ] Push code to main branch
- [ ] Verify deployment

## Future Enhancements
- [ ] Add support for other EU countries
- [ ] Implement real-time gazette RSS monitoring
- [ ] Add bulk data export features
