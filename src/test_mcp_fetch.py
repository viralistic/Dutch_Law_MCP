"""
Test script to fetch and convert Dutch law to MCP format.
"""
import logging
from src.models.wetten_parser import WettenParser
from src.api.client import MCPClient

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Initialize parser
    parser = WettenParser()
    
    # Test with Algemene wet bestuursrecht (General Administrative Law Act)
    bwb_id = "BWBR0005537"
    
    try:
        # First test: Search for the law
        logger.info("Searching for Algemene wet bestuursrecht...")
        search_results = parser.search_laws("Algemene wet bestuursrecht")
        logger.info(f"Found {len(search_results)} results")
        for result in search_results:
            logger.info(f"- {result['title']} (BWB ID: {result['bwb_id']})")
        
        # Second test: Parse the law into MCP format
        logger.info(f"\nFetching and parsing law with BWB ID: {bwb_id}...")
        mcp_law = parser.parse_law_to_mcp(bwb_id)
        
        # Display the parsed information
        metadata = mcp_law.identification_and_basic_data.metadata
        logger.info("\nParsed Law Information:")
        logger.info(f"Name: {metadata.name_of_law}")
        logger.info(f"Citation: {metadata.citation_title}")
        logger.info(f"BWB ID: {metadata.identification_number}")
        logger.info(f"Domain: {metadata.legal_domain}")
        logger.info(f"Authority: {metadata.regulatory_authority}")
        logger.info(f"Status: {metadata.status}")
        logger.info(f"Entry into force: {metadata.date_of_entry_into_force}")
        
        # Third test: Try to submit to API (if available)
        try:
            client = MCPClient("https://api.wetten.overheid.nl")
            response = client.submit_law(mcp_law)
            logger.info("\nAPI Submission successful!")
            logger.info(f"API Response: {response}")
        except Exception as e:
            logger.warning(f"\nAPI submission skipped (expected in test environment): {e}")
        
    except Exception as e:
        logger.error(f"Error during testing: {e}")

if __name__ == "__main__":
    main() 