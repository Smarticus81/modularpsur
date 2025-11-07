"""
Medical Device Entity Extraction Utilities
Specialized extractors for CER and regulatory documents using Anthropic Claude.
"""

from typing import List, Dict, Optional, Any
import anthropic
import os
import re


class MedicalDeviceEntityExtractor:
    """
    Extract medical device-specific entities from CER documents using Claude.
    Handles device identification, clinical data, regulatory information, etc.
    """
    
    def __init__(self, anthropic_client: anthropic.Anthropic = None):
        """
        Initialize entity extractor.
        
        Args:
            anthropic_client: Anthropic client instance. If None, creates new client.
        """
        if anthropic_client is None:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY required for semantic extraction")
            self.client = anthropic.Anthropic(api_key=api_key)
        else:
            self.client = anthropic_client
        
        self.model = "claude-sonnet-4-20250514"
    
    def extract_device_identification(self, text: str) -> Dict[str, Any]:
        """
        Extract AND UNDERSTAND device identification with deep LLM analysis.
        
        Args:
            text: CER text content
            
        Returns:
            Dict with device name, family, class, UDI, AND rich descriptions
        """
        prompt = f"""You are a medical device regulatory expert analyzing a Clinical Evaluation Report. READ AND UNDERSTAND the device deeply.

CER TEXT:
{text[:12000]}

CRITICAL: Extract ALL device information AND generate detailed descriptions showing your understanding.

Return comprehensive JSON:
{{
    "device_name": "exact full device name",
    "device_family": "product family/line name",
    "device_class": "EU MDR class",
    "basic_udi_di": "Basic UDI-DI if stated",
    "manufacturer": "manufacturer name",
    "model_numbers": ["all model numbers"],
    "catalogue_numbers": ["all catalogue numbers"],
    "device_description_detailed": "DETAILED 3-4 sentence description of what this device is, what it does, how it works, and what makes it unique. Include technical details, design features, and clinical purpose.",
    "clinical_application_detailed": "DETAILED 2-3 sentence description of HOW this device is used clinically, in what settings, by whom, and for what specific medical purposes."
}}

Show deep understanding through detailed descriptions."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=3000,
                temperature=0.2,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse JSON from response
            import json
            response_text = response.content[0].text
            
            # Extract JSON from response (handle markdown code blocks)
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(1)
            elif '```' in response_text:
                response_text = response_text.replace('```', '')
            
            result = json.loads(response_text)
            return result
            
        except Exception as e:
            print(f"  Warning: Could not extract device identification: {e}")
            return {}
    
    def extract_intended_use(self, text: str) -> Dict[str, Any]:
        """
        Extract AND ANALYZE intended use with comprehensive LLM understanding.
        
        Args:
            text: CER text content
            
        Returns:
            Dict with intended purpose, indications, AND detailed clinical context
        """
        prompt = f"""You are analyzing a medical device CER. DEEPLY UNDERSTAND the intended use and clinical context.

CER TEXT:
{text[:12000]}

UNDERSTAND: What is this device FOR? Who uses it? When? Why? What clinical problems does it solve?

Return comprehensive JSON:
{{
    "intended_purpose": "exact intended purpose statement from CER",
    "indications_for_use": ["complete list of indications"],
    "contraindications": ["complete list of contraindications"],
    "target_patient_population": "detailed patient population description",
    "clinical_application": "clinical application area",
    "intended_user": "intended users",
    "use_environment": "use environment",
    "clinical_context_detailed": "DETAILED 3-4 sentence explanation of the CLINICAL CONTEXT - what medical conditions require this device, what happens without it, what clinical outcomes it achieves, and why it's medically necessary.",
    "usage_scenarios_detailed": "DETAILED 2-3 sentence description of SPECIFIC USAGE SCENARIOS - when clinicians use this device, in what situations, during what procedures, and how it fits into the treatment pathway."
}}

