"""
Parser for Dutch legislation from wetten.overheid.nl.

This module provides functionality to scrape and parse Dutch legal texts
from the official government website.
"""
import re
import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

import requests
from bs4 import BeautifulSoup

from src.models.law_model import (
    MCPLaw,
    Metadata,
    HierarchicalPosition,
    IdentificationAndBasicData,
    LawStatus,
)

logger = logging.getLogger(__name__)


class WettenParser:
    """Parser for Dutch laws from wetten.overheid.nl."""

    BASE_URL = "https://wetten.overheid.nl"
    SEARCH_URL = f"{BASE_URL}/zoeken"
    
    def __init__(self, cache_dir: Optional[str] = None):
        """Initialize the parser."""
        self.cache_dir = cache_dir
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,nl;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        })
        
        # Default values for metadata fields
        self.default_metadata = {
            "name_of_law": "Unknown Law",
            "citation_title": "Unknown Law",
            "date_of_entry_into_force": "Unknown",
            "regulatory_authority": "Ministerie van Justitie en Veiligheid",
            "legal_domain": "Other"
        }
        
        # Dutch month names mapping
        self.dutch_months = {
            'januari': '01',
            'februari': '02',
            'maart': '03',
            'april': '04',
            'mei': '05',
            'juni': '06',
            'juli': '07',
            'augustus': '08',
            'september': '09',
            'oktober': '10',
            'november': '11',
            'december': '12'
        }
        
        # Common law names and their metadata
        self.common_laws = {
            "BWBR0005537": {
                "name_of_law": "Algemene wet bestuursrecht",
                "citation_title": "Awb",
                "date_of_entry_into_force": "1994-01-01",
                "regulatory_authority": "Ministerie van Justitie en Veiligheid",
                "legal_domain": "Administrative Law",
                "identification_number": "BWBR0005537"
            },
            "BWBR0005291": {
                "name_of_law": "Burgerlijk Wetboek",
                "citation_title": "BW",
                "date_of_entry_into_force": "1992-01-01",
                "regulatory_authority": "Ministerie van Justitie en Veiligheid",
                "legal_domain": "Civil Law",
                "identification_number": "BWBR0005291"
            },
            "BWBR0001854": {
                "name_of_law": "Wetboek van Strafrecht",
                "citation_title": "Sr",
                "date_of_entry_into_force": "1886-09-01",
                "regulatory_authority": "Ministerie van Justitie en Veiligheid",
                "legal_domain": "Criminal Law",
                "identification_number": "BWBR0001854"
            },
            "BWBR0001840": {
                "name_of_law": "Grondwet",
                "citation_title": "Gw",
                "date_of_entry_into_force": "1815-03-24",
                "regulatory_authority": "Ministerie van Binnenlandse Zaken en Koninkrijksrelaties",
                "legal_domain": "Constitutional Law",
                "identification_number": "BWBR0001840"
            },
            "BWBR0009405": {
                "name_of_law": "Wet op de arbeidsovereenkomst",
                "citation_title": "BW7",
                "date_of_entry_into_force": "1907-07-13",
                "regulatory_authority": "Ministerie van Sociale Zaken en Werkgelegenheid",
                "legal_domain": "Employment Law",
                "identification_number": "BWBR0009405"
            },
            "BWBR0006502": {
                "name_of_law": "Algemene wet gelijke behandeling",
                "citation_title": "AWGB",
                "date_of_entry_into_force": "1994-09-01",
                "regulatory_authority": "Ministerie van Binnenlandse Zaken en Koninkrijksrelaties",
                "legal_domain": "Equal Treatment Law",
                "identification_number": "BWBR0006502"
            }
        }
    
    def _make_request(self, url: str, params: Optional[Dict[str, Any]] = None, max_retries: int = 3) -> str:
        """Make an HTTP request with retries."""
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, params=params, timeout=10)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                if attempt == max_retries - 1:
                    raise
                logger.warning(f"Request failed (attempt {attempt + 1}/{max_retries}): {e}")
                time.sleep(1)  # Wait before retrying
    
    def fetch_law_by_bwb_id(self, bwb_id: str) -> str:
        """Fetch law content by BWB ID."""
        if not bwb_id.startswith("BWBR"):
            bwb_id = f"BWBR{bwb_id}"
        
        url = f"{self.BASE_URL}/{bwb_id}"
        logger.info(f"Fetching law from URL: {url}")
        
        try:
            return self._make_request(url)
        except requests.RequestException as e:
            raise ValueError(f"Failed to fetch law with BWB ID {bwb_id}: {e}")
    
    def parse_metadata(self, html_content: str) -> Metadata:
        """Extract metadata from the HTML content."""
        try:
            soup = BeautifulSoup(html_content, "html.parser")
            
            # Extract title
            title = "Unknown Law"
            title_element = (
                soup.find("h1", class_="wet-title") or
                soup.find("h1", class_="titel") or
                soup.find("h1")  # Fallback to any h1
            )
            if title_element:
                title = title_element.get_text(strip=True)
            
            # Extract BWB ID from the content
            bwb_id = "Unknown"
            bwb_matches = re.findall(r"BWBR\d+", html_content)
            if bwb_matches:
                bwb_id = bwb_matches[0]
            
            # Extract date
            date_str = datetime.now().strftime("%Y-%m-%d")  # Default to today
            date_matches = re.findall(r"Geldend van (\d{2}-\d{2}-\d{4})", html_content)
            if date_matches:
                try:
                    date_parts = date_matches[0].split("-")
                    date_str = f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}"
                except (IndexError, ValueError) as e:
                    logger.warning(f"Failed to parse date: {e}")
            
            # Extract authority
            authority = "Unknown"
            authority_element = soup.find(string=re.compile(r"Ministerie van|Minister van"))
            if authority_element:
                authority = authority_element.strip()
            
            return Metadata(
                name_of_law=title,
                citation_title=title,
                identification_number=bwb_id,
                legal_domain=self._infer_legal_domain(title),
                regulatory_authority=authority,
                date_of_entry_into_force=datetime.strptime(date_str, "%Y-%m-%d").date(),
                version=date_str,
                status=LawStatus.IN_FORCE
            )
        except Exception as e:
            logger.error(f"Error parsing metadata: {e}")
            raise
    
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
        """Parse a law from wetten.overheid.nl into MCP format."""
        url = f"{self.BASE_URL}/{bwb_id}"
        logger.info(f"Fetching law from URL: {url}")
        
        try:
            response = requests.get(url, headers=self.session.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract metadata
            metadata = self._extract_metadata(soup, bwb_id)
            
            # Extract content
            content = self._extract_content(soup)
            
            return MCPLaw(
                metadata=metadata,
                content=content
            )
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch law: {e}")
            # Return a law object with default metadata
            return MCPLaw(
                metadata=self._get_default_metadata(bwb_id),
                content={"articles": [], "chapters": [], "sections": []}
            )
    
    def _extract_metadata(self, soup: BeautifulSoup, bwb_id: str) -> Dict[str, Any]:
        """Extract metadata from the law page."""
        metadata = self._get_default_metadata(bwb_id)
        
        try:
            # Extract title
            title_elem = soup.find('h1', class_='wet-titel')
            if title_elem:
                metadata["name_of_law"] = title_elem.text.strip()
            
            # Extract citation title
            citation_elem = soup.find('div', class_='wet-citatie')
            if citation_elem:
                citation_text = citation_elem.text.strip()
                citation_match = re.search(r'\(([^)]+)\)', citation_text)
                if citation_match:
                    metadata["citation_title"] = citation_match.group(1)
            
            # Extract entry into force date
            date_elem = soup.find('div', class_='wet-inwerkingtreding')
            if date_elem:
                date_text = date_elem.text.strip()
                date = self._parse_dutch_date(date_text)
                if date:
                    metadata["date_of_entry_into_force"] = date
            
            # Extract regulatory authority
            authority_elem = soup.find('div', class_='wet-beheerder')
            if authority_elem:
                metadata["regulatory_authority"] = authority_elem.text.strip()
            
            # Determine legal domain
            metadata["legal_domain"] = self._determine_law_type(metadata["name_of_law"])
            
            # Add identification number
            metadata["identification_number"] = bwb_id
            
        except Exception as e:
            logger.error(f"Error extracting metadata: {e}")
        
        return metadata
    
    def _parse_dutch_date(self, text: str) -> Optional[str]:
        """Parse a Dutch date string into a standardized format."""
        try:
            # Try to find a date in the format "DD month YYYY"
            date_match = re.search(r'(\d{1,2})\s+([a-zA-Z]+)\s+(\d{4})', text)
            if date_match:
                day = date_match.group(1).zfill(2)
                month = self.dutch_months.get(date_match.group(2).lower())
                year = date_match.group(3)
                if month:
                    return f"{year}-{month}-{day}"
            
            # Try to find a date in the format "DD-MM-YYYY"
            date_match = re.search(r'(\d{2})-(\d{2})-(\d{4})', text)
            if date_match:
                return f"{date_match.group(3)}-{date_match.group(2)}-{date_match.group(1)}"
            
            # Try to find a date in the format "YYYY-MM-DD"
            date_match = re.search(r'(\d{4})-(\d{2})-(\d{2})', text)
            if date_match:
                return f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
            
            # If no date found, check if this is a common law with known date
            bwb_match = re.search(r'BWBR\d+', text)
            if bwb_match and bwb_match.group(0) in self.common_laws:
                return self.common_laws[bwb_match.group(0)]["date_of_entry_into_force"]
            
        except Exception as e:
            logger.error(f"Error parsing date from text '{text}': {e}")
        
        return None
    
    def _extract_content(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract content from the law page."""
        content = {
            "articles": [],
            "chapters": [],
            "sections": []
        }
        
        try:
            # Extract articles
            article_elems = soup.find_all('div', class_='wet-artikel')
            for article in article_elems:
                article_data = {
                    "number": "",
                    "title": "",
                    "text": "",
                    "paragraphs": []
                }
                
                # Extract article number
                number_elem = article.find('div', class_='artikel-nummer')
                if number_elem:
                    article_data["number"] = number_elem.text.strip()
                
                # Extract article title
                title_elem = article.find('div', class_='artikel-titel')
                if title_elem:
                    article_data["title"] = title_elem.text.strip()
                
                # Extract article text
                text_elem = article.find('div', class_='artikel-tekst')
                if text_elem:
                    article_data["text"] = text_elem.text.strip()
                
                # Extract paragraphs
                para_elems = article.find_all('div', class_='artikel-lid')
                for para in para_elems:
                    para_data = {
                        "number": "",
                        "text": ""
                    }
                    
                    # Extract paragraph number
                    para_number = para.find('div', class_='lid-nummer')
                    if para_number:
                        para_data["number"] = para_number.text.strip()
                    
                    # Extract paragraph text
                    para_text = para.find('div', class_='lid-tekst')
                    if para_text:
                        para_data["text"] = para_text.text.strip()
                    
                    article_data["paragraphs"].append(para_data)
                
                content["articles"].append(article_data)
            
            # Extract chapters
            chapter_elems = soup.find_all('div', class_='wet-hoofdstuk')
            for chapter in chapter_elems:
                chapter_data = {
                    "number": "",
                    "title": "",
                    "articles": []
                }
                
                # Extract chapter number
                number_elem = chapter.find('div', class_='hoofdstuk-nummer')
                if number_elem:
                    chapter_data["number"] = number_elem.text.strip()
                
                # Extract chapter title
                title_elem = chapter.find('div', class_='hoofdstuk-titel')
                if title_elem:
                    chapter_data["title"] = title_elem.text.strip()
                
                # Extract articles in chapter
                article_elems = chapter.find_all('div', class_='wet-artikel')
                for article in article_elems:
                    article_data = {
                        "number": "",
                        "title": "",
                        "text": ""
                    }
                    
                    # Extract article number
                    art_number = article.find('div', class_='artikel-nummer')
                    if art_number:
                        article_data["number"] = art_number.text.strip()
                    
                    # Extract article title
                    art_title = article.find('div', class_='artikel-titel')
                    if art_title:
                        article_data["title"] = art_title.text.strip()
                    
                    # Extract article text
                    art_text = article.find('div', class_='artikel-tekst')
                    if art_text:
                        article_data["text"] = art_text.text.strip()
                    
                    chapter_data["articles"].append(article_data)
                
                content["chapters"].append(chapter_data)
            
            # Extract sections
            section_elems = soup.find_all('div', class_='wet-afdeling')
            for section in section_elems:
                section_data = {
                    "number": "",
                    "title": "",
                    "articles": []
                }
                
                # Extract section number
                number_elem = section.find('div', class_='afdeling-nummer')
                if number_elem:
                    section_data["number"] = number_elem.text.strip()
                
                # Extract section title
                title_elem = section.find('div', class_='afdeling-titel')
                if title_elem:
                    section_data["title"] = title_elem.text.strip()
                
                # Extract articles in section
                article_elems = section.find_all('div', class_='wet-artikel')
                for article in article_elems:
                    article_data = {
                        "number": "",
                        "title": "",
                        "text": ""
                    }
                    
                    # Extract article number
                    art_number = article.find('div', class_='artikel-nummer')
                    if art_number:
                        article_data["number"] = art_number.text.strip()
                    
                    # Extract article title
                    art_title = article.find('div', class_='artikel-titel')
                    if art_title:
                        article_data["title"] = art_title.text.strip()
                    
                    # Extract article text
                    art_text = article.find('div', class_='artikel-tekst')
                    if art_text:
                        article_data["text"] = art_text.text.strip()
                    
                    section_data["articles"].append(article_data)
                
                content["sections"].append(section_data)
            
        except Exception as e:
            logger.error(f"Error extracting content: {e}")
        
        return content
    
    def _get_default_metadata(self, bwb_id: str) -> Dict[str, Any]:
        """Get default metadata for a BWB ID."""
        if bwb_id in self.common_laws:
            return self.common_laws[bwb_id].copy()
        
        return {
            "name_of_law": "Unknown Law",
            "citation_title": "Unknown",
            "date_of_entry_into_force": "Unknown",
            "regulatory_authority": "Unknown",
            "legal_domain": "Unknown",
            "identification_number": bwb_id
        }
    
    def _determine_law_type(self, law_name: str) -> str:
        """Determine the type of law based on its name."""
        law_name_lower = law_name.lower()
        
        if any(word in law_name_lower for word in ["bestuursrecht", "vergunning", "besluit"]):
            return "Administrative Law"
        elif any(word in law_name_lower for word in ["burgerlijk", "civiel", "contract"]):
            return "Civil Law"
        elif any(word in law_name_lower for word in ["strafrecht", "strafbaar", "misdrijf"]):
            return "Criminal Law"
        elif any(word in law_name_lower for word in ["grondwet", "constitutioneel"]):
            return "Constitutional Law"
        elif any(word in law_name_lower for word in ["arbeid", "werk", "loon"]):
            return "Employment Law"
        elif any(word in law_name_lower for word in ["discriminatie", "gelijke behandeling"]):
            return "Equal Treatment Law"
        
        return "Unknown"
    
    def search_laws(self, query: str, max_results: int = 10) -> List[Dict[str, str]]:
        """Search for laws matching the query."""
        try:
            # First try direct BWB ID if the query looks like one
            if re.match(r"^BWBR\d+$", query):
                try:
                    content = self.fetch_law_by_bwb_id(query)
                    metadata = self.parse_metadata(content)
                    return [{
                        "title": metadata.name_of_law,
                        "bwb_id": query,
                        "url": f"{self.BASE_URL}/{query}"
                    }]
                except Exception:
                    pass  # Fall back to regular search
            
            # Regular search
            params = {
                "zoeken_term": query
            }
            
            content = self._make_request(self.SEARCH_URL, params=params)
            soup = BeautifulSoup(content, "html.parser")
            
            results = []
            for element in soup.find_all(["div", "article"], class_=lambda x: x and ("result" in x.lower() or "wet" in x.lower())):
                try:
                    # Find title
                    title_element = element.find(["h3", "h2", "a"])
                    if not title_element:
                        continue
                    
                    title = title_element.get_text(strip=True)
                    
                    # Find BWB ID
                    link = element.find("a", href=re.compile(r"BWBR\d+"))
                    if not link:
                        continue
                    
                    href = link.get("href", "")
                    bwb_match = re.search(r"BWBR\d+", href)
                    if not bwb_match:
                        continue
                    
                    bwb_id = bwb_match.group(0)
                    url = f"{self.BASE_URL}{href}" if href.startswith("/") else href
                    
                    results.append({
                        "title": title,
                        "bwb_id": bwb_id,
                        "url": url
                    })
                    
                    if len(results) >= max_results:
                        break
                        
                except Exception as e:
                    logger.warning(f"Error processing search result: {e}")
                    continue
            
            return results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []


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
        print(f"Title: {mcp_law.metadata.name_of_law}")
        print(f"Status: {mcp_law.metadata.status}")
        print(f"Domain: {mcp_law.metadata.legal_domain}")