"""
Structured Data Model for Clinical Evaluation Reports (CER)
Provides comprehensive data classes for semantic CER parsing and analysis.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum


class DeviceClass(Enum):
    """EU MDR Device Classifications"""
    CLASS_I = "I"
    CLASS_IIA = "IIa"
    CLASS_IIB = "IIb"
    CLASS_III = "III"


class RegulatoryRoute(Enum):
    """Regulatory pathways"""
    EU_MDR = "EU MDR"
    FDA_510K = "FDA 510(k)"
    FDA_PMA = "FDA PMA"
    FDA_DE_NOVO = "FDA De Novo"
    OTHER = "Other"


@dataclass
class DeviceIdentification:
    """Core device identification information with rich LLM analysis"""
    device_name: str = ""
    device_family: str = ""
    basic_udi_di: str = ""
    device_class: str = ""
    manufacturer: str = ""
    model_numbers: List[str] = field(default_factory=list)
    catalogue_numbers: List[str] = field(default_factory=list)
    
    # NEW: Rich LLM-generated descriptions
    device_description_detailed: str = ""
    clinical_application_detailed: str = ""
    
    def to_context_string(self) -> str:
        """Generate rich context string with detailed device understanding"""
        context = f"""=== DEVICE IDENTIFICATION ===

Device Name: {self.device_name}
Device Family: {self.device_family}
Class: {self.device_class}
Manufacturer: {self.manufacturer}
Models: {', '.join(self.model_numbers) if self.model_numbers else 'See CER'}

DETAILED DEVICE DESCRIPTION:
{self.device_description_detailed if self.device_description_detailed else 'Medical device as described in CER documentation.'}

CLINICAL APPLICATION:
{self.clinical_application_detailed if self.clinical_application_detailed else 'Clinical application per CER intended use.'}"""
        
        return context


@dataclass
class IntendedUse:
    """Device intended use and indications with rich clinical context"""
    intended_purpose: str = ""
    indications_for_use: List[str] = field(default_factory=list)
    contraindications: List[str] = field(default_factory=list)
    target_patient_population: str = ""
    clinical_application: str = ""
    intended_user: str = ""
    use_environment: str = ""
    
    # NEW: Rich LLM-generated clinical context
    clinical_context_detailed: str = ""
    usage_scenarios_detailed: str = ""
    
    def to_context_string(self) -> str:
        """Generate rich context with detailed clinical understanding"""
        context = f"""=== INTENDED USE & CLINICAL CONTEXT ===

Intended Purpose: {self.intended_purpose}

Indications: {chr(10).join(['- ' + ind for ind in self.indications_for_use]) if self.indications_for_use else 'See CER'}

Contraindications: {chr(10).join(['- ' + c for c in self.contraindications]) if self.contraindications else 'None stated'}

Target Population: {self.target_patient_population}
Clinical Application: {self.clinical_application}
Intended User: {self.intended_user}
Use Environment: {self.use_environment}

CLINICAL CONTEXT & MEDICAL NECESSITY:
{self.clinical_context_detailed if self.clinical_context_detailed else 'Clinical context per CER documentation.'}

USAGE SCENARIOS:
{self.usage_scenarios_detailed if self.usage_scenarios_detailed else 'Usage scenarios per CER intended use.'}"""
        
        return context


@dataclass
class PatientPopulation:
    """Target patient population characteristics"""
    age_range: str = ""
    gender_distribution: str = ""
    clinical_conditions: List[str] = field(default_factory=list)
    special_populations: List[str] = field(default_factory=list)
    comorbidities: List[str] = field(default_factory=list)
    estimated_size: str = ""
    geographic_distribution: str = ""
    
    def to_context_string(self) -> str:
        """Generate context string for LLM prompts"""
        return f"""Age Range: {self.age_range}
Gender: {self.gender_distribution}
Clinical Conditions: {', '.join(self.clinical_conditions) if self.clinical_conditions else 'See CER'}
Special Populations: {', '.join(self.special_populations) if self.special_populations else 'None'}"""


@dataclass
class ClinicalBenefit:
    """Clinical benefit information"""
    benefit_description: str = ""
    clinical_evidence: str = ""
    magnitude_of_benefit: str = ""
    supporting_studies: List[str] = field(default_factory=list)


@dataclass
class ResidualRisk:
    """Residual risk after mitigation"""
    risk_description: str = ""
    severity: str = ""
    probability: str = ""
    risk_level: str = ""
    mitigation_measures: List[str] = field(default_factory=list)
    acceptability_justification: str = ""


@dataclass
class LiteratureSearch:
    """Literature search methodology and results with detailed analysis"""
    search_date_start: Optional[str] = None
    search_date_end: Optional[str] = None
    databases_searched: List[str] = field(default_factory=list)
    search_terms: List[str] = field(default_factory=list)
    inclusion_criteria: List[str] = field(default_factory=list)
    exclusion_criteria: List[str] = field(default_factory=list)
    articles_screened: int = 0
    articles_included: int = 0
    key_findings: str = ""
    
    # NEW: Rich LLM-generated summaries
    search_methodology_details: str = ""
    clinical_evidence_summary: str = ""
    state_of_art_findings: str = ""
    
    def to_context_string(self) -> str:
        """Generate rich context string for LLM prompts with detailed analysis"""
        context = f"""=== LITERATURE SEARCH INFORMATION ===

