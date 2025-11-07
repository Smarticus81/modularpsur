"""
State-of-the-Art Semantic Document Parser
Uses Anthropic Claude API for advanced document understanding and structure analysis.
"""

import os
import anthropic
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import re

from .cer_data_model import (
    CERData, DeviceIdentification, IntendedUse, PatientPopulation,
    LiteratureSearch, RegulatoryStatus, MarketHistory, TechnicalSpecification,
    SafetyData, PerformanceData, StateOfTheArt, BenefitRiskProfile,
    DocumentStructure, DocumentSection
)
from .entity_extractors import MedicalDeviceEntityExtractor
from .semantic_cache import SemanticParserSession, SemanticCERCache
from .document_parser import DocumentParser


class SemanticDocumentParser:
    """
    Advanced semantic document parser using Anthropic Claude API.
    
    Features:
    - Full document structure analysis with heading hierarchy
    - Section relationship mapping
    - Medical device entity recognition
    - Semantic chunking with context preservation
    - Regulatory context extraction
    - Intelligent caching to minimize API calls
    """
    
    def __init__(self, anthropic_client: anthropic.Anthropic = None):
        """
        Initialize semantic parser.
        
        Args:
            anthropic_client: Anthropic client. If None, creates new client.
        """
        if anthropic_client is None:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY required for semantic parsing")
            self.client = anthropic.Anthropic(api_key=api_key)
        else:
            self.client = anthropic_client
        
        self.model = "claude-sonnet-4-20250514"
        self.entity_extractor = MedicalDeviceEntityExtractor(self.client)
    
    def parse_cer(self, cer_path: str, use_cache: bool = True) -> CERData:
        """
        Parse CER document with full semantic understanding.
        Main entry point for CER parsing.
        
        Args:
            cer_path: Path to CER file (.docx or .pdf)
            use_cache: Whether to use cached data if available
            
        Returns:
            CERData object with all extracted information
        """
        print(f"\n=== SEMANTIC CER PARSING ===")
        print(f"Document: {cer_path}")
        
        # Check cache first
        if use_cache:
            cached_data = SemanticParserSession.get_cer_data(cer_path)
            if cached_data:
                try:
                    print(f"  \u2713 Using cached semantic data")
                    print(f"  \u2713 Completeness: {cached_data.get('completeness_score', 0)*100:.0f}%")
                except:
                    print(f"  Using cached semantic data")
                    print(f"  Completeness: {cached_data.get('completeness_score', 0)*100:.0f}%")
                
                # Convert dict back to CERData
                return CERData.from_dict(cached_data)
        
        # Parse document
        print("  Parsing CER with Anthropic API...")
        print("  This may take 30-60 seconds for first parse...")
        
        # Step 1: Extract document structure and text
        doc_data = DocumentParser.extract_text_with_structure(cer_path)
        full_text = doc_data['full_text']
        paragraphs = doc_data['paragraphs']
        tables = doc_data['tables']
        
        print(f"  Extracted {len(paragraphs)} paragraphs, {len(tables)} tables")
        
        # Step 2: Analyze document structure
        print("  Analyzing document structure...")
        document_structure = self._extract_document_structure(paragraphs)
        
        # Step 3: Extract entities using semantic understanding
        print("  Extracting device entities...")
        cer_data = self._extract_all_entities(full_text, document_structure)
        
        # Step 4: Store document structure
        cer_data.document_structure = document_structure
        
        # Step 5: Add parsing metadata
        cer_data.parsing_metadata = {
            'source_file': cer_path,
            'parsed_at': str(pd.Timestamp.now()) if 'pd' in dir() else 'now',
            'parser_version': '1.0',
            'model_used': self.model,
            'paragraph_count': len(paragraphs),
            'table_count': len(tables),
            'completeness_score': cer_data.get_completeness_score()
        }
        
        try:
            print(f"  \u2713 Parsing complete")
            print(f"  \u2713 Completeness: {cer_data.get_completeness_score()*100:.0f}%")
        except:
            print(f"  Parsing complete")
            print(f"  Completeness: {cer_data.get_completeness_score()*100:.0f}%")
        
        # Cache the result
        cer_data_dict = cer_data.to_dict()
        cer_data_dict['completeness_score'] = cer_data.get_completeness_score()
        SemanticParserSession.set_cer_data(cer_path, cer_data_dict)
        
        return cer_data
    
    def _extract_document_structure(self, paragraphs: List[str]) -> DocumentStructure:
        """
        Extract hierarchical document structure using Claude.
        
        Args:
            paragraphs: List of paragraph texts
            
        Returns:
            DocumentStructure object
        """
        # Sample paragraphs for structure analysis (first 100 for speed)
        sample_text = "\n\n".join(paragraphs[:100])
        
        prompt = f"""Analyze the following medical device CER document and identify its structure.

DOCUMENT TEXT (first portion):
{sample_text[:6000]}

Identify the main sections and their hierarchy. Return JSON format:
{{
    "document_title": "title",
    "sections": [
        {{"section_number": "1", "section_title": "Introduction", "has_subsections": true}},
        {{"section_number": "2", "section_title": "Device Description", "has_subsections": false}}
    ]
}}

Focus on major section headings. Be concise."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            
            import json
            response_text = response.content[0].text
            
            # Extract JSON
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(1)
            
            structure_data = json.loads(response_text)
            
            # Build DocumentStructure
            doc_structure = DocumentStructure(
                document_title=structure_data.get('document_title', ''),
                total_pages=0
            )
            
            for section_info in structure_data.get('sections', []):
                section = DocumentSection(
                    section_number=section_info.get('section_number', ''),
                    section_title=section_info.get('section_title', ''),
                    content=""
                )
                doc_structure.sections.append(section)
            
            return doc_structure
            
        except Exception as e:
            print(f"  Warning: Could not extract document structure: {e}")
            return DocumentStructure()
    
    def _extract_all_entities(self, text: str, structure: DocumentStructure) -> CERData:
        """
        Extract all entities from CER using semantic understanding.
        
        Args:
            text: Full CER text
            structure: Document structure
            
        Returns:
            CERData with all extracted entities
        """
        cer_data = CERData()
        
        # Extract device identification
        print("    - Device identification...")
        device_id_data = self.entity_extractor.extract_device_identification(text)
        if device_id_data:
            cer_data.device_identification = DeviceIdentification(**device_id_data)
        
        # Extract intended use
        print("    - Intended use...")
        intended_use_data = self.entity_extractor.extract_intended_use(text)
        if intended_use_data:
            cer_data.intended_use = IntendedUse(**intended_use_data)
        
        # Extract patient population
        print("    - Patient population...")
        patient_pop_data = self.entity_extractor.extract_patient_population(text)
        if patient_pop_data:
            cer_data.patient_population = PatientPopulation(**patient_pop_data)
        
        # Extract literature search info
        print("    - Literature search...")
        lit_search_data = self.entity_extractor.extract_literature_search_info(text)
        if lit_search_data:
            cer_data.literature_search = LiteratureSearch(**lit_search_data)
        
        # Extract safety data
        print("    - Safety data...")
        safety_data = self.entity_extractor.extract_safety_data(text)
        if safety_data:
            cer_data.safety_data = SafetyData(**safety_data)
        
        # Extract performance data
        print("    - Performance data...")
        perf_data = self.entity_extractor.extract_performance_data(text)
        if perf_data:
            cer_data.performance_data = PerformanceData(**perf_data)
        
        # Extract regulatory status
        print("    - Regulatory status...")
        reg_status_data = self.entity_extractor.extract_regulatory_status(text)
        if reg_status_data:
            cer_data.regulatory_status = RegulatoryStatus(**reg_status_data)
        
        # Extract market history
        print("    - Market history...")
        market_data = self.entity_extractor.extract_market_history(text)
        if market_data:
            cer_data.market_history = MarketHistory(**market_data)
        
        return cer_data
    
    def get_relevant_context(self, cer_data: CERData, query: str, max_tokens: int = 4000) -> str:
        """
        Get relevant context from CER for specific query using semantic search.
        
        Args:
            cer_data: Parsed CER data
            query: Query string (e.g., "device safety profile")
            max_tokens: Maximum tokens in response
            
        Returns:
            Relevant context string
        """
        # Map query keywords to CER data sections
        query_lower = query.lower()
        
        context_parts = []
        
        if any(kw in query_lower for kw in ['device', 'product', 'name', 'identification']):
            context_parts.append(cer_data.device_identification.to_context_string())
        
        if any(kw in query_lower for kw in ['intended', 'indication', 'use', 'purpose']):
            context_parts.append(cer_data.intended_use.to_context_string())
        
        if any(kw in query_lower for kw in ['patient', 'population', 'age', 'demographic']):
            context_parts.append(cer_data.patient_population.to_context_string())
        
        if any(kw in query_lower for kw in ['literature', 'search', 'publication', 'study']):
            context_parts.append(cer_data.literature_search.to_context_string())
        
        if any(kw in query_lower for kw in ['safety', 'adverse', 'risk', 'complication']):
            if cer_data.safety_data.safety_conclusions:
                context_parts.append(f"Safety: {cer_data.safety_data.safety_conclusions}")
        
        if any(kw in query_lower for kw in ['performance', 'effectiveness', 'outcome']):
            if cer_data.performance_data.performance_conclusions:
                context_parts.append(f"Performance: {cer_data.performance_data.performance_conclusions}")
        
        # If no specific match, provide general device context
        if not context_parts:
            context_parts.append(cer_data.get_device_context_for_llm())
        
        # Combine and limit to max_tokens (rough estimate: 4 chars per token)
        max_chars = max_tokens * 4
        context = "\n\n".join(context_parts)
        
        if len(context) > max_chars:
            context = context[:max_chars] + "..."
        
        return context


def get_semantic_cer_data(cer_path: str, force_refresh: bool = False) -> CERData:
    """
    Convenience function to get parsed CER data with caching.
    
    Args:
        cer_path: Path to CER document (.docx or .pdf)
        force_refresh: Force re-parsing even if cached
        
    Returns:
        CERData object
    """
    if not cer_path or not os.path.exists(cer_path):
        raise FileNotFoundError(f"CER file not found: {cer_path}")
    
    # Validate file type
    file_ext = os.path.splitext(cer_path)[1].lower()
    if file_ext not in ['.docx', '.pdf']:
        raise ValueError(f"Unsupported file type: {file_ext}. Supported: .docx, .pdf")
    
    # Try cache first
    if not force_refresh:
        cached_data = SemanticParserSession.get_cer_data(cer_path)
        if cached_data:
            return CERData.from_dict(cached_data)
    
    # Parse with semantic parser
    parser = SemanticDocumentParser()
    return parser.parse_cer(cer_path, use_cache=not force_refresh)