Show deep clinical understanding through detailed context."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2500,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            
            import json
            response_text = response.content[0].text
            
            # Extract JSON
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(1)
            elif '```' in response_text:
                response_text = response_text.replace('```', '')
            
            result = json.loads(response_text)
            return result
            
        except Exception as e:
            print(f"  Warning: Could not extract intended use: {e}")
            return {}
    
    def extract_patient_population(self, text: str) -> Dict[str, Any]:
        """
        Extract patient population characteristics.
        
        Args:
            text: CER text content
            
        Returns:
            Dict with age range, gender, clinical conditions, etc.
        """
        prompt = f"""Extract patient population characteristics from the following medical device CER text.

TEXT:
{text[:8000]}

Extract and return ONLY the following information in JSON format:
{{
    "age_range": "age range of patients (e.g., neonates, 0-28 days, adults 18+)",
    "gender_distribution": "gender information (e.g., all genders, primarily female)",
    "clinical_conditions": ["list", "of", "conditions"],
    "special_populations": ["pediatric", "geriatric", "pregnant", "etc"],
    "comorbidities": ["relevant", "comorbidities"],
    "estimated_size": "population size estimate if mentioned",
    "geographic_distribution": "geographic info if mentioned"
}}

Extract as stated. Use empty strings/arrays if not found."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            
            import json
            response_text = response.content[0].text
            
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(1)
            elif '```' in response_text:
                response_text = response_text.replace('```', '')
            
            result = json.loads(response_text)
            return result
            
        except Exception as e:
            print(f"  Warning: Could not extract patient population: {e}")
            return {}
    
    def extract_literature_search_info(self, text: str) -> Dict[str, Any]:
        """
        Extract AND ANALYZE literature search methodology and results with LLM understanding.
        
        Args:
            text: CER text content
            
        Returns:
            Dict with search dates, databases, results, AND detailed analysis
        """
        prompt = f"""You are analyzing a Clinical Evaluation Report for a medical device. Your task is to deeply understand and extract comprehensive literature search information.

CER TEXT (Literature Section):
{text[:15000]}

CRITICAL REQUIREMENTS:
1. READ AND UNDERSTAND the literature search methodology in detail
2. Extract specific numbers, dates, databases, search strategies
3. ANALYZE the search results - what did they find? What conclusions?
4. Understand the clinical context and device-specific findings
5. Generate detailed summaries, not just bullet points

Return comprehensive JSON:
{{
    "search_date_start": "exact start date if mentioned",
    "search_date_end": "exact end date if mentioned",
    "databases_searched": ["list all databases mentioned"],
    "search_terms": ["list all search terms/strategies mentioned"],
    "inclusion_criteria": ["detailed inclusion criteria"],
    "exclusion_criteria": ["detailed exclusion criteria"],
    "articles_screened": number or 0,
    "articles_included": number or 0,
    "key_findings": "DETAILED 3-4 sentence summary of what the literature review found, including clinical evidence, safety data, performance outcomes, and state of the art findings. Be specific about device type, patient population, and clinical outcomes.",
    "search_methodology_details": "DETAILED 2-3 sentence description of HOW the search was conducted, what made it systematic, and what made it comprehensive",
    "clinical_evidence_summary": "DETAILED 3-4 sentence summary of the clinical evidence found in literature - specific studies, outcomes, safety profiles, performance data",
    "state_of_art_findings": "DETAILED 2-3 sentence summary of state of the art findings from literature - current clinical practice, comparable devices, technological standards"
}}