Search Period: {self.search_date_start or 'Per CER'} to {self.search_date_end or 'Per CER'}
Databases: {', '.join(self.databases_searched) if self.databases_searched else 'Per CER methodology (PubMed, ClinicalTrials.gov, Embase)'}
Articles Screened: {self.articles_screened if self.articles_screened > 0 else 'Per CER documentation'}
Articles Included: {self.articles_included if self.articles_included > 0 else 'Per CER documentation'}

SEARCH METHODOLOGY:
{self.search_methodology_details if self.search_methodology_details else 'Systematic literature search conducted per CER protocol targeting peer-reviewed publications on device safety and performance.'}

KEY FINDINGS:
{self.key_findings if self.key_findings else 'Literature review findings documented in CER.'}

CLINICAL EVIDENCE FROM LITERATURE:
{self.clinical_evidence_summary if self.clinical_evidence_summary else 'Clinical evidence and safety data from literature review available in CER documentation.'}

STATE OF THE ART:
{self.state_of_art_findings if self.state_of_art_findings else 'State of the art analysis and comparative device information documented in CER.'}"""
        
        return context


@dataclass
class ClinicalStudy:
    """Clinical study information"""
    study_id: str = ""
    study_type: str = ""
    study_population_size: int = 0
    study_design: str = ""
    primary_endpoints: List[str] = field(default_factory=list)
    key_results: str = ""
    safety_outcomes: str = ""
    performance_outcomes: str = ""


@dataclass
class RegulatoryStatus:
    """Regulatory status and history"""
    ce_mark_date: Optional[str] = None
    notified_body: str = ""
    certificate_number: str = ""
    fda_status: str = ""
    other_regulatory_approvals: List[str] = field(default_factory=list)
    regulatory_route: str = ""


@dataclass
class MarketHistory:
    """Device market history"""
    first_market_date: Optional[str] = None
    markets_distributed: List[str] = field(default_factory=list)
    cumulative_units_sold: int = 0
    years_on_market: int = 0
    market_experience: str = ""


@dataclass
class TechnicalSpecification:
    """Technical device specifications"""
    device_description: str = ""
    principle_of_operation: str = ""
    materials: List[str] = field(default_factory=list)
    dimensions: str = ""
    sterility: str = ""
    shelf_life: str = ""
    key_features: List[str] = field(default_factory=list)


@dataclass
class StateOfTheArt:
    """State of the art information"""
    sota_summary: str = ""
    comparable_devices: List[str] = field(default_factory=list)
    technological_advances: str = ""
    clinical_practice_standards: str = ""


@dataclass
class DocumentSection:
    """Generic document section"""
    section_number: str = ""
    section_title: str = ""
    content: str = ""
    subsections: List['DocumentSection'] = field(default_factory=list)
    tables: List[Dict[str, Any]] = field(default_factory=list)
    figures: List[str] = field(default_factory=list)


@dataclass
class DocumentStructure:
    """CER document structure"""
    document_title: str = ""
    document_version: str = ""
    document_date: Optional[str] = None
    sections: List[DocumentSection] = field(default_factory=list)
    total_pages: int = 0
    
    def get_section_by_keyword(self, keyword: str) -> Optional[DocumentSection]:
        """Find section by keyword in title"""
        keyword_lower = keyword.lower()
        for section in self.sections:
            if keyword_lower in section.section_title.lower():
                return section
        return None


@dataclass
class SafetyData:
    """Safety data from CER"""
    adverse_events: List[str] = field(default_factory=list)
    device_related_complications: List[str] = field(default_factory=list)
    safety_conclusions: str = ""
    known_risks: List[ResidualRisk] = field(default_factory=list)


@dataclass
class PerformanceData:
    """Performance data from CER"""
    performance_metrics: Dict[str, str] = field(default_factory=dict)
    clinical_outcomes: List[str] = field(default_factory=list)
    performance_conclusions: str = ""
    effectiveness_data: str = ""


@dataclass
class BenefitRiskProfile:
    """Benefit-risk assessment"""
    benefits: List[ClinicalBenefit] = field(default_factory=list)
    risks: List[ResidualRisk] = field(default_factory=list)
    benefit_risk_conclusion: str = ""
    acceptability_justification: str = ""
    favorable_profile: bool = True


@dataclass
class CERData:
    """
    Complete CER semantic data model.
    Stores all extracted information from CER in structured format.
    """
    
    # Core Device Information
    device_identification: DeviceIdentification = field(default_factory=DeviceIdentification)
    intended_use: IntendedUse = field(default_factory=IntendedUse)
    technical_specifications: TechnicalSpecification = field(default_factory=TechnicalSpecification)
    
    # Clinical Information
    patient_population: PatientPopulation = field(default_factory=PatientPopulation)
    clinical_benefits: List[ClinicalBenefit] = field(default_factory=list)
    safety_data: SafetyData = field(default_factory=SafetyData)
    performance_data: PerformanceData = field(default_factory=PerformanceData)
    
    # Literature & Evidence
    literature_search: LiteratureSearch = field(default_factory=LiteratureSearch)
    clinical_studies: List[ClinicalStudy] = field(default_factory=list)
    state_of_the_art: StateOfTheArt = field(default_factory=StateOfTheArt)
    
    # Regulatory Context
    regulatory_status: RegulatoryStatus = field(default_factory=RegulatoryStatus)
    market_history: MarketHistory = field(default_factory=MarketHistory)
    
    # Benefit-Risk
    benefit_risk_profile: BenefitRiskProfile = field(default_factory=BenefitRiskProfile)
    
    # Document Metadata
    document_structure: DocumentStructure = field(default_factory=DocumentStructure)
    parsing_metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CERData':
        """Create from dictionary (for deserialization)"""
        # This is a simplified version - full implementation would handle nested objects
        cer_data = cls()
        
        # Populate fields from dict
        if 'device_identification' in data:
            cer_data.device_identification = DeviceIdentification(**data['device_identification'])
        if 'intended_use' in data:
            cer_data.intended_use = IntendedUse(**data['intended_use'])
        if 'patient_population' in data:
            cer_data.patient_population = PatientPopulation(**data['patient_population'])
        if 'literature_search' in data:
            cer_data.literature_search = LiteratureSearch(**data['literature_search'])
        if 'regulatory_status' in data:
            cer_data.regulatory_status = RegulatoryStatus(**data['regulatory_status'])
        if 'market_history' in data:
            cer_data.market_history = MarketHistory(**data['market_history'])
        if 'technical_specifications' in data:
            cer_data.technical_specifications = TechnicalSpecification(**data['technical_specifications'])
        if 'safety_data' in data:
            cer_data.safety_data = SafetyData(**data['safety_data'])
        if 'performance_data' in data:
            cer_data.performance_data = PerformanceData(**data['performance_data'])
        if 'state_of_the_art' in data:
            cer_data.state_of_the_art = StateOfTheArt(**data['state_of_the_art'])
        if 'benefit_risk_profile' in data:
            cer_data.benefit_risk_profile = BenefitRiskProfile(**data['benefit_risk_profile'])
        if 'document_structure' in data:
            cer_data.document_structure = DocumentStructure(**data['document_structure'])
        if 'parsing_metadata' in data:
            cer_data.parsing_metadata = data['parsing_metadata']
        
        return cer_data
    
    def get_device_context_for_llm(self) -> str:
        """Generate comprehensive device context string for LLM prompts"""
        return f"""=== DEVICE INFORMATION FROM CER ===

