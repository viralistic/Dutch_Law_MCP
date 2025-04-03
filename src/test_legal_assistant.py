"""
Test script to verify MCP's ability to provide reliable legal assistance.
"""
import logging
from typing import List, Dict, Any, Set
from src.models.wetten_parser import WettenParser
from src.models.law_model import MCPLaw

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LegalAssistant:
    """Test class to verify MCP's legal assistance capabilities."""
    
    def __init__(self):
        self.parser = WettenParser()
        # Common law categories and their BWB IDs
        self.law_categories = {
            "administrative": "BWBR0005537",  # Algemene wet bestuursrecht
            "civil": "BWBR0005291",  # Burgerlijk Wetboek
            "criminal": "BWBR0001854",  # Wetboek van Strafrecht
            "constitutional": "BWBR0001840",  # Grondwet
            "employment": "BWBR0009405",  # Wet op de arbeidsovereenkomst
            "discrimination": "BWBR0006502",  # Algemene wet gelijke behandeling
        }
        
        # Keywords for law categorization
        self.category_keywords = {
            "administrative": [
                "bestuur", "gemeente", "overheid", "vergunning", "besluit",
                "boete", "parkeren", "aanvragen", "procedure", "bezwaar",
                "vergunning", "toestemming", "handhaving"
            ],
            "civil": [
                "contract", "schade", "eigendom", "huur", "koop",
                "verhuur", "verkoop", "aansprakelijk", "schulden", "betaling",
                "overeenkomst", "verbintenis", "wanprestatie"
            ],
            "criminal": [
                "strafbaar", "overtreding", "boete", "politie",
                "misdrijf", "strafrecht", "veroordeling", "gevangenis",
                "aangifte", "delict", "straf"
            ],
            "constitutional": [
                "recht", "grondrecht", "discriminatie", "vrijheid",
                "mensenrechten", "grondwet", "gelijke behandeling",
                "fundamenteel", "constitutioneel"
            ],
            "employment": [
                "werk", "baas", "werknemer", "salaris", "contract",
                "ontslag", "arbeid", "werkgever", "loon", "CAO",
                "dienstverband", "arbeidsvoorwaarden", "werktijden"
            ],
            "discrimination": [
                "discriminatie", "gelijke behandeling", "ras", "geslacht",
                "leeftijd", "handicap", "afkomst", "religie", "seksuele oriëntatie",
                "ongelijke behandeling", "uitsluiting", "vooroordelen", "intimidatie",
                "pesten", "ongelijkheid"
            ]
        }
        
        # Define related categories that should be considered together
        self.related_categories = {
            "discrimination": ["employment", "constitutional"],
            "employment": ["civil", "discrimination"],
            "administrative": ["constitutional"],
        }
    
    def analyze_situation(self, situation: str) -> Dict[str, Any]:
        """Analyze a legal situation and find relevant laws."""
        logger.info(f"\nAnalyzing situation: {situation}")
        
        # First, try to identify relevant law categories
        relevant_categories = self._identify_relevant_categories(situation)
        logger.info(f"Identified relevant categories: {relevant_categories}")
        
        # Add related categories
        expanded_categories = self._expand_categories(relevant_categories)
        logger.info(f"Expanded categories: {expanded_categories}")
        
        # Fetch and analyze relevant laws
        relevant_laws = []
        for category in expanded_categories:
            if category in self.law_categories:
                try:
                    law = self.parser.parse_law_to_mcp(self.law_categories[category])
                    relevant_laws.append(law)
                    logger.info(f"Successfully parsed {category} law")
                except Exception as e:
                    logger.error(f"Failed to parse {category} law: {e}")
        
        # Analyze the laws and provide structured advice
        advice = self._generate_advice(situation, relevant_laws, expanded_categories)
        
        return {
            "situation": situation,
            "relevant_categories": list(expanded_categories),
            "relevant_laws": [law.metadata["name_of_law"] for law in relevant_laws],
            "advice": advice,
            "references": self._extract_references(relevant_laws)
        }
    
    def _identify_relevant_categories(self, situation: str) -> Set[str]:
        """Identify which law categories are relevant to the situation."""
        categories = set()
        situation_lower = situation.lower()
        
        # Check each category's keywords
        for category, keywords in self.category_keywords.items():
            if any(keyword in situation_lower for keyword in keywords):
                categories.add(category)
        
        return categories
    
    def _expand_categories(self, categories: Set[str]) -> Set[str]:
        """Expand categories with related categories."""
        expanded = categories.copy()
        for category in categories:
            if category in self.related_categories:
                expanded.update(self.related_categories[category])
        return expanded
    
    def _generate_advice(self, situation: str, laws: List[MCPLaw], categories: Set[str]) -> str:
        """Generate advice based on relevant laws."""
        if not laws:
            return "Geen relevante wetgeving gevonden voor deze situatie."
        
        advice_parts = []
        
        # First, add general information about each law
        for law in laws:
            metadata = law.metadata
            advice_parts.append(
                f"De {metadata['name_of_law']} ({metadata['citation_title']}) is relevant voor uw situatie. "
                f"Deze wet is van kracht sinds {metadata['date_of_entry_into_force']} en wordt beheerd door "
                f"{metadata['regulatory_authority']}."
            )
        
        # Then, add specific advice based on the categories
        if "discrimination" in categories:
            # Find relevant articles from the discrimination law
            discrimination_law = next((law for law in laws if law.metadata["legal_domain"] == "Equal Treatment Law"), None)
            if discrimination_law and discrimination_law.content["articles"]:
                relevant_articles = [
                    article for article in discrimination_law.content["articles"]
                    if any(keyword in article["text"].lower() for keyword in ["discriminatie", "gelijke behandeling"])
                ]
                if relevant_articles:
                    advice_parts.append("\nRelevante artikelen uit de Algemene wet gelijke behandeling:")
                    for article in relevant_articles[:3]:  # Show up to 3 relevant articles
                        advice_parts.append(f"- Artikel {article['number']}: {article['title']}")
            
            advice_parts.append(
                "\nBij discriminatie heeft u verschillende rechtsmiddelen tot uw beschikking:\n"
                "1. U kunt een klacht indienen bij het College voor de Rechten van de Mens\n"
                "2. U kunt contact opnemen met een antidiscriminatiebureau in uw regio\n"
                "3. U kunt juridische bijstand zoeken via het Juridisch Loket of een advocaat\n"
                "4. In geval van strafbare discriminatie kunt u aangifte doen bij de politie"
            )
            
            if "employment" in categories:
                # Find relevant articles from the employment law
                employment_law = next((law for law in laws if law.metadata["legal_domain"] == "Employment Law"), None)
                if employment_law and employment_law.content["articles"]:
                    relevant_articles = [
                        article for article in employment_law.content["articles"]
                        if any(keyword in article["text"].lower() for keyword in ["discriminatie", "gelijke behandeling", "arbeidsvoorwaarden"])
                    ]
                    if relevant_articles:
                        advice_parts.append("\nRelevante artikelen uit de Wet op de arbeidsovereenkomst:")
                        for article in relevant_articles[:3]:  # Show up to 3 relevant articles
                            advice_parts.append(f"- Artikel {article['number']}: {article['title']}")
                
                advice_parts.append(
                    "\nSpecifiek voor discriminatie op het werk:\n"
                    "1. Meld de situatie eerst bij uw leidinggevende of HR-afdeling\n"
                    "2. Neem contact op met de vertrouwenspersoon binnen uw organisatie\n"
                    "3. Schakel uw ondernemingsraad in als die er is\n"
                    "4. Overweeg contact met een vakbond voor juridische ondersteuning"
                )
        
        elif "employment" in categories:
            # Find relevant articles from the employment law
            employment_law = next((law for law in laws if law.metadata["legal_domain"] == "Employment Law"), None)
            if employment_law and employment_law.content["articles"]:
                relevant_articles = [
                    article for article in employment_law.content["articles"]
                    if any(keyword in article["text"].lower() for keyword in ["arbeidsovereenkomst", "ontslag", "salaris"])
                ]
                if relevant_articles:
                    advice_parts.append("\nRelevante artikelen uit de Wet op de arbeidsovereenkomst:")
                    for article in relevant_articles[:3]:  # Show up to 3 relevant articles
                        advice_parts.append(f"- Artikel {article['number']}: {article['title']}")
            
            advice_parts.append(
                "\nBij arbeidsrechtelijke kwesties:\n"
                "1. Controleer uw arbeidsovereenkomst en de CAO\n"
                "2. Neem contact op met uw vakbond of een arbeidsrechtadvocaat\n"
                "3. Het Juridisch Loket kan u informeren over uw rechten\n"
                "4. Bewaar alle relevante documenten en correspondentie"
            )
        
        elif "administrative" in categories:
            # Find relevant articles from the administrative law
            administrative_law = next((law for law in laws if law.metadata["legal_domain"] == "Administrative Law"), None)
            if administrative_law and administrative_law.content["articles"]:
                relevant_articles = [
                    article for article in administrative_law.content["articles"]
                    if any(keyword in article["text"].lower() for keyword in ["bezwaar", "beroep", "besluit"])
                ]
                if relevant_articles:
                    advice_parts.append("\nRelevante artikelen uit de Algemene wet bestuursrecht:")
                    for article in relevant_articles[:3]:  # Show up to 3 relevant articles
                        advice_parts.append(f"- Artikel {article['number']}: {article['title']}")
            
            advice_parts.append(
                "\nVoor procedures met de overheid:\n"
                "1. Let op de bezwaartermijn (meestal 6 weken)\n"
                "2. Verzamel alle relevante documenten\n"
                "3. Overweeg juridische bijstand via het Juridisch Loket\n"
                "4. U kunt vaak gratis advies krijgen bij uw gemeente"
            )
        
        elif "civil" in categories:
            # Find relevant articles from the civil law
            civil_law = next((law for law in laws if law.metadata["legal_domain"] == "Civil Law"), None)
            if civil_law and civil_law.content["articles"]:
                relevant_articles = [
                    article for article in civil_law.content["articles"]
                    if any(keyword in article["text"].lower() for keyword in ["contract", "huur", "koop"])
                ]
                if relevant_articles:
                    advice_parts.append("\nRelevante artikelen uit het Burgerlijk Wetboek:")
                    for article in relevant_articles[:3]:  # Show up to 3 relevant articles
                        advice_parts.append(f"- Artikel {article['number']}: {article['title']}")
            
            advice_parts.append(
                "\nBij civielrechtelijke geschillen:\n"
                "1. Verzamel alle relevante documenten en correspondentie\n"
                "2. Probeer eerst in overleg tot een oplossing te komen\n"
                "3. Overweeg mediation als alternatief voor een rechtszaak\n"
                "4. Zoek tijdig juridische bijstand als een oplossing uitblijft"
            )
        
        return "\n\n".join(advice_parts)
    
    def _extract_references(self, laws: List[MCPLaw]) -> List[Dict[str, str]]:
        """Extract specific references from the laws."""
        references = []
        for law in laws:
            metadata = law.metadata
            references.append({
                "name": metadata["name_of_law"],
                "citation": metadata["citation_title"],
                "bwb_id": metadata["identification_number"],
                "domain": metadata["legal_domain"],
                "entry_force": metadata["date_of_entry_into_force"],
                "authority": metadata["regulatory_authority"]
            })
        return references

