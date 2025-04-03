"""
Legal Query Agent for Dutch Law MCP.

This module provides an AI agent that can answer legal questions
based on Dutch legislation in MCP format.
"""
import json
import logging
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Tuple

from ..api.client import MCPClient
from ..models.law_model import MCPLaw

logger = logging.getLogger(__name__)


@dataclass
class QueryResult:
    """Result of a legal query."""
    
    answer: str
    confidence: float
    relevant_articles: List[Dict[str, Any]]
    relevant_case_law: List[Dict[str, Any]]
    sources: List[str]
    explanation: Optional[str] = None


class ExpertiseLevel:
    """Expertise levels for the query agent."""
    
    LAYPERSON = "layperson"
    STUDENT = "student"
    PROFESSIONAL = "professional"
    EXPERT = "expert"


class LegalQueryAgent:
    """Agent for answering legal questions about Dutch law."""
    
    def __init__(
        self, 
        api_client: MCPClient,
        model_name: str = "legal-bert-dutch",
        expertise_level: str = ExpertiseLevel.LAYPERSON,
        include_case_law: bool = True,
        include_explanations: bool = True,
        max_results: int = 5
    ):
        """Initialize the legal query agent.
        
        Args:
            api_client: The MCP API client
            model_name: Name of the AI model to use
            expertise_level: Target expertise level for responses
            include_case_law: Whether to include case law in responses
            include_explanations: Whether to include explanations
            max_results: Maximum number of results to return
        """
        self.client = api_client
        self.model_name = model_name
        self.expertise_level = expertise_level
        self.include_case_law = include_case_law
        self.include_explanations = include_explanations
        self.max_results = max_results
        
        # Simple keyword mappings for demonstration purposes
        # In a real implementation, this would use vector embeddings or a more sophisticated approach
        self.domain_keywords = {
            "property": ["eigendom", "bezit", "zaak", "goed", "registergoed"],
            "contract": ["overeenkomst", "contract", "verbintenis", "wanprestatie"],
            "tort": ["onrechtmatige daad", "schade", "aansprakelijkheid"],
            "family": ["huwelijk", "echtscheiding", "alimentatie", "gezag", "ouderlijk"],
            "criminal": ["strafbaar", "misdrijf", "overtreding", "gevangenisstraf"],
            "administrative": ["besluit", "bestuursorgaan", "bezwaar", "beroep"],
            "tax": ["belasting", "fiscaal", "heffing", "aanslag"],
            "labor": ["arbeidsovereenkomst", "ontslag", "werknemer", "werkgever"],
            "business": ["vennootschap", "bestuurder", "onderneming", "fusie"]
        }
    
    def _extract_query_entities(self, query: str) -> Dict[str, Any]:
        """Extract entities from a query.
        
        Args:
            query: The query to extract entities from
            
        Returns:
            Dictionary with extracted entities
        """
        # This would use NLP in a real implementation
        # Here we use a very simple keyword-based approach
        
        entities = {
            "domains": [],
            "law_types": [],
            "specific_laws": [],
            "specific_articles": [],
            "question_type": None
        }
        
        # Detect legal domains
        for domain, keywords in self.domain_keywords.items():
            if any(keyword in query.lower() for keyword in keywords):
                entities["domains"].append(domain)
        
        # Detect specific laws (simple regex patterns)
        bw_match = re.search(r"burgerlijk(?:\s+wet)?(?:boek)?\s+(\d+)", query.lower())
        if bw_match:
            entities["specific_laws"].append(f"BW{bw_match.group(1)}")
        
        if "grondwet" in query.lower():
            entities["specific_laws"].append("Grondwet")
        
        if "algemene wet bestuursrecht" in query.lower() or "awb" in query.lower():
            entities["specific_laws"].append("AWB")
        
        # Detect specific articles
        article_match = re.search(r"artikel\s+(\d+[a-z]?(?::\d+)?)", query.lower())
        if article_match:
            entities["specific_articles"].append(article_match.group(1))
        
        # Determine question type
        if any(word in query.lower() for word in ["wat is", "wat zijn", "wat betekent", "definitie"]):
            entities["question_type"] = "definition"
        elif any(word in query.lower() for word in ["hoe", "procedure", "stappen"]):
            entities["question_type"] = "procedure"
        elif any(word in query.lower() for word in ["wanneer", "in welk geval"]):
            entities["question_type"] = "condition"
        elif any(word in query.lower() for word in ["mag", "moet", "verplicht", "verboden"]):
            entities["question_type"] = "obligation"
        
        return entities
    
    def _search_relevant_laws(self, query: str, entities: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search for laws relevant to the query.
        
        Args:
            query: The original query
            entities: Extracted entities from the query
            
        Returns:
            List of relevant laws
        """
        # If we have specific laws mentioned, search for those
        if entities["specific_laws"]:
            results = []
            for law_id in entities["specific_laws"]:
                # Map common abbreviations to potential search terms
                search_term = law_id
                if law_id.startswith("BW"):
                    search_term = f"Burgerlijk Wetboek {law_id[2:]}"
                elif law_id == "AWB":
                    search_term = "Algemene wet bestuursrecht"
                
                # Search for the specific law
                laws = self.client.search_laws(search_term)
                results.extend(laws)
            
            return results[:self.max_results]
        
        # If we have domains, search based on those
        if entities["domains"]:
            domain_terms = []
            for domain in entities["domains"]:
                if domain == "property":
                    domain_terms.append("eigendom")
                elif domain == "contract":
                    domain_terms.append("overeenkomst")
                elif domain == "tort":
                    domain_terms.append("onrechtmatige daad")
                # Add mappings for other domains
                
            # Search for each domain term and combine results
            results = []
            for term in domain_terms:
                laws = self.client.search_laws(term)
                results.extend(laws)
            
            # Remove duplicates (based on law ID)
            unique_results = []
            seen_ids = set()
            for law in results:
                if law["id"] not in seen_ids:
                    unique_results.append(law)
                    seen_ids.add(law["id"])
            
            return unique_results[:self.max_results]
        
        # If we have neither specific laws nor domains, search with the full query
        return self.client.search_laws(query)[:self.max_results]
    
    def _find_relevant_articles(self, laws: List[Dict[str, Any]], query: str, entities: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find articles relevant to the query within the given laws.
        
        Args:
            laws: List of laws to search in
            query: The original query
            entities: Extracted entities from the query
            
        Returns:
            List of relevant articles
        """
        relevant_articles = []
        
        # If we have specific articles, find those
        if entities["specific_articles"] and laws:
            for law in laws:
                law_id = law["id"]
                for article_id in entities["specific_articles"]:
                    try:
                        article = self.client.get_article(law_id, article_id)
                        relevant_articles.append(article)
                    except Exception as e:
                        logger.warning(f"Failed to get article {article_id} from law {law_id}: {e}")
        
        # Otherwise, search for relevant articles based on the query
        else:
            for law in laws:
                law_id = law["id"]
                
                # In a real implementation, this would use semantic search
                # For demonstration, we simulate retrieving relevant articles
                try:
                    # Simulate API call to search articles within a law
                    # In a real implementation, this would be a proper API call
                    article_search_results = [
                        {"id": "1", "title": "Article 1", "content": "This is article 1", "relevance": 0.85},
                        {"id": "2", "title": "Article 2", "content": "This is article 2", "relevance": 0.75},
                    ]
                    
                    relevant_articles.extend([
                        {**article, "law_id": law_id, "law_title": law["title"]}
                        for article in article_search_results
                    ])
                except Exception as e:
                    logger.warning(f"Failed to search articles in law {law_id}: {e}")
        
        # Sort by relevance and limit results
        relevant_articles.sort(key=lambda x: x.get("relevance", 0), reverse=True)
        return relevant_articles[:self.max_results]
    
    def _find_relevant_case_law(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find case law relevant to the given articles.
        
        Args:
            articles: List of articles to find case law for
            
        Returns:
            List of relevant case law
        """
        if not self.include_case_law:
            return []
        
        relevant_cases = []
        
        for article in articles:
            law_id = article.get("law_id")
            article_id = article.get("id")
            
            if law_id and article_id:
                try:
                    # In a real implementation, this would get cases specifically for an article
                    # For demonstration, we get cases for the whole law
                    cases = self.client.get_case_law(law_id)
                    
                    # Add source information
                    for case in cases:
                        case["source_article"] = article_id
                        case["source_law"] = law_id
                    
                    relevant_cases.extend(cases)
                except Exception as e:
                    logger.warning(f"Failed to get case law for article {article_id} in law {law_id}: {e}")
        
        # Remove duplicates and limit results
        unique_cases = []
        seen_case_ids = set()
        
        for case in relevant_cases:
            case_id = case.get("id")
            if case_id and case_id not in seen_case_ids:
                unique_cases.append(case)
                seen_case_ids.add(case_id)
        
        return unique_cases[:self.max_results]
    
    def _generate_explanation(self, query: str, entities: Dict[str, Any], articles: List[Dict[str, Any]], expertise_level: str) -> str:
        """Generate an explanation for the query result.
        
        Args:
            query: The original query
            entities: Extracted entities from the query
            articles: Relevant articles
            expertise_level: Target expertise level
            
        Returns:
            Explanation text
        """
        if not self.include_explanations:
            return None
        
        # This would use an LLM in a real implementation
        # For demonstration, we generate a simple explanation
        
        if expertise_level == ExpertiseLevel.LAYPERSON:
            explanation = "In simple terms: "
        elif expertise_level == ExpertiseLevel.STUDENT:
            explanation = "For law students: "
        elif expertise_level == ExpertiseLevel.PROFESSIONAL:
            explanation = "Professional legal analysis: "
        else:
            explanation = "Expert legal analysis: "
        
        # Add a basic explanation based on question type
        question_type = entities.get("question_type")
        
        if question_type == "definition":
            explanation += "This legal concept is defined in the cited articles. "
        elif question_type == "procedure":
            explanation += "The procedure is outlined in the following articles. "
        elif question_type == "condition":
            explanation += "The conditions are specified in the relevant legislation. "
        elif question_type == "obligation":
            explanation += "The legal obligations and requirements are as follows. "
        else:
            explanation += "The relevant legal provisions are: "
        
        # Add information about the articles
        if articles:
            explanation += f"There are {len(articles)} relevant articles that address this question. "
            
            # For simple explanations, summarize the first article
            if expertise_level == ExpertiseLevel.LAYPERSON and articles:
                article = articles[0]
                explanation += f"Most importantly, {article.get('title', 'the law')} states that [simplified explanation would go here]. "
        
        return explanation
    
    def query(self, question: str, expertise_level: Optional[str] = None) -> QueryResult:
        """Answer a legal question.
        
        Args:
            question: The legal question to answer
            expertise_level: Target expertise level for the response
            
        Returns:
            QueryResult with the answer and relevant information
        """
        # Use the provided expertise level or the default
        expertise = expertise_level or self.expertise_level
        
        # Extract entities from the query
        entities = self._extract_query_entities(question)
        logger.info(f"Extracted entities: {entities}")
        
        # Search for relevant laws
        relevant_laws = self._search_relevant_laws(question, entities)
        logger.info(f"Found {len(relevant_laws)} relevant laws")
        
        # Find relevant articles within those laws
        relevant_articles = self._find_relevant_articles(relevant_laws, question, entities)
        logger.info(f"Found {len(relevant_articles)} relevant articles")
        
        # Find relevant case law
        relevant_case_law = self._find_relevant_case_law(relevant_articles)
        logger.info(f"Found {len(relevant_case_law)} relevant cases")
        
        # Generate sources list
        sources = []
        for article in relevant_articles:
            law_title = article.get("law_title", "Unknown Law")
            article_id = article.get("id", "Unknown Article")
            sources.append(f"{law_title}, Article {article_id}")
        
        for case in relevant_case_law:
            case_name = case.get("name", "Unknown Case")
            case_reference = case.get("reference", "")
            if case_reference:
                sources.append(f"{case_name} ({case_reference})")
            else:
                sources.append(case_name)
        
        # Generate explanation
        explanation = self._generate_explanation(question, entities, relevant_articles, expertise)
        
        # In a real implementation, this would generate an answer using an LLM
        # For demonstration, we create a simple answer
        answer = f"Based on the Dutch legislation, "
        
        if relevant_articles:
            article = relevant_articles[0]
            answer += f"according to {article.get('law_title', 'the law')}, Article {article.get('id', '')}, "
        
        answer += "the answer to your question would involve [detailed answer would be generated here]."
        
        # Return the result
        return QueryResult(
            answer=answer,
            confidence=0.85,  # This would be calculated based on the model's confidence
            relevant_articles=relevant_articles,
            relevant_case_law=relevant_case_law,
            sources=sources,
            explanation=explanation
        )


# Example usage
if __name__ == "__main__":
    # Initialize client with mock URL
    client = MCPClient("https://api.dutchlawmcp.example.com", api_key="your_api_key")
    
    # Initialize the agent
    agent = LegalQueryAgent(
        api_client=client,
        expertise_level=ExpertiseLevel.LAYPERSON,
        include_case_law=True,
        include_explanations=True
    )
    
    # Example question
    question = "Wat zijn de vereisten voor een rechtsgeldig testament volgens het Burgerlijk Wetboek?"
    
    try:
        # Get the answer
        result = agent.query(question)
        
        print(f"Question: {question}\n")
        print(f"Answer: {result.answer}\n")
        
        if result.explanation:
            print(f"Explanation: {result.explanation}\n")
        
        print("Relevant Articles:")
        for article in result.relevant_articles:
            law_title = article.get("law_title", "Unknown Law")
            article_id = article.get("id", "Unknown")
            print(f"- {law_title}, Article {article_id}")
        
        print("\nRelevant Case Law:")
        for case in result.relevant_case_law:
            case_name = case.get("name", "Unknown Case")
            print(f"- {case_name}")
        
        print("\nSources:")
        for source in result.sources:
            print(f"- {source}")
        
    except Exception as e:
        print(f"Error: {e}")