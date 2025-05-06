"""
Manual Processor - Organizes and processes refrigeration manuals.
Handles file organization, component mapping, and manual processing.
"""

import os
import shutil
from pathlib import Path
import json
from typing import Dict, List, Optional
import re
from dataclasses import dataclass

# Add project root to Python path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from embeddings.embedding_pipeline import EmbeddingPipeline


@dataclass
class ManualInfo:
    """Information about a processed manual."""
    filename: str
    component_type: str
    manufacturer: str
    model: Optional[str]
    manual_reference: str
    file_path: str


class ManualProcessor:
    """
    Organizes and processes refrigeration manuals.
    Handles file organization, component mapping, and manual processing.
    """

    def __init__(self, base_dir: str = "manuals"):
        """
        Initialize the manual processor.
        
        Args:
            base_dir: Base directory for manual organization
        """
        self.base_dir = Path(base_dir)
        self.organized_dir = self.base_dir / "organized"
        self.processed_dir = self.base_dir / "processed"
        self.component_mapping: Dict[str, ManualInfo] = {}
        
        # Load configuration
        self.config = self._load_config()
        
        # Create directory structure
        self._create_directory_structure()

    def _load_config(self) -> Dict:
        """
        Load configuration from JSON file.
        
        Returns:
            Configuration dictionary
        """
        config_path = Path("config/manual_config.json")
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, "r") as f:
            return json.load(f)

    def _get_manufacturers(self) -> Dict[str, str]:
        """
        Get manufacturer mapping from configuration.
        
        Returns:
            Dictionary mapping manufacturer keys to full names
        """
        return self.config["manufacturers"]

    def _get_component_types(self) -> List[str]:
        """
        Get component types from configuration.
        
        Returns:
            List of component type names
        """
        return list(self.config["component_types"].keys())

    def _create_directory_structure(self):
        """Create the directory structure for manual organization."""
        # Main directories
        self.organized_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
        # Component type directories
        for component_type in self._get_component_types():
            (self.organized_dir / component_type).mkdir(exist_ok=True)

    def _extract_manual_info(self, filename: str) -> ManualInfo:
        """
        Extract information from manual filename.
        
        Args:
            filename: Name of the manual file
        
        Returns:
            ManualInfo object with extracted information
        """
        # Remove file extension and convert to lowercase
        name = Path(filename).stem.lower()
        
        # Try to identify manufacturer
        manufacturer = None
        for key, value in self._get_manufacturers().items():
            if key in name:
                manufacturer = value
                break
        
        # Try to identify component type
        component_type = None
        for type_name, type_info in self.config["component_types"].items():
            if any(keyword in name for keyword in type_info["keywords"]):
                component_type = type_name
                break
        
        # Extract model number if present
        model = None
        for pattern in self.config["model_patterns"]:
            model_match = re.search(pattern, name)
            if model_match:
                model = model_match.group()
                break
        
        return ManualInfo(
            filename=filename,
            component_type=component_type or "unknown",
            manufacturer=manufacturer or "Unknown",
            model=model,
            manual_reference=name,
            file_path=str(self.organized_dir / (component_type or "unknown") / filename)
        )

    def organize_manuals(self, source_dir: str):
        """
        Organize manuals into component-specific directories.
        
        Args:
            source_dir: Directory containing unorganized manuals
        """
        source_path = Path(source_dir)
        
        # Process each PDF file
        for pdf_file in source_path.glob("**/*.pdf"):
            # Extract information
            manual_info = self._extract_manual_info(pdf_file.name)
            
            # Copy to organized directory
            target_dir = self.organized_dir / manual_info.component_type
            target_dir.mkdir(exist_ok=True)
            shutil.copy2(pdf_file, target_dir / pdf_file.name)
            
            # Store mapping
            self.component_mapping[pdf_file.name] = manual_info
            
            print(f"Organized: {pdf_file.name} -> {manual_info.component_type}")

    def process_manuals(self):
        """Process organized manuals using the embedding pipeline."""
        pipeline = EmbeddingPipeline()
        
        # Process each component type directory
        for component_dir in self.organized_dir.iterdir():
            if component_dir.is_dir():
                print(f"\nProcessing {component_dir.name}...")
                
                # Create component mapping for this directory
                dir_mapping = {
                    info.manual_reference: info.component_type
                    for info in self.component_mapping.values()
                    if info.component_type == component_dir.name
                }
                
                # Process directory
                pipeline.process_directory(
                    str(component_dir),
                    component_mapping=dir_mapping
                )

    def update_component_specs(self, specs_path: str = "component_specs.json"):
        """
        Update component specifications with processed manual information.
        
        Args:
            specs_path: Path to component_specs.json
        """
        # Load current specs
        with open(specs_path, "r") as f:
            specs = json.load(f)
        
        # Update specs with manual information
        for manual_info in self.component_mapping.values():
            if manual_info.component_type in specs["components"]:
                # Find matching component by model number
                for component_name, component_data in specs["components"][manual_info.component_type].items():
                    if manual_info.model and manual_info.model in component_name:
                        component_data["manual_reference"] = manual_info.manual_reference
                        break
        
        # Save updated specs
        with open(specs_path, "w") as f:
            json.dump(specs, f, indent=4)

    def save_mapping(self, mapping_path: str = "manual_mapping.json"):
        """
        Save manual mapping to JSON file.
        
        Args:
            mapping_path: Path to save mapping file
        """
        # Convert ManualInfo objects to dictionaries
        mapping_dict = {
            filename: {
                "component_type": info.component_type,
                "manufacturer": info.manufacturer,
                "model": info.model,
                "manual_reference": info.manual_reference,
                "file_path": info.file_path
            }
            for filename, info in self.component_mapping.items()
        }
        
        # Save mapping
        with open(mapping_path, "w") as f:
            json.dump(mapping_dict, f, indent=4)


def main():
    """Main function to organize and process manuals."""
    # Initialize processor
    processor = ManualProcessor()
    
    # Organize manuals
    print("Organizing manuals...")
    processor.organize_manuals("manuals/raw")
    
    # Process manuals
    print("\nProcessing manuals...")
    processor.process_manuals()
    
    # Update component specs
    print("\nUpdating component specifications...")
    processor.update_component_specs()
    
    # Save mapping
    print("\nSaving manual mapping...")
    processor.save_mapping()
    
    print("\nManual processing complete!")


if __name__ == "__main__":
    main() 