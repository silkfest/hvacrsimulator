"""
RackSimulator - Simulates a supermarket refrigeration rack system.
Provides realistic sensor data and equipment states for training and testing.
"""

from typing import Dict, List, Optional, Union
from dataclasses import dataclass
import random


@dataclass
class RackState:
    """Current state of the refrigeration rack system."""
    suction_pressure_psig: float
    discharge_pressure_psig: float
    discharge_temp_f: float
    superheat_f: float
    subcooling_f: float
    compressor_amps: float
    condenser_fan_speed: int  # 0-100%
    liquid_line_temp_f: float
    alarms: List[str]


class RackSimulator:
    """
    Simulates a supermarket refrigeration rack system with realistic
    sensor behavior and equipment states.
    """

    def __init__(self):
        """Initialize the rack simulator with default values."""
        # Normal operating ranges for R-448A
        self.normal_ranges = {
            "suction_pressure_psig": (35, 45),
            "discharge_pressure_psig": (180, 220),
            "discharge_temp_f": (160, 200),
            "superheat_f": (8, 15),
            "subcooling_f": (8, 15),
            "compressor_amps": (10, 15),
            "condenser_fan_speed": (60, 100),
            "liquid_line_temp_f": (90, 110)
        }
        
        # Initialize with normal operating values
        self.current_state = self._generate_normal_state()

    def _generate_normal_state(self) -> RackState:
        """Generate a normal operating state within acceptable ranges."""
        return RackState(
            suction_pressure_psig=random.uniform(*self.normal_ranges["suction_pressure_psig"]),
            discharge_pressure_psig=random.uniform(*self.normal_ranges["discharge_pressure_psig"]),
            discharge_temp_f=random.uniform(*self.normal_ranges["discharge_temp_f"]),
            superheat_f=random.uniform(*self.normal_ranges["superheat_f"]),
            subcooling_f=random.uniform(*self.normal_ranges["subcooling_f"]),
            compressor_amps=random.uniform(*self.normal_ranges["compressor_amps"]),
            condenser_fan_speed=random.randint(*self.normal_ranges["condenser_fan_speed"]),
            liquid_line_temp_f=random.uniform(*self.normal_ranges["liquid_line_temp_f"]),
            alarms=[]
        )

    def simulate_fault(self, fault_type: str) -> RackState:
        """
        Simulate a specific fault condition in the rack system.
        
        Args:
            fault_type: Type of fault to simulate
                Options: "low_charge", "high_discharge_temp", "low_suction_pressure"
        
        Returns:
            Updated RackState with simulated fault conditions
        """
        # Start with normal state
        self.current_state = self._generate_normal_state()
        
        if fault_type == "low_charge":
            self._simulate_low_charge()
        elif fault_type == "high_discharge_temp":
            self._simulate_high_discharge_temp()
        elif fault_type == "low_suction_pressure":
            self._simulate_low_suction_pressure()
        
        return self.current_state

    def _simulate_low_charge(self):
        """Simulate symptoms of low refrigerant charge."""
        self.current_state.suction_pressure_psig *= 0.7  # Reduce by 30%
        self.current_state.superheat_f *= 1.5  # Increase by 50%
        self.current_state.subcooling_f *= 0.5  # Reduce by 50%
        self.current_state.discharge_temp_f *= 1.2  # Increase by 20%
        self.current_state.alarms.append("low_suction_pressure")

    def _simulate_high_discharge_temp(self):
        """Simulate symptoms of high discharge temperature."""
        self.current_state.discharge_temp_f = 250  # Set to dangerous level
        self.current_state.discharge_pressure_psig *= 1.3  # Increase by 30%
        self.current_state.condenser_fan_speed = 30  # Reduce fan speed
        self.current_state.alarms.append("high_discharge_temp")

    def _simulate_low_suction_pressure(self):
        """Simulate symptoms of low suction pressure."""
        self.current_state.suction_pressure_psig = 25  # Set to low level
        self.current_state.superheat_f = 25  # Increase superheat
        self.current_state.compressor_amps *= 0.8  # Reduce compressor load
        self.current_state.alarms.append("low_suction_pressure")

    def get_current_state(self) -> Dict[str, Union[float, List[str]]]:
        """
        Get the current state of the rack system as a dictionary.
        Returns sensor values and alarms in a format suitable for diagnostics.
        """
        return {
            "suction_pressure_psig": self.current_state.suction_pressure_psig,
            "discharge_pressure_psig": self.current_state.discharge_pressure_psig,
            "discharge_temp_f": self.current_state.discharge_temp_f,
            "superheat_f": self.current_state.superheat_f,
            "subcooling_f": self.current_state.subcooling_f,
            "compressor_amps": self.current_state.compressor_amps,
            "condenser_fan_speed": self.current_state.condenser_fan_speed,
            "liquid_line_temp_f": self.current_state.liquid_line_temp_f,
            "alarms": self.current_state.alarms
        } 