"""
Parser for Dutch legislation from wetten.overheid.nl.

This module provides functionality to scrape and parse Dutch legal texts
from the official government website.
"""
import re
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

import requests
from bs4 import BeautifulSoup

from ..models.law_model import (
    MCPLaw,
    Metadata,
    HierarchicalPosition,
    IdentificationAndBasicData,
    LawStatus,
)

logger = logging.getLogger(__name__)


class WettenParser:
    """Parser for Dutch legislation from wetten.overheid.nl."""

    BASE_URL = "https://wetten.overheid.nl"
    SEARCH_URL = f"{BASE_URL}/zoeken"
    
    def __init__(self, cache_dir: Optional[str] = None):
        """Initialize the parser.
        
        Args:
            cache_dir: Directory to cache downloaded content
        """
        self.cache_dir = cache_dir
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "DutchLawMCP/1.0 (https://github.com/username/Dutch_Law_MCP)"
        })
    
    def fetch_law_by_bwb_id(self, bwb_id: str) -> str:
        """Fetch law content by BWB ID.
        
        Args:
            bwb_id: The BWB ID of the law (e.g., "BWBR0001840" for the Dutch Constitution)
            
        Returns:
            The HTML content of the law
            
        Raises:
            ValueError: If the law cannot be found
        """
        url = f"{self.BASE_URL}/{bwb_id}"
        response = self.session.get(url)
        
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch law with BWB ID {bwb_id}: {response.status_code}")
        
        return response.text
    
    def parse_metadata(self, html_content: str) -> Metadata:
        """Extract metadata from the HTML content.
        
        Args:
            html_content: The HTML content of the law
            
        Returns:
            Metadata object with extracted information
        """
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Extract title
        title_element = soup.find("h1", class_="wet-title")
        title = title_element.text.strip() if title_element else "Unknown Law"
        
        # Extract BWB ID
        bwb_id = "Unknown"
        bwb_element = soup.find("dt", string=re.compile(r"Identificatienummer"))
        if bwb_element and bwb_element.find_next("dd"):
            bwb_id = bwb_element.find_next("dd").text.strip()
        
        # Extract effective date
        date_str = "2000-01-01"  # Default
        date_element = soup.find("dt", string=re.compile(r"Geldend van"))
        if date_element and date_element.find_next("dd"):
            date_text = date_element.find_next("dd").text.strip()
            # Parse date from Dutch format (e.g., "01-01-2000")
            try:
                date_parts = date_text.split("-")
                if len(date_parts) == 3:
                    date_str = f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}"
            except Exception as e:
                logger.warning(f"Failed to parse date: {date_text} - {e}")
        
        effective_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        # Extract status
        status = LawStatus.IN_FORCE  # Default
        status_element = soup.find("dt", string=re.compile(r"Status"))
        if status_element and status_element.find_next("dd"):
            status_text = status_element.find_next("dd").text.strip().lower()
            if "vervallen" in status_text:
                status = LawStatus.REPEALED
            elif "toekomstig" in status_text:
                status = LawStatus.FUTURE
        
        # Extract authority
        authority = "Unknown"
        authority_element = soup.find("dt", string=re.compile(r"Ministerie"))
        if authority_element and authority_element.find_next("dd"):
            authority = authority_element.find_next("dd").text.strip()
        
        return Metadata(
            name_of_law=title,
            citation_title=title,  # Simplified for now
            identification_number=bwb_id,
            legal_domain=self._infer_legal_domain(title),
            regulatory_authority=authority,
            date_of_entry_into_force=effective_date,
            version="1.0",  # Simplified
            status=status,
        )
    
    def _infer_legal_domain(self, title: str) -> str:
        """Infer the legal domain from the title.
        
        Args:
            title: The title of the law
            
        Returns:
            The inferred legal domain
        """
        title_lower = title.lower()
        
        if any(term in title_lower for term in ["strafrecht", "strafvordering", "straffen"]):
            return "Criminal Law"
        elif any(term in title_lower for term in ["burgerlijk", "vermogen", "verbintenis"]):
            return "Civil Law"
        elif any(term in title_lower for term in ["grondwet", "constitutie"]):
            return "Constitutional Law"
        elif any(term in title_lower for term in ["belasting", "fiscaal"]):
            return "Tax Law"
        elif any(term in title_lower for term in ["bestuurs", "algemene wet"]):
            return "Administrative Law"
        else:
            return "Other"
    
    def parse_hierarchical_position(self, html_content: str) -> HierarchicalPosition:
        """Extract hierarchical position information from the HTML content.
        
        Args:
            html_content: The HTML content of the law
            
        Returns:
            HierarchicalPosition object with extracted information
        """
        # This would normally involve more complex parsing
        # Simplified implementation for example purposes
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Check for EU relations
        eu_relation = None
        eu_element = soup.find(string=re.compile(r"Europese richtlijn|EU-verordening"))
        if eu_element:
            eu_relation = eu_element.parent.text.strip()
        
        return HierarchicalPosition(
            relationship_to_constitution=None,  # Would require deeper analysis
            relationship_to_eu_law=eu_relation,
            relationship_to_international_treaties=None,  # Would require deeper analysis
            position_within_national_legislation=None,  # Would require deeper analysis
        )
    
    def parse_law_to_mcp(self, bwb_id: str) -> MCPLaw:
        """Parse a law into the MCP format.
        
        Args:
            bwb_id: The BWB ID of the law
            
        Returns:
            MCPLaw object with parsed information
        """
        html_content = self.fetch_law_by_bwb_id(bwb_id)
        
        metadata = self.parse_metadata(html_content)
        hierarchical_position = self.parse_hierarchical_position(html_content)
        
        # Create the basic identification part
        identification = IdentificationAndBasicData(
            metadata=metadata,
            hierarchical_position=hierarchical_position,
        )
        
        # Create a minimal MCPLaw object
        # In a real implementation, all sections would be populated
        return MCPLaw(identification_and_basic_data=identification)
    
    def search_laws(self, query: str, max_results: int = 10) -> List[Dict[str, str]]:
        """Search for laws matching the query.
        
        Args:
            query: The search query
            max_results: Maximum number of results to return
            
        Returns:
            List of laws matching the query
        """
        params = {
            "zoekterm": query,
            "geldigheidsdatum": datetime.now().strftime("%d-%m-%Y"),
        }
        
        response = self.session.get(self.SEARCH_URL, params=params)
        
        if response.status_code != 200:
            raise ValueError(f"Failed to search laws: {response.status_code}")
        
        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        
        result_elements = soup.select(".searchresult")
        for element in result_elements[:max_results]:
            title_element = element.select_one(".title")
            link_element = element.select_one("a")
            
            if title_element and link_element and link_element.get("href"):
                title = title_element.text.strip()
                href = link_element["href"]
                
                # Extract BWB ID from href
                bwb_match = re.search(r"/(BWBR\d+)", href)
                bwb_id = bwb_match.group(1) if bwb_match else None
                
                results.append({
                    "title": title,
                    "bwb_id": bwb_id,
                    "url": f"{self.BASE_URL}{href}" if href.startswith("/") else href
                })
        
        return results


# Usage example
if __name__ == "__main__":
    parser = WettenParser()
    
    # Search for laws related to "grondwet" (constitution)
    search_results = parser.search_laws("grondwet", max_results=5)
    
    for result in search_results:
        print(f"Title: {result['title']}")
        print(f"BWB ID: {result['bwb_id']}")
        print(f"URL: {result['url']}")
        print("---")
    
    # Parse the Dutch Constitution
    if search_results and search_results[0]["bwb_id"]:
        constitution_id = search_results[0]["bwb_id"]
        mcp_law = parser.parse_law_to_mcp(constitution_id)
        
        print("\nParsed Constitution:")
        print(f"Title: {mcp_law.identification_and_basic_data.metadata.name_of_law}")
        print(f"Status: {mcp_law.identification_and_basic_data.metadata.status}")
        print(f"Domain: {mcp_law.identification_and_basic_data.metadata.legal_domain}")