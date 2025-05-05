"""
DiagnosticsEngine - Core logic for diagnosing refrigeration system faults.
Follows AI Coding Guidelines with modular design and apprentice-friendly comments.
"""

from typing import Dict, List, Optional, Union
from dataclasses import dataclass


@dataclass
class DiagnosticResult:
    """Structured output for diagnostic results following MCP format."""
    diagnosis: str
    confidence: float  # 0.0 to 1.0
    next_steps: List[str]
    safety_warnings: List[str]
    source_references: List[str]  # Manual references and section numbers


class DiagnosticsEngine:
    """
    Core diagnostic engine that evaluates refrigeration system symptoms
    and provides AI-enhanced fault detection with confidence levels.
    """

    def __init__(self):
        """Initialize the diagnostics engine with component thresholds."""
        # Load component specifications and thresholds
        self.component_specs = self._load_component_specs()
        
        # Initialize safety thresholds
        self.safety_thresholds = {
            "max_discharge_temp_f": 275,  # From Copeland AE4-1327
            "min_suction_pressure_psig": 20,  # For R-448A
            "max_superheat_f": 30,  # General guideline
            "min_subcooling_f": 5,  # General guideline
        }

    def _load_component_specs(self) -> Dict:
        """
        Load component specifications from JSON file.
        Returns structured data for compressors, valves, etc.
        """
        # TODO: Implement loading from component_specs.json
        return {}

    def diagnose(self, sensor_data: Dict[str, Union[float, bool]]) -> DiagnosticResult:
        """
        Main diagnostic function that evaluates sensor data and returns diagnosis.
        
        Args:
            sensor_data: Dictionary of sensor readings and alarm states
                Example: {
                    "suction_pressure_psig": 45.0,
                    "discharge_temp_f": 180.0,
                    "superheat_f": 15.0,
                    "subcooling_f": 10.0,
                    "compressor_amps": 12.5,
                    "alarms": ["high_discharge_temp"]
                }
        
        Returns:
            DiagnosticResult with diagnosis, confidence, next steps, and warnings
        """
        # Check for safety-critical conditions first
        safety_warnings = self._check_safety_conditions(sensor_data)
        
        # Analyze symptoms and calculate confidence
        diagnosis, confidence, next_steps = self._analyze_symptoms(sensor_data)
        
        # Get relevant manual references
        source_refs = self._get_source_references(diagnosis)
        
        return DiagnosticResult(
            diagnosis=diagnosis,
            confidence=confidence,
            next_steps=next_steps,
            safety_warnings=safety_warnings,
            source_references=source_refs
        )

    def _check_safety_conditions(self, data: Dict) -> List[str]:
        """
        Check for safety-critical conditions that require immediate attention.
        Returns list of safety warnings if any dangerous conditions are detected.
        """
        warnings = []
        
        # Check discharge temperature
        if data.get("discharge_temp_f", 0) > self.safety_thresholds["max_discharge_temp_f"]:
            warnings.append(
                f"CRITICAL: Discharge temperature {data['discharge_temp_f']}°F exceeds "
                f"maximum safe limit of {self.safety_thresholds['max_discharge_temp_f']}°F. "
                "Shut down if persistent."
            )
        
        # Check suction pressure
        if data.get("suction_pressure_psig", 0) < self.safety_thresholds["min_suction_pressure_psig"]:
            warnings.append(
                f"WARNING: Suction pressure {data['suction_pressure_psig']} psig below "
                f"minimum safe limit of {self.safety_thresholds['min_suction_pressure_psig']} psig. "
                "Check for low charge or restriction."
            )
        
        return warnings

    def _analyze_symptoms(self, data: Dict) -> tuple[str, float, List[str]]:
        """
        Analyze sensor data to determine the most likely fault condition.
        Returns tuple of (diagnosis, confidence, next_steps).
        """
        # Initialize with default values
        diagnosis = "No clear fault condition detected"
        confidence = 0.0
        next_steps = ["Continue monitoring system parameters"]
        
        # Check for low suction pressure with high superheat
        if (data.get("suction_pressure_psig", 0) < 35 and 
            data.get("superheat_f", 0) > 20):
            diagnosis = "Possible low refrigerant charge or liquid line restriction"
            confidence = 0.85
            next_steps = [
                "Check sight glass for bubbles",
                "Measure subcooling at condenser",
                "Inspect liquid line for restrictions",
                "Verify refrigerant charge"
            ]
        
        # Check for high discharge temperature
        elif data.get("discharge_temp_f", 0) > 200:
            diagnosis = "High discharge temperature condition"
            confidence = 0.90
            next_steps = [
                "Check condenser fan operation",
                "Verify condenser cleanliness",
                "Check for non-condensables",
                "Verify proper refrigerant charge"
            ]
        
        return diagnosis, confidence, next_steps

    def _get_source_references(self, diagnosis: str) -> List[str]:
        """
        Get relevant manual references for the given diagnosis.
        Returns list of manual references and section numbers.
        """
        # TODO: Implement vector search to find relevant manual sections
        return ["Copeland AE4-1327: Section 3.2", "Danfoss AKV Service Manual: Page 45"] 