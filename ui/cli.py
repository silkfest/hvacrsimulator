"""
SimulatorCLI - Command-line interface for the refrigeration rack simulator.
Provides an interactive way to simulate faults and get AI-powered diagnoses.
"""

from typing import Dict, List, Optional, Union
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm


class SimulatorCLI:
    """
    Command-line interface for interacting with the refrigeration simulator.
    Provides a user-friendly way to simulate faults and view diagnoses.
    """

    def __init__(self, simulator, diagnostics, llm):
        """
        Initialize the CLI with required components.
        
        Args:
            simulator: RackSimulator instance
            diagnostics: DiagnosticsEngine instance
            llm: LLMInterface instance
        """
        self.simulator = simulator
        self.diagnostics = diagnostics
        self.llm = llm
        self.console = Console()

    def run(self):
        """Main CLI loop."""
        self.console.print(Panel.fit(
            "[bold blue]Supermarket Refrigeration Rack Simulator[/bold blue]\n"
            "Interactive training and diagnostic tool",
            title="Welcome"
        ))

        while True:
            self._show_menu()
            choice = Prompt.ask("Select an option", choices=["1", "2", "3", "q"])
            
            if choice == "q":
                break
            elif choice == "1":
                self._simulate_fault()
            elif choice == "2":
                self._show_current_state()
            elif choice == "3":
                self._get_diagnosis()

    def _show_menu(self):
        """Display the main menu options."""
        self.console.print("\n[bold]Main Menu:[/bold]")
        self.console.print("1. Simulate Fault")
        self.console.print("2. Show Current State")
        self.console.print("3. Get Diagnosis")
        self.console.print("q. Quit")

    def _simulate_fault(self):
        """Simulate a fault condition."""
        self.console.print("\n[bold]Available Fault Types:[/bold]")
        self.console.print("1. Low Refrigerant Charge")
        self.console.print("2. High Discharge Temperature")
        self.console.print("3. Low Suction Pressure")
        
        choice = Prompt.ask("Select fault type", choices=["1", "2", "3"])
        
        fault_map = {
            "1": "low_charge",
            "2": "high_discharge_temp",
            "3": "low_suction_pressure"
        }
        
        fault_type = fault_map[choice]
        self.simulator.simulate_fault(fault_type)
        
        self.console.print("\n[green]Fault condition simulated successfully![/green]")
        self._show_current_state()

    def _show_current_state(self):
        """Display the current system state in a formatted table."""
        state = self.simulator.get_current_state()
        
        table = Table(title="Current System State")
        table.add_column("Parameter", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in state.items():
            if key != "alarms":
                table.add_row(key, str(value))
        
        self.console.print(table)
        
        if state["alarms"]:
            self.console.print("\n[bold red]Active Alarms:[/bold red]")
            for alarm in state["alarms"]:
                self.console.print(f"• {alarm}")

    def _get_diagnosis(self):
        """Get AI-powered diagnosis for current state."""
        state = self.simulator.get_current_state()
        
        # Get diagnosis from diagnostics engine
        result = self.diagnostics.diagnose(state)
        
        # Display diagnosis
        self.console.print("\n[bold]Diagnosis Results:[/bold]")
        self.console.print(Panel(
            f"[bold]Diagnosis:[/bold] {result.diagnosis}\n"
            f"[bold]Confidence:[/bold] {result.confidence:.2f}",
            title="Diagnosis"
        ))
        
        # Display next steps
        if result.next_steps:
            self.console.print("\n[bold]Recommended Next Steps:[/bold]")
            for step in result.next_steps:
                self.console.print(f"• {step}")
        
        # Display safety warnings
        if result.safety_warnings:
            self.console.print("\n[bold red]Safety Warnings:[/bold red]")
            for warning in result.safety_warnings:
                self.console.print(f"⚠️ {warning}")
        
        # Display source references
        if result.source_references:
            self.console.print("\n[bold]Source References:[/bold]")
            for ref in result.source_references:
                self.console.print(f"• {ref}")
        
        # Ask if user wants to get LLM analysis
        if Confirm.ask("\nWould you like AI analysis of this diagnosis?"):
            self._get_llm_analysis(state, result)

    def _get_llm_analysis(self, state: Dict, diagnosis_result):
        """Get additional analysis from LLM."""
        # TODO: Implement vector search to get relevant manual sections
        manual_context = ["Sample manual section 1", "Sample manual section 2"]
        
        try:
            llm_response = self.llm.ask_llm(state, manual_context)
            
            self.console.print("\n[bold]AI Analysis:[/bold]")
            self.console.print(Panel(
                llm_response.text,
                title="LLM Response"
            ))
            
            if llm_response.source_references:
                self.console.print("\n[bold]Additional References:[/bold]")
                for ref in llm_response.source_references:
                    self.console.print(f"• {ref}")
                    
        except Exception as e:
            self.console.print(f"\n[red]Error getting AI analysis: {str(e)}[/red]") 