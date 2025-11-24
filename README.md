# Open Companies Registry

A Streamlit MVP application for exploring European public company and business registry data, starting with Estonia.

## Overview

This application provides access to European public company and business registry data through official government APIs. It integrates with the Estonian Business Registry (\u00c4riregister) to retrieve real-time information about company formations, liquidations, bankruptcies, and ownership structures.

## Features

- **Real-time Data Access**: Connect directly to official registry APIs
- **Database Storage**: Persist data in PostgreSQL for historical analysis
- **AI-Powered Insights**: Use XAI's language models for intelligent data analysis
- **Interactive Visualizations**: Explore data through charts and tables
- **Multi-Country Support**: Designed to scale to other EU countries

## Tech Stack

- **Frontend**: Streamlit
- **Backend/Data**: Pandas, PostgreSQL, SQLAlchemy
- **LLM**: XAI API via LangChain and LangGraph
- **Database**: PostgreSQL with dedicated `company` schema

## Installation

### Prerequisites

- Python 3.11+
- PostgreSQL database
- Estonian Business Registry API credentials
- XAI API key

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/kaljuvee/open-companies.git
   cd open-companies
   ```

2. **Create virtual environment**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.sample .env
   # Edit .env with your credentials
   ```

5. **Initialize database**
   ```bash
   # Run the SQL schema creation script
   python -c "from utils.db_utils import get_db_engine; from sqlalchemy import text; engine = get_db_engine(); conn = engine.connect(); sql = open('sql/create_schema.sql').read(); conn.execute(text(sql)); conn.commit(); print('Schema created')"
   ```

6. **Run the application**
   ```bash
   streamlit run Home.py
   ```

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# Database Configuration
MAIN_DB_URL=postgresql://username:password@host:port/database

# Estonian Business Registry API
ESTONIA_API_USERNAME=your-username
ESTONIA_API_PASSWORD=your-password

# XAI API Configuration
XAI_API_KEY=your-xai-api-key

# GitHub Configuration (optional)
GITHUB_TOKEN=your-github-token
GITHUB_USERNAME=your-username
```

## Database Schema

The application uses a PostgreSQL database with the following schema:

### Tables

- **company.companies**: Main company information
  - registry_code, name, status, country_code, address
  - registration_date, liquidation_date, bankruptcy_date

- **company.ubos**: Ultimate Beneficial Owners
  - company_id, name, identification_code, country
  - ownership_percentage

- **company.events**: Company events (formations, liquidations, etc.)
  - company_id, event_type, event_date, description

- **company.statistics**: Statistical data
  - country_code, stat_type, stat_date, count, metadata

## Estonian Business Registry API

The application uses the Estonian Business Registry (\u00c4riregister) XML/SOAP API.

### API Details

- **Endpoint**: https://ariregxmlv6.rik.ee/
- **Protocol**: XML/SOAP
- **Authentication**: Username and password
- **Rate Limits**: 
  - 50,000 queries per day
  - 1 simultaneous query
  - 20 requests per minute for document downloads

### Available Services

- Detailed company data query
- Company annual reports
- Rights of representation
- Beneficial owners data
- Company data change lists

**Note**: The API requires individual company lookups. For bulk data access, use the downloadable CSV/JSON files from the [open data portal](https://avaandmed.ariregister.rik.ee/en/downloading-open-data).

## Usage

### Home Page

The home page provides an overview of the application and system status.

### Estonia Analytics

Navigate to **EE Analytics** in the sidebar to:

- View company data from the Estonian registry
- Search for specific companies
- Analyze liquidations and bankruptcies
- Generate AI-powered insights
- Export data to CSV

### Data Sources

- **Live API**: Fetch real-time data from the Estonian registry
- **Database**: Use cached data from the PostgreSQL database

## Testing

Run the test suite to verify all components:

```bash
# Test database connection
python tests/test_database.py

# Test Estonia API
python tests/test_estonia_api.py

# Test XAI API
python tests/test_xai_api.py
```

Test results are saved to `test-results/*.json`.

## Project Structure

```
open-companies/
\u251c\u2500\u2500 Home.py                 # Main Streamlit entry point
\u251c\u2500\u2500 pages/                  # Streamlit pages
\u2502   \u2514\u2500\u2500 0_EE_Analytics.py  # Estonia analytics page
\u251c\u2500\u2500 utils/                  # Utility modules
\u2502   \u251c\u2500\u2500 db_utils.py        # Database utilities
\u2502   \u251c\u2500\u2500 estonia_api.py     # Estonia API client
\u2502   \u2514\u2500\u2500 xai_utils.py       # XAI API integration
\u251c\u2500\u2500 sql/                    # SQL scripts
\u2502   \u2514\u2500\u2500 create_schema.sql  # Database schema DDL
\u251c\u2500\u2500 tests/                  # Test scripts
\u2502   \u251c\u2500\u2500 test_database.py
\u2502   \u251c\u2500\u2500 test_estonia_api.py
\u2502   \u2514\u2500\u2500 test_xai_api.py
\u251c\u2500\u2500 test-results/          # Test output (JSON)
\u251c\u2500\u2500 requirements.txt       # Python dependencies
\u251c\u2500\u2500 .env.sample            # Environment variables template
\u2514\u2500\u2500 README.md              # This file
```

## API Integration

### Estonia API

```python
from utils.estonia_api import EstoniaAPI

# Initialize client
api = EstoniaAPI()

# Get company details
company = api.get_company_details('14854757')
```

### XAI API

```python
from utils.xai_utils import XAIAnalyzer

# Initialize analyzer
analyzer = XAIAnalyzer()

# Analyze company data
analysis = analyzer.analyze_company_data(company_data)

# Generate insights
insights = analyzer.generate_insights(data, context)
```

### Database

```python
from utils.db_utils import get_companies, insert_company

# Get companies
companies = get_companies(status='LIK', country_code='EE')

# Insert company
insert_company({
    'registry_code': '12345678',
    'name': 'Example Company',
    'status': 'Active',
    'country_code': 'EE',
    ...
})
```

## Limitations

- The Estonian API uses XML/SOAP protocol (not REST/JSON)
- Bulk queries by status are not supported via the API
- For large datasets, use the downloadable open data files
- API rate limits apply (see API Details section)

## Future Enhancements

- Add support for other EU countries
- Implement real-time gazette RSS monitoring
- Add bulk data export features
- Enhanced data visualization
- Advanced AI-powered analytics

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Contact

For questions or support, please open an issue on GitHub.

## Acknowledgments

- Estonian Business Registry (\u00c4riregister) for providing open data access
- XAI for AI-powered analysis capabilities
- Streamlit for the web framework

## Resources

- [Estonian Business Registry](https://ariregister.rik.ee/)
- [Open Data API Documentation](https://avaandmed.ariregister.rik.ee/en/open-data-api/introduction-api-services)
- [Downloadable Open Data](https://avaandmed.ariregister.rik.ee/en/downloading-open-data)
- [EU Business Registers](https://e-justice.europa.eu/topics/registers-business-insolvency-land/business-registers-search-company-eu/general-information-find-company_en)