{self.device_identification.to_context_string()}

{self.intended_use.to_context_string()}

{self.patient_population.to_context_string()}

Technical Description: {self.technical_specifications.device_description[:500] if self.technical_specifications.device_description else 'See CER'}

Market History: {self.market_history.market_experience if self.market_history.market_experience else f'First marketed: {self.market_history.first_market_date}'}

Safety Profile: {self.safety_data.safety_conclusions[:300] if self.safety_data.safety_conclusions else 'See CER'}

Performance: {self.performance_data.performance_conclusions[:300] if self.performance_data.performance_conclusions else 'See CER'}"""
    
    def get_literature_context_for_llm(self) -> str:
        """Generate literature search context for LLM prompts"""
        return self.literature_search.to_context_string()
    
    def is_complete(self) -> bool:
        """Check if essential fields are populated"""
        return (
            bool(self.device_identification.device_name) and
            bool(self.intended_use.intended_purpose) and
            bool(self.patient_population.target_patient_population or self.patient_population.age_range)
        )
    
    def get_completeness_score(self) -> float:
        """Calculate completeness score (0.0 to 1.0)"""
        total_fields = 15
        filled_fields = 0
        
        if self.device_identification.device_name:
            filled_fields += 1
        if self.intended_use.intended_purpose:
            filled_fields += 1
        if self.patient_population.age_range:
            filled_fields += 1
        if self.technical_specifications.device_description:
            filled_fields += 1
        if self.literature_search.databases_searched:
            filled_fields += 1
        if self.safety_data.safety_conclusions:
            filled_fields += 1
        if self.performance_data.performance_conclusions:
            filled_fields += 1
        if self.market_history.first_market_date:
            filled_fields += 1
        if self.regulatory_status.ce_mark_date:
            filled_fields += 1
        if self.state_of_the_art.sota_summary:
            filled_fields += 1
        if self.benefit_risk_profile.benefit_risk_conclusion:
            filled_fields += 1
        if self.intended_use.contraindications:
            filled_fields += 1
        if self.clinical_benefits:
            filled_fields += 1
        if self.clinical_studies:
            filled_fields += 1
        if self.document_structure.sections:
            filled_fields += 1
        
        return filled_fields / total_fields

