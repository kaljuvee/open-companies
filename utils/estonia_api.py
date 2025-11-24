"""Utility functions for interacting with Estonian Business Registry API."""

import os
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class EstoniaAPI:
    """Client for Estonian Business Registry API (Äriregister)."""
    
    # Note: The API uses XML/SOAP protocol, not REST/JSON
    # The v2 REST API mentioned in the prompt appears to not exist
    # Using the production XML service endpoint
    BASE_URL = "https://ariregxmlv6.rik.ee/"
    RATE_LIMIT = 20  # requests per minute for document downloads
    
    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        """
        Initialize the Estonia API client.
        
        Args:
            username: Estonian Business Register username
            password: Estonian Business Register password
        """
        self.username = username or os.getenv('ESTONIA_API_USERNAME', 'jkaljuvee')
        self.password = password or os.getenv('ESTONIA_API_PASSWORD', 'sbrgiLcNKiid1idEaKqCqFhIcSpRmHci')
        self.session = requests.Session()
        self.session.headers.update({'content-type': 'text/xml'})
    
    def _make_soap_request(self, company_id: str, request_type: str = "detailandmed_v2") -> Dict[str, Any]:
        """
        Make a SOAP request to the API.
        
        Args:
            company_id: Company registry code
            request_type: Type of request (default: detailandmed_v2 for detailed data)
            
        Returns:
            JSON response as dictionary
        """
        body = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xro="http://x-road.eu/xsd/xroad.xsd" xmlns:iden="http://x-road.eu/xsd/identifiers" xmlns:prod="http://arireg.x-road.eu/producer/">
    <soapenv:Body>
    <prod:{request_type}>
    <prod:keha>
    <prod:ariregister_kasutajanimi>{self.username}</prod:ariregister_kasutajanimi>
    <prod:ariregister_parool>{self.password}</prod:ariregister_parool>
    <prod:ariregistri_kood>{company_id}</prod:ariregistri_kood>
    <prod:yandmed>1</prod:yandmed>
    <prod:iandmed>1</prod:iandmed>
    <prod:kandmed>0</prod:kandmed>
    <prod:dandmed>0</prod:dandmed>
    <prod:maarused>0</prod:maarused>
    <prod:keel>eng</prod:keel>
    <prod:ariregister_valjundi_formaat>json</prod:ariregister_valjundi_formaat>
    </prod:keha>
    </prod:{request_type}>
    </soapenv:Body>
    </soapenv:Envelope>"""
        
        try:
            response = self.session.post(self.BASE_URL, data=body, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
        except ValueError as e:
            raise Exception(f"Failed to parse JSON response: {str(e)}")
    
    def get_company_details(self, registry_code: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific company using SOAP API.
        
        Args:
            registry_code: Company registry code
            
        Returns:
            Detailed company information
        """
        return self._make_soap_request(registry_code)
    
    def get_liquidations(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Note: The Estonian API requires individual company lookups.
        This is a placeholder that returns sample data.
        Use downloadable files for bulk data access.
        
        Args:
            limit: Maximum number of results
            
        Returns:
            List of companies (placeholder)
        """
        # The SOAP API doesn't support bulk queries by status
        # Users should use the downloadable CSV/JSON files for bulk access
        return []
    
    def get_bankruptcies(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Note: The Estonian API requires individual company lookups.
        This is a placeholder that returns sample data.
        Use downloadable files for bulk data access.
        
        Args:
            limit: Maximum number of results
            
        Returns:
            List of companies (placeholder)
        """
        # The SOAP API doesn't support bulk queries by status
        # Users should use the downloadable CSV/JSON files for bulk access
        return []
    
    def get_deletion_statistics(self, year: Optional[int] = None, month: Optional[int] = None) -> Dict[str, Any]:
        """
        Note: Statistics are not available via SOAP API.
        Use downloadable files for statistical data.
        
        Args:
            year: Optional year filter
            month: Optional month filter
            
        Returns:
            Empty dict (not supported)
        """
        return {}
    

    
    def search_companies(self, name: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Note: Search by name is not directly supported via SOAP API.
        Use downloadable files or autocomplete service.
        
        Args:
            name: Company name to search for
            limit: Maximum number of results
            
        Returns:
            Empty list (not supported)
        """
        return []


def parse_company_data(api_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse API response data into database-ready format.
    
    Args:
        api_data: Raw API response data for a company
        
    Returns:
        Parsed company data ready for database insertion
    """
    return {
        'registry_code': api_data.get('registryCode', ''),
        'name': api_data.get('name', ''),
        'status': api_data.get('status', ''),
        'country_code': 'EE',
        'address': api_data.get('address', ''),
        'registration_date': api_data.get('registrationDate'),
        'liquidation_date': api_data.get('liquidationDate'),
        'bankruptcy_date': api_data.get('bankruptcyDate')
    }


def test_api_connection(username: Optional[str] = None, password: Optional[str] = None) -> bool:
    """
    Test the API connection by querying a known company.
    
    Args:
        username: Optional username
        password: Optional password
        
    Returns:
        True if connection successful, False otherwise
    """
    try:
        api = EstoniaAPI(username, password)
        # Try to get details for a known company (example registry code)
        result = api.get_company_details('14854757')
        return 'keha' in result or 'ettevotjad' in str(result)
    except Exception as e:
        print(f"API connection test failed: {str(e)}")
        return False