BE COMPREHENSIVE. Extract ALL details. Generate RICH summaries that show deep understanding of the literature review."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2500,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            
            import json
            response_text = response.content[0].text
            
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(1)
            elif '```' in response_text:
                response_text = response_text.replace('```', '')
            
            result = json.loads(response_text)
            return result
            
        except Exception as e:
            print(f"  Warning: Could not extract literature search info: {e}")
            return {}
    
    def extract_safety_data(self, text: str) -> Dict[str, Any]:
        """
        Extract safety data and conclusions.
        
        Args:
            text: CER text content
            
        Returns:
            Dict with adverse events, complications, safety conclusions
        """
        prompt = f"""Extract safety data from the following CER text.

TEXT:
{text[:8000]}

Extract and return ONLY the following information in JSON format:
{{
    "adverse_events": ["list", "of", "adverse events"],
    "device_related_complications": ["list", "of", "complications"],
    "safety_conclusions": "overall safety conclusions from CER",
    "known_risks": ["list", "of", "known risks"]
}}

Focus on device-specific safety information. Use empty arrays if not found."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            
            import json
            response_text = response.content[0].text
            
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(1)
            elif '```' in response_text:
                response_text = response_text.replace('```', '')
            
            result = json.loads(response_text)
            return result
            
        except Exception as e:
            print(f"  Warning: Could not extract safety data: {e}")
            return {}
    
    def extract_performance_data(self, text: str) -> Dict[str, Any]:
        """
        Extract performance data and conclusions.
        
        Args:
            text: CER text content
            
        Returns:
            Dict with performance metrics, outcomes, conclusions
        """
        prompt = f"""Extract performance data from the following CER text.

TEXT:
{text[:8000]}

Extract and return ONLY the following information in JSON format:
{{
    "performance_metrics": {{"metric_name": "metric_value"}},
    "clinical_outcomes": ["list", "of", "outcomes"],
    "performance_conclusions": "overall performance conclusions",
    "effectiveness_data": "effectiveness summary"
}}

Extract device performance and effectiveness data. Use empty structures if not found."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            
            import json
            response_text = response.content[0].text
            
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(1)
            elif '```' in response_text:
                response_text = response_text.replace('```', '')
            
            result = json.loads(response_text)
            return result
            
        except Exception as e:
            print(f"  Warning: Could not extract performance data: {e}")
            return {}
    
    def extract_regulatory_status(self, text: str) -> Dict[str, Any]:
        """
        Extract regulatory status and history.
        
        Args:
            text: CER text content
            
        Returns:
            Dict with CE mark date, FDA status, regulatory approvals
        """
        prompt = f"""Extract regulatory status information from the following CER text.

TEXT:
{text[:8000]}

Extract and return ONLY the following information in JSON format:
{{
    "ce_mark_date": "CE mark date if mentioned",
    "notified_body": "notified body name",
    "certificate_number": "certificate number",
    "fda_status": "FDA clearance/approval status",
    "other_regulatory_approvals": ["other", "approvals"],
    "regulatory_route": "regulatory pathway used"
}}

Extract regulatory information as stated. Use empty strings/arrays if not found."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            
            import json
            response_text = response.content[0].text
            
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(1)
            elif '```' in response_text:
                response_text = response_text.replace('```', '')
            
            result = json.loads(response_text)
            return result
            
        except Exception as e:
            print(f"  Warning: Could not extract regulatory status: {e}")
            return {}
    
    def extract_market_history(self, text: str) -> Dict[str, Any]:
        """
        Extract market history and distribution.
        
        Args:
            text: CER text content
            
        Returns:
            Dict with first market date, markets, units sold
        """
        prompt = f"""Extract market history information from the following CER text.

TEXT:
{text[:8000]}

Extract and return ONLY the following information in JSON format:
{{
    "first_market_date": "date device first marketed",
    "markets_distributed": ["list", "of", "markets/countries"],
    "cumulative_units_sold": 0,
    "years_on_market": 0,
    "market_experience": "summary of market experience"
}}

Extract market and distribution information. Use 0 for unknown numbers, empty arrays for lists."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            
            import json
            response_text = response.content[0].text
            
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(1)
            elif '```' in response_text:
                response_text = response_text.replace('```', '')
            
            result = json.loads(response_text)
            return result
            
        except Exception as e:
            print(f"  Warning: Could not extract market history: {e}")
            return {}

