"""
Validate Mappings - Validates and corrects manual component mappings.
Provides interactive interface for reviewing and correcting mappings.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
import sys
from colorama import init, Fore, Style

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts.manual_processor import ManualProcessor, ManualInfo


class MappingValidator:
    """
    Validates and corrects manual component mappings.
    Provides interactive interface for reviewing and correcting mappings.
    """

    def __init__(self, mapping_path: str = "manual_mapping.json"):
        """
        Initialize the validator.
        
        Args:
            mapping_path: Path to the mapping file
        """
        self.mapping_path = mapping_path
        self.processor = ManualProcessor()
        self.mappings: Dict[str, Dict] = {}
        self.load_mappings()

    def load_mappings(self):
        """Load mappings from JSON file."""
        try:
            with open(self.mapping_path, "r") as f:
                self.mappings = json.load(f)
        except FileNotFoundError:
            print(f"Error: Mapping file {self.mapping_path} not found.")
            sys.exit(1)

    def save_mappings(self):
        """Save mappings to JSON file."""
        with open(self.mapping_path, "w") as f:
            json.dump(self.mappings, f, indent=4)

    def validate_mapping(self, filename: str, mapping: Dict) -> bool:
        """
        Validate a single mapping.
        
        Args:
            filename: Name of the manual file
            mapping: Mapping information
        
        Returns:
            True if mapping is valid, False otherwise
        """
        # Check required fields
        required_fields = ["component_type", "manufacturer", "manual_reference"]
        if not all(field in mapping for field in required_fields):
            print(f"{Fore.RED}Error: Missing required fields in mapping for {filename}{Style.RESET_ALL}")
            return False
        
        # Check component type
        if mapping["component_type"] not in self.processor._get_component_types():
            print(f"{Fore.RED}Error: Invalid component type '{mapping['component_type']}' for {filename}{Style.RESET_ALL}")
            return False
        
        # Check manufacturer
        if mapping["manufacturer"] not in self.processor._get_manufacturers().values():
            print(f"{Fore.RED}Error: Invalid manufacturer '{mapping['manufacturer']}' for {filename}{Style.RESET_ALL}")
            return False
        
        # Check file path
        if not Path(mapping["file_path"]).exists():
            print(f"{Fore.RED}Error: File not found at {mapping['file_path']}{Style.RESET_ALL}")
            return False
        
        return True

    def validate_all(self) -> Dict[str, List[str]]:
        """
        Validate all mappings.
        
        Returns:
            Dictionary of validation errors by filename
        """
        errors = {}
        for filename, mapping in self.mappings.items():
            if not self.validate_mapping(filename, mapping):
                errors[filename] = []
                # Add specific error messages
                if mapping["component_type"] not in self.processor._get_component_types():
                    errors[filename].append(f"Invalid component type: {mapping['component_type']}")
                if mapping["manufacturer"] not in self.processor._get_manufacturers().values():
                    errors[filename].append(f"Invalid manufacturer: {mapping['manufacturer']}")
                if not Path(mapping["file_path"]).exists():
                    errors[filename].append(f"File not found: {mapping['file_path']}")
        
        return errors

    def correct_mapping(self, filename: str):
        """
        Interactively correct a mapping.
        
        Args:
            filename: Name of the manual file to correct
        """
        if filename not in self.mappings:
            print(f"{Fore.RED}Error: No mapping found for {filename}{Style.RESET_ALL}")
            return
        
        mapping = self.mappings[filename]
        print(f"\n{Fore.CYAN}Correcting mapping for {filename}{Style.RESET_ALL}")
        
        # Show current mapping
        print("\nCurrent mapping:")
        for key, value in mapping.items():
            print(f"  {key}: {value}")
        
        # Get corrections
        print("\nEnter new values (press Enter to keep current value):")
        
        # Component type
        component_types = self.processor._get_component_types()
        print(f"\nAvailable component types: {', '.join(component_types)}")
        new_type = input(f"Component type [{mapping['component_type']}]: ").strip()
        if new_type and new_type in component_types:
            mapping["component_type"] = new_type
        
        # Manufacturer
        manufacturers = self.processor._get_manufacturers()
        print(f"\nAvailable manufacturers: {', '.join(manufacturers.values())}")
        new_manufacturer = input(f"Manufacturer [{mapping['manufacturer']}]: ").strip()
        if new_manufacturer and new_manufacturer in manufacturers.values():
            mapping["manufacturer"] = new_manufacturer
        
        # Model
        new_model = input(f"Model [{mapping.get('model', '')}]: ").strip()
        if new_model:
            mapping["model"] = new_model
        
        # Manual reference
        new_reference = input(f"Manual reference [{mapping['manual_reference']}]: ").strip()
        if new_reference:
            mapping["manual_reference"] = new_reference
        
        # Update file path
        mapping["file_path"] = str(
            self.processor.organized_dir / 
            mapping["component_type"] / 
            filename
        )
        
        # Save changes
        self.save_mappings()
        print(f"{Fore.GREEN}Mapping updated for {filename}{Style.RESET_ALL}")

    def interactive_validation(self):
        """Run interactive validation and correction process."""
        init()  # Initialize colorama
        
        while True:
            # Validate all mappings
            errors = self.validate_all()
            
            if not errors:
                print(f"{Fore.GREEN}All mappings are valid!{Style.RESET_ALL}")
                break
            
            # Show errors
            print(f"\n{Fore.YELLOW}Found {len(errors)} files with invalid mappings:{Style.RESET_ALL}")
            for filename, file_errors in errors.items():
                print(f"\n{filename}:")
                for error in file_errors:
                    print(f"  - {error}")
            
            # Ask for action
            print("\nOptions:")
            print("1. Correct a specific file")
            print("2. Exit")
            
            choice = input("\nEnter your choice (1-2): ").strip()
            
            if choice == "1":
                filename = input("Enter filename to correct: ").strip()
                if filename in errors:
                    self.correct_mapping(filename)
                else:
                    print(f"{Fore.RED}Error: No invalid mapping found for {filename}{Style.RESET_ALL}")
            elif choice == "2":
                break
            else:
                print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")


def main():
    """Main function to run the validation process."""
    validator = MappingValidator()
    validator.interactive_validation()


if __name__ == "__main__":
    main() 