def main():
    assistant = LegalAssistant()
    
    # Test cases
    test_situations = [
        "Ik heb een boete gekregen van de gemeente voor het parkeren van mijn auto.",
        "Mijn huurbaas wil mijn huurcontract niet verlengen.",
        "Ik word gediscrimineerd op mijn werk vanwege mijn afkomst.",
        "Ik wil een vergunning aanvragen voor mijn bedrijf.",
        "Ik word gepest op mijn werk vanwege mijn geaardheid.",
        "Mijn werkgever weigert mij promotie te geven vanwege mijn leeftijd."
    ]
    
    for situation in test_situations:
        result = assistant.analyze_situation(situation)
        print("\n" + "="*50)
        print(f"Situatie: {result['situation']}")
        print(f"Relevante categorieën: {', '.join(result['relevant_categories'])}")
        print(f"Relevante wetten: {', '.join(result['relevant_laws'])}")
        print(f"\nAdvies:\n{result['advice']}")
        print("\nReferenties:")
        for ref in result['references']:
            print(f"- {ref['name']} ({ref['citation']})")
            print(f"  BWB ID: {ref['bwb_id']}")
            print(f"  Domein: {ref['domain']}")
            print(f"  Inwerkingtreding: {ref['entry_force']}")
            print(f"  Bevoegd gezag: {ref['authority']}")
        print("="*50)

if __name__ == "__main__":
    main() 