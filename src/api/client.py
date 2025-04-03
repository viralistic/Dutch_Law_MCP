"""
MCP API Client.

This module provides a client for the MCP API to access and manipulate
Dutch legal data in MCP format.
"""
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Union

import requests

from ..models.law_model import MCPLaw

logger = logging.getLogger(__name__)


class MCPClient:
    """Client for the MCP API."""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """Initialize the client.
        
        Args:
            base_url: Base URL of the MCP API
            api_key: API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            })
        else:
            self.session.headers.update({
                "Content-Type": "application/json",
                "Accept": "application/json"
            })
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response.
        
        Args:
            response: Response from the API
            
        Returns:
            Parsed JSON response
            
        Raises:
            ValueError: If the response is not valid JSON
            requests.HTTPError: If the response status code indicates an error
        """
        try:
            response.raise_for_status()
            return response.json()
        except json.JSONDecodeError:
            logger.error(f"Failed to decode JSON response: {response.text}")
            raise ValueError("Invalid JSON response from API")
        except requests.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            
            # Try to extract error details from response
            error_msg = "Unknown error"
            try:
                error_data = response.json()
                if "error" in error_data:
                    error_msg = error_data["error"]
                elif "message" in error_data:
                    error_msg = error_data["message"]
            except (json.JSONDecodeError, KeyError):
                error_msg = response.text
            
            raise requests.HTTPError(f"{response.status_code}: {error_msg}", response=response)
    
    def get_laws(self, limit: int = 10, offset: int = 0) -> List[Dict[str, Any]]:
        """Get a list of laws.
        
        Args:
            limit: Maximum number of laws to return
            offset: Offset for pagination
            
        Returns:
            List of laws
        """
        url = f"{self.base_url}/laws"
        params = {"limit": limit, "offset": offset}
        
        response = self.session.get(url, params=params)
        data = self._handle_response(response)
        
        return data.get("laws", [])
    
    def get_law(self, law_id: str) -> Dict[str, Any]:
        """Get a law by ID.
        
        Args:
            law_id: The ID of the law (usually BWB ID)
            
        Returns:
            Law data
            
        Raises:
            requests.HTTPError: If the law cannot be found
        """
        url = f"{self.base_url}/laws/{law_id}"
        
        response = self.session.get(url)
        return self._handle_response(response)
    
    def search_laws(self, query: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search for laws.
        
        Args:
            query: Search query
            filters: Additional filters
            
        Returns:
            List of matching laws
        """
        url = f"{self.base_url}/search"
        
        payload = {"query": query}
        if filters:
            payload["filters"] = filters
        
        response = self.session.post(url, json=payload)
        data = self._handle_response(response)
        
        return data.get("results", [])
    
    def get_article(self, law_id: str, article_id: str) -> Dict[str, Any]:
        """Get a specific article from a law.
        
        Args:
            law_id: The ID of the law
            article_id: The ID of the article
            
        Returns:
            Article data
            
        Raises:
            requests.HTTPError: If the article cannot be found
        """
        url = f"{self.base_url}/laws/{law_id}/articles/{article_id}"
        
        response = self.session.get(url)
        return self._handle_response(response)
    
    def get_case_law(self, law_id: str, limit: int = 10, offset: int = 0) -> List[Dict[str, Any]]:
        """Get case law related to a specific law.
        
        Args:
            law_id: The ID of the law
            limit: Maximum number of cases to return
            offset: Offset for pagination
            
        Returns:
            List of related case law
        """
        url = f"{self.base_url}/laws/{law_id}/case-law"
        params = {"limit": limit, "offset": offset}
        
        response = self.session.get(url, params=params)
        data = self._handle_response(response)
        
        return data.get("cases", [])
    
    def submit_law(self, law_data: Union[Dict[str, Any], MCPLaw]) -> Dict[str, Any]:
        """Submit a new law to the API.
        
        Args:
            law_data: Law data in MCP format
            
        Returns:
            Response data with the created law
            
        Raises:
            requests.HTTPError: If the submission fails
        """
        url = f"{self.base_url}/laws"
        
        # Convert MCPLaw object to dict if necessary
        if isinstance(law_data, MCPLaw):
            # This would require proper serialization
            # Here we just use a simple dictionary conversion for illustration
            payload = {
                "identification_and_basic_data": {
                    "metadata": {
                        "name_of_law": law_data.identification_and_basic_data.metadata.name_of_law,
                        "citation_title": law_data.identification_and_basic_data.metadata.citation_title,
                        "identification_number": law_data.identification_and_basic_data.metadata.identification_number,
                        "legal_domain": law_data.identification_and_basic_data.metadata.legal_domain,
                        "regulatory_authority": law_data.identification_and_basic_data.metadata.regulatory_authority,
                        "date_of_entry_into_force": law_data.identification_and_basic_data.metadata.date_of_entry_into_force.isoformat(),
                        "version": law_data.identification_and_basic_data.metadata.version,
                        "status": law_data.identification_and_basic_data.metadata.status
                    }
                }
            }
        else:
            payload = law_data
        
        response = self.session.post(url, json=payload)
        return self._handle_response(response)
    
    def update_law(self, law_id: str, law_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing law.
        
        Args:
            law_id: The ID of the law to update
            law_data: Law data to update
            
        Returns:
            Response data with the updated law
            
        Raises:
            requests.HTTPError: If the update fails
        """
        url = f"{self.base_url}/laws/{law_id}"
        
        response = self.session.put(url, json=law_data)
        return self._handle_response(response)
    
    def get_related_laws(self, law_id: str) -> List[Dict[str, Any]]:
        """Get laws related to a specific law.
        
        Args:
            law_id: The ID of the law
            
        Returns:
            List of related laws
        """
        url = f"{self.base_url}/laws/{law_id}/related"
        
        response = self.session.get(url)
        data = self._handle_response(response)
        
        return data.get("related_laws", [])
    
    def get_law_timeline(self, law_id: str) -> List[Dict[str, Any]]:
        """Get the timeline of changes for a law.
        
        Args:
            law_id: The ID of the law
            
        Returns:
            List of timeline events
        """
        url = f"{self.base_url}/laws/{law_id}/timeline"
        
        response = self.session.get(url)
        data = self._handle_response(response)
        
        return data.get("timeline", [])
    
    def get_law_statistics(self, law_id: str) -> Dict[str, Any]:
        """Get statistics for a law.
        
        Args:
            law_id: The ID of the law
            
        Returns:
            Statistics data
        """
        url = f"{self.base_url}/laws/{law_id}/statistics"
        
        response = self.session.get(url)
        return self._handle_response(response)


# Example usage
if __name__ == "__main__":
    # Initialize client with mock URL (in a real scenario, this would be your actual API endpoint)
    client = MCPClient("https://api.dutchlawmcp.example.com", api_key="your_api_key")
    
    try:
        # Search for laws related to "burgerlijk wetboek" (civil code)
        search_results = client.search_laws("burgerlijk wetboek")
        
        print(f"Found {len(search_results)} laws related to 'burgerlijk wetboek'")
        
        # Get details of the first result
        if search_results:
            first_law_id = search_results[0]["id"]
            law_details = client.get_law(first_law_id)
            
            print(f"\nDetails for {law_details['identification_and_basic_data']['metadata']['name_of_law']}:")
            print(f"Status: {law_details['identification_and_basic_data']['metadata']['status']}")
            print(f"Domain: {law_details['identification_and_basic_data']['metadata']['legal_domain']}")
            
            # Get related case law
            case_law = client.get_case_law(first_law_id)
            print(f"\nFound {len(case_law)} related court cases")
            
    except requests.HTTPError as e:
        print(f"API error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")