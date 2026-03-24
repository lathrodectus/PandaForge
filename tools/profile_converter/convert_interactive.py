#!/usr/bin/env python3
"""
Pandaforge Profile Converter - Interactive CLI

Internal tool for converting OrcaSlicer profiles to Pandaforge format.
Uses project paths automatically and provides interactive selection.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Set
from orca_to_pandaforge import ProfileConverter


class PrinterModel:
    """Represents a single printer model"""
    def __init__(self, name: str, file: str, gcode_flavor: str):
        self.name = name
        self.file = file
        self.gcode_flavor = gcode_flavor
        self.is_klipper = gcode_flavor == "klipper"


class PrinterBrand:
    """Represents a printer brand with its models"""
    def __init__(self, name: str, path: Path):
        self.name = name
        self.path = path
        self.models: List[PrinterModel] = []
        self._scan_models()

    def _scan_models(self):
        """Scan for printer models in this brand's directory"""
        machine_dir = self.path / "machine"
        if not machine_dir.exists():
            return

        for profile_file in machine_dir.glob("*.json"):
            try:
                with open(profile_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data.get("instantiation") == "true":
                        model_name = data.get("name", profile_file.stem)
                        gcode_flavor = data.get("gcode_flavor", "unknown")
                        self.models.append(PrinterModel(model_name, profile_file.name, gcode_flavor))
            except Exception as e:
                pass

        self.models.sort(key=lambda x: x.name)

    @property
    def klipper_count(self):
        return sum(1 for m in self.models if m.is_klipper)


def print_header():
    """Print header"""
    print("\n" + "="*70)
    print("  PANDAFORGE PROFILE CONVERTER - Interactive CLI")
    print("  Internal Tool - Automatic Path Configuration")
    print("="*70 + "\n")


def scan_brands(orca_profiles_dir: Path) -> Dict[str, PrinterBrand]:
    """Scan for available brands"""
    print("Scanning for printer brands...")
    brands = {}

    for brand_dir in sorted(orca_profiles_dir.iterdir()):
        if brand_dir.is_dir() and not brand_dir.name.startswith("."):
            if (brand_dir / "machine").exists():
                brand = PrinterBrand(brand_dir.name, brand_dir)
                if brand.models:
                    brands[brand.name] = brand

    return brands


def select_brands(brands: Dict[str, PrinterBrand]) -> List[str]:
    """Interactive brand selection"""
    print("\n" + "="*70)
    print("AVAILABLE BRANDS")
    print("="*70 + "\n")

    brand_list = sorted(brands.keys())

    # Display brands with numbers
    for i, brand_name in enumerate(brand_list, 1):
        brand = brands[brand_name]
        klipper_text = f"({brand.klipper_count} Klipper)" if brand.klipper_count > 0 else ""
        print(f"  [{i:2d}] {brand_name:30s} - {len(brand.models):2d} models {klipper_text}")

    print(f"\n  [A]  Select All Brands")
    print(f"  [K]  Select All Klipper Printers Only")
    print(f"  [Q]  Quit")

    print("\n" + "-"*70)
    print("Enter brand numbers (comma-separated), A for all, K for Klipper, or Q to quit:")
    print("Example: 1,3,5  or  1-5  or  A  or  K")
    print("-"*70)

    while True:
        choice = input("\nYour selection: ").strip().upper()

        if choice == 'Q':
            print("\nExiting...")
            sys.exit(0)

        if choice == 'A':
            return brand_list

        if choice == 'K':
            # Return only brands with Klipper printers
            return [name for name, brand in brands.items() if brand.klipper_count > 0]

        # Parse number selection
        try:
            selected = []
            parts = choice.split(',')

            for part in parts:
                part = part.strip()
                if '-' in part:
                    # Range like 1-5
                    start, end = part.split('-')
                    start, end = int(start.strip()), int(end.strip())
                    for i in range(start, end + 1):
                        if 1 <= i <= len(brand_list):
                            selected.append(brand_list[i-1])
                else:
                    # Single number
                    i = int(part)
                    if 1 <= i <= len(brand_list):
                        selected.append(brand_list[i-1])

            if selected:
                return selected
            else:
                print("❌ No valid brands selected. Try again.")

        except ValueError:
            print("❌ Invalid input. Use numbers (1,2,3), ranges (1-5), A for all, or K for Klipper.")


def select_printers(brand_name: str, brand: PrinterBrand) -> List[str]:
    """Interactive printer selection for a brand"""
    print("\n" + "="*70)
    print(f"PRINTERS IN {brand_name}")
    print("="*70 + "\n")

    # Display printers with numbers
    for i, model in enumerate(brand.models, 1):
        klipper_text = "✓ Klipper" if model.is_klipper else ""
        print(f"  [{i:2d}] {model.name:50s} {klipper_text}")

    print(f"\n  [A]  Select All Printers in {brand_name}")
    print(f"  [K]  Select All Klipper Printers Only")
    print(f"  [S]  Skip this brand")

    print("\n" + "-"*70)
    print("Enter printer numbers (comma-separated), A for all, K for Klipper, or S to skip:")
    print("Example: 1,3,5  or  1-5  or  A  or  K")
    print("-"*70)

    while True:
        choice = input("\nYour selection: ").strip().upper()

        if choice == 'S':
            return []

        if choice == 'A':
            return [model.name for model in brand.models]

        if choice == 'K':
            return [model.name for model in brand.models if model.is_klipper]

        # Parse number selection
        try:
            selected = []
            parts = choice.split(',')

            for part in parts:
                part = part.strip()
                if '-' in part:
                    # Range like 1-5
                    start, end = part.split('-')
                    start, end = int(start.strip()), int(end.strip())
                    for i in range(start, end + 1):
                        if 1 <= i <= len(brand.models):
                            selected.append(brand.models[i-1].name)
                else:
                    # Single number
                    i = int(part)
                    if 1 <= i <= len(brand.models):
                        selected.append(brand.models[i-1].name)

            if selected:
                return selected
            else:
                print("❌ No valid printers selected. Try again.")

        except ValueError:
            print("❌ Invalid input. Use numbers (1,2,3), ranges (1-5), A for all, or K for Klipper.")


def confirm_conversion(selections: Dict[str, List[str]], brands: Dict[str, PrinterBrand]) -> bool:
    """Confirm conversion with user"""
    print("\n" + "="*70)
    print("CONVERSION SUMMARY")
    print("="*70 + "\n")

    total_printers = 0
    for brand_name, printer_names in selections.items():
        if printer_names:  # All printers
            count = len(brands[brand_name].models) if not printer_names else len(printer_names)
            total_printers += count
            if len(printer_names) == len(brands[brand_name].models):
                print(f"  • {brand_name}: All printers ({count} models)")
            else:
                print(f"  • {brand_name}: {count} selected printers")
                for printer_name in printer_names[:3]:
                    print(f"      - {printer_name}")
                if len(printer_names) > 3:
                    print(f"      ... and {len(printer_names) - 3} more")

    print(f"\nTotal: {len(selections)} brands, {total_printers} printers")
    print("\n" + "-"*70)

    while True:
        choice = input("Proceed with conversion? (Y/N): ").strip().upper()
        if choice == 'Y':
            return True
        elif choice == 'N':
            return False


def convert_profiles(selections: Dict[str, List[str]], brands: Dict[str, PrinterBrand], output_dir: Path):
    """Convert selected profiles"""
    print("\n" + "="*70)
    print("CONVERTING PROFILES")
    print("="*70 + "\n")

    for i, (brand_name, printer_names) in enumerate(selections.items(), 1):
        brand = brands[brand_name]

        print(f"\n[{i}/{len(selections)}] Converting {brand_name}...")
        print("-"*70)

        output_path = output_dir / brand_name
        converter = ProfileConverter(brand.path, output_path, brand_name)

        try:
            converter.convert_all()
            print(f"✅ {brand_name} converted successfully")
        except Exception as e:
            print(f"❌ Error converting {brand_name}: {e}")

    print("\n" + "="*70)
    print("✅ CONVERSION COMPLETE!")
    print("="*70)
    print(f"\nOutput directory: {output_dir}")


def main():
    """Main entry point"""
    # Automatic path configuration
    project_root = Path(__file__).parent.parent.parent
    orca_profiles_dir = project_root / "OrcaSlicer-main" / "resources" / "profiles"
    output_dir = project_root / "BambuStudio-2.5.0.66" / "resources" / "profiles"

    print_header()

    # Show paths
    print("Project Paths (Automatic):")
    print(f"  Source: {orca_profiles_dir}")
    print(f"  Output: {output_dir}")

    # Check paths exist
    if not orca_profiles_dir.exists():
        print(f"\n❌ Error: OrcaSlicer profiles not found at {orca_profiles_dir}")
        sys.exit(1)

    # Scan brands
    brands = scan_brands(orca_profiles_dir)

    if not brands:
        print("\n❌ No printer brands found")
        sys.exit(1)

    print(f"\n✅ Found {len(brands)} brands with {sum(len(b.models) for b in brands.values())} total printers")

    # Select brands
    selected_brands = select_brands(brands)

    if not selected_brands:
        print("\n❌ No brands selected")
        sys.exit(1)

    # For each brand, select printers
    selections = {}

    for brand_name in selected_brands:
        brand = brands[brand_name]

        # Ask if user wants to select specific printers or all
        print(f"\n{'='*70}")
        print(f"Brand: {brand_name} ({len(brand.models)} printers, {brand.klipper_count} Klipper)")
        print('='*70)
        print("\nOptions:")
        print("  [A] Convert all printers in this brand")
        print("  [S] Select specific printers")
        print("  [K] Skip this brand")

        while True:
            choice = input("\nYour choice (A/S/K): ").strip().upper()

            if choice == 'A':
                selections[brand_name] = [model.name for model in brand.models]
                print(f"✓ Selected all {len(brand.models)} printers")
                break
            elif choice == 'S':
                selected_printers = select_printers(brand_name, brand)
                if selected_printers:
                    selections[brand_name] = selected_printers
                    print(f"✓ Selected {len(selected_printers)} printers")
                break
            elif choice == 'K':
                print(f"⊘ Skipped {brand_name}")
                break
            else:
                print("❌ Invalid choice. Use A, S, or K.")

    if not selections:
        print("\n❌ No printers selected for conversion")
        sys.exit(1)

    # Confirm and convert
    if confirm_conversion(selections, brands):
        convert_profiles(selections, brands, output_dir)
    else:
        print("\n⊘ Conversion cancelled")
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⊘ Cancelled by user")
        sys.exit(0)
