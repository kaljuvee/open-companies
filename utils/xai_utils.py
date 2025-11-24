"""Utility functions for XAI API integration using LangChain and LangGraph."""

import os
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment variables
load_dotenv()


class XAIAnalyzer:
    """Wrapper for XAI API using LangChain."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize XAI analyzer.
        
        Args:
            api_key: XAI API key (defaults to environment variable)
        """
        self.api_key = api_key or os.getenv('XAI_API_KEY')
        if not self.api_key:
            raise ValueError("XAI_API_KEY not found in environment variables")
        
        # Initialize LangChain ChatOpenAI with XAI endpoint
        self.llm = ChatOpenAI(
            model="grok-3",
            openai_api_key=self.api_key,
            openai_api_base="https://api.x.ai/v1",
            temperature=0.7
        )
    
    def analyze_company_data(self, company_data: Dict[str, Any]) -> str:
        """
        Analyze company data and provide insights.
        
        Args:
            company_data: Dictionary containing company information
            
        Returns:
            Analysis text
        """
        prompt = f"""
        Analyze the following company data and provide insights:
        
        Company Name: {company_data.get('name', 'N/A')}
        Registry Code: {company_data.get('registry_code', 'N/A')}
        Status: {company_data.get('status', 'N/A')}
        Address: {company_data.get('address', 'N/A')}
        
        Provide a brief analysis of the company's status and any notable observations.
        """
        
        messages = [
            SystemMessage(content="You are a business analyst specializing in European company registries."),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def extract_relevant_fields(self, raw_data: Dict[str, Any], data_type: str = "company") -> Dict[str, Any]:
        """
        Use LLM to identify and extract relevant fields from raw API data.
        
        Args:
            raw_data: Raw data from API
            data_type: Type of data being processed
            
        Returns:
            Dictionary of extracted relevant fields
        """
        prompt = f"""
        Given the following raw {data_type} data from an API response, identify and extract the most relevant fields.
        Focus on: name, identification codes, status, dates, addresses, and ownership information.
        
        Raw data:
        {str(raw_data)}
        
        Return a structured summary of the key fields and their values.
        """
        
        messages = [
            SystemMessage(content="You are a data extraction specialist. Extract structured information from raw data."),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        return {"analysis": response.content, "raw_data": raw_data}
    
    def summarize_statistics(self, stats_data: List[Dict[str, Any]]) -> str:
        """
        Generate a summary of statistical data.
        
        Args:
            stats_data: List of statistics records
            
        Returns:
            Summary text
        """
        prompt = f"""
        Analyze the following company registry statistics and provide a summary with key insights:
        
        {str(stats_data)}
        
        Focus on trends, notable changes, and important patterns.
        """
        
        messages = [
            SystemMessage(content="You are a data analyst specializing in business statistics."),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def compare_companies(self, companies: List[Dict[str, Any]]) -> str:
        """
        Compare multiple companies and provide insights.
        
        Args:
            companies: List of company data dictionaries
            
        Returns:
            Comparison analysis
        """
        companies_text = "\n\n".join([
            f"Company {i+1}:\n" + "\n".join([f"  {k}: {v}" for k, v in comp.items()])
            for i, comp in enumerate(companies)
        ])
        
        prompt = f"""
        Compare the following companies and provide insights on their similarities, differences, and notable characteristics:
        
        {companies_text}
        """
        
        messages = [
            SystemMessage(content="You are a business analyst comparing companies."),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def generate_insights(self, data: Any, context: str = "") -> str:
        """
        Generate general insights from any data.
        
        Args:
            data: Data to analyze
            context: Additional context for the analysis
            
        Returns:
            Generated insights
        """
        prompt = f"""
        {context}
        
        Analyze the following data and provide actionable insights:
        
        {str(data)}
        """
        
        messages = [
            SystemMessage(content="You are an AI analyst providing business insights."),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        return response.content


def test_xai_connection(api_key: Optional[str] = None) -> bool:
    """
    Test XAI API connection.
    
    Args:
        api_key: Optional API key
        
    Returns:
        True if connection successful, False otherwise
    """
    try:
        analyzer = XAIAnalyzer(api_key)
        test_data = {"name": "Test Company", "status": "Active"}
        result = analyzer.analyze_company_data(test_data)
        return len(result) > 0
    except Exception as e:
        print(f"XAI connection test failed: {str(e)}")
        return False
