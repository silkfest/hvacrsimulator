# main.py — Starter Scaffold for Supermarket Rack Simulator

from diagnostics.engine import DiagnosticsEngine
from simulator.rack_simulator import RackSimulator
from llm.interface import LLMInterface
from ui.cli import SimulatorCLI


def main():
    print("Initializing Supermarket Rack Simulator...")

    # Set up modules
    simulator = RackSimulator()
    diagnostics = DiagnosticsEngine()
    llm = LLMInterface(provider="gemini")  # Default can be Gemini, OpenAI later
    cli = SimulatorCLI(simulator, diagnostics, llm)

    # Launch interface
    cli.run()


if __name__ == "__main__":
    main()
