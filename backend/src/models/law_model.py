"""
Data models for Dutch Law MCP system.
"""
from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import List, Dict, Optional, Any


class LawStatus(str, Enum):
    IN_FORCE = "In force"
    REPEALED = "Repealed"
    FUTURE = "Future"


@dataclass
class Metadata:
    name_of_law: str
    citation_title: str
    identification_number: str
    legal_domain: str
    regulatory_authority: str
    date_of_entry_into_force: date
    version: str
    status: LawStatus
    
    
@dataclass
class HierarchicalPosition:
    relationship_to_constitution: Optional[str] = None
    relationship_to_eu_law: Optional[str] = None
    relationship_to_international_treaties: Optional[str] = None
    position_within_national_legislation: Optional[str] = None


@dataclass
class IdentificationAndBasicData:
    metadata: Metadata
    hierarchical_position: HierarchicalPosition


@dataclass
class Amendment:
    date: date
    description: str
    reference: str


@dataclass
class PlannedAmendment:
    date: date
    description: str
    status: str


@dataclass
class LegislativeHistory:
    initiator: Optional[str] = None
    reason: Optional[str] = None
    bill: Optional[str] = None
    parliamentary_treatment: Optional[str] = None
    important_changes: Optional[str] = None


@dataclass
class AmendmentHistory:
    amendments: List[Amendment] = field(default_factory=list)
    planned_amendments: List[PlannedAmendment] = field(default_factory=list)


@dataclass
class HistoricalContext:
    legislative_history: LegislativeHistory = field(default_factory=LegislativeHistory)
    amendment_history: AmendmentHistory = field(default_factory=AmendmentHistory)


@dataclass
class CoreProvision:
    article: str
    description: str


@dataclass
class Definition:
    term: str
    definition: str


@dataclass
class StructuralOverview:
    chapter_structure: Optional[str] = None
    core_provisions: List[CoreProvision] = field(default_factory=list)
    definitions: List[Definition] = field(default_factory=list)
    delegation_provisions: List[str] = field(default_factory=list)


@dataclass
class ConceptualCategory:
    category: str
    concepts: List[str] = field(default_factory=list)


@dataclass
class SemanticRelationships:
    conceptual_categories: List[ConceptualCategory] = field(default_factory=list)
    legal_relationships: Optional[str] = None
    procedural_flowcharts: Optional[str] = None


@dataclass
class ContentMapping:
    structural_overview: StructuralOverview = field(default_factory=StructuralOverview)
    semantic_relationships: SemanticRelationships = field(default_factory=SemanticRelationships)


@dataclass
class LandmarkCase:
    case: str
    reference: str
    significance: str


@dataclass
class CaseLaw:
    landmark_cases: List[LandmarkCase] = field(default_factory=list)
    supreme_court_opinions: List[str] = field(default_factory=list)
    international_case_law: List[str] = field(default_factory=list)


@dataclass
class Doctrine:
    key_literature: List[str] = field(default_factory=list)
    academic_views: Optional[str] = None
    relevant_annotations: List[str] = field(default_factory=list)


@dataclass
class InterpretativeContext:
    case_law: CaseLaw = field(default_factory=CaseLaw)
    doctrine: Doctrine = field(default_factory=Doctrine)


@dataclass
class ImplementationPractice:
    responsible_authorities: List[str] = field(default_factory=list)
    policy_rules: List[str] = field(default_factory=list)
    supervision_and_enforcement: List[str] = field(default_factory=list)


@dataclass
class SocietalImpact:
    target_groups: List[str] = field(default_factory=list)
    practical_issues: List[str] = field(default_factory=list)
    evaluations: List[str] = field(default_factory=list)


@dataclass
class PracticalApplication:
    implementation_practice: ImplementationPractice = field(default_factory=ImplementationPractice)
    societal_impact: SocietalImpact = field(default_factory=SocietalImpact)


@dataclass
class TechnicalSpecifications:
    api_access: Optional[str] = None
    linked_data: Optional[str] = None
    persistent_identifiers: Optional[str] = None


@dataclass
class UserInteraction:
    visualization_tools: List[str] = field(default_factory=list)
    search_methods: List[str] = field(default_factory=list)
    notification_systems: List[str] = field(default_factory=list)


@dataclass
class DigitalIntegration:
    technical_specifications: TechnicalSpecifications = field(default_factory=TechnicalSpecifications)
    user_interaction: UserInteraction = field(default_factory=UserInteraction)


@dataclass
class PlannedDevelopments:
    intended_changes: List[str] = field(default_factory=list)
    current_policy_discussions: List[str] = field(default_factory=list)
    innovative_applications: List[str] = field(default_factory=list)


@dataclass
class RisksAndOpportunities:
    identified_gaps: List[str] = field(default_factory=list)
    technological_challenges: List[str] = field(default_factory=list)
    harmonization_possibilities: List[str] = field(default_factory=list)


@dataclass
class FuturePerspective:
    planned_developments: PlannedDevelopments = field(default_factory=PlannedDevelopments)
    risks_and_opportunities: RisksAndOpportunities = field(default_factory=RisksAndOpportunities)


@dataclass
class LinguisticAspects:
    readability_index: Optional[str] = None
    alternatives_in_plain_language: Optional[str] = None
    multilingual_versions: List[str] = field(default_factory=list)


@dataclass
class Inclusivity:
    accessibility_for_people_with_disabilities: Optional[str] = None
    cultural_context: Optional[str] = None
    educational_resources: List[str] = field(default_factory=list)


@dataclass
class Accessibility:
    linguistic_aspects: LinguisticAspects = field(default_factory=LinguisticAspects)
    inclusivity: Inclusivity = field(default_factory=Inclusivity)


@dataclass
class MCPLaw:
    """Model for representing a law in the MCP system."""
    metadata: Dict[str, Any]
    content: Dict[str, Any]
    
    def __post_init__(self):
        """Validate the law data after initialization."""
        required_metadata = [
            "name_of_law",
            "citation_title",
            "date_of_entry_into_force",
            "regulatory_authority",
            "legal_domain",
            "identification_number"
        ]
        
        for field in required_metadata:
            if field not in self.metadata:
                self.metadata[field] = "Unknown"
        
        if "articles" not in self.content:
            self.content["articles"] = []
        if "chapters" not in self.content:
            self.content["chapters"] = []
        if "sections" not in self.content:
            self.content["sections"] = []

    historical_context: HistoricalContext = field(default_factory=HistoricalContext)
    content_mapping: ContentMapping = field(default_factory=ContentMapping)
    interpretative_context: InterpretativeContext = field(default_factory=InterpretativeContext)
    practical_application: PracticalApplication = field(default_factory=PracticalApplication)
    digital_integration: DigitalIntegration = field(default_factory=DigitalIntegration)
    future_perspective: FuturePerspective = field(default_factory=FuturePerspective)
    accessibility: Accessibility = field(default_factory=Accessibility)