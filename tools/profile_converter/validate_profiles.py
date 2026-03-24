#!/usr/bin/env python3
"""
Profile Validator for Pandaforge

Validates converted profiles to ensure they meet Pandaforge requirements.
Checks for required fields, Klipper settings, and profile consistency.

Usage:
    python3 validate_profiles.py <profile_dir>

Example:
    python3 validate_profiles.py ~/Pandaforge/BambuStudio-2.5.0.66/resources/profiles/Creality
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class ProfileValidator:
    """Validates Pandaforge profiles"""

    def __init__(self, profile_dir: Path):
        self.profile_dir = Path(profile_dir)
        self.errors = []
        self.warnings = []
        self.info = []

    def validate_all(self) -> bool:
        """Validate all profiles in directory"""
        print(f"Validating profiles in: {self.profile_dir}")
        print("=" * 70)

        # Validate vendor JSON
        vendor_json = self.find_vendor_json()
        if vendor_json:
            self.validate_vendor_json(vendor_json)
        else:
            self.errors.append("No vendor JSON file found")

        # Validate machine profiles
        machine_dir = self.profile_dir / "machine"
        if machine_dir.exists():
            print("\n=== Validating Machine Profiles ===")
            for profile_file in machine_dir.glob("*.json"):
                self.validate_machine_profile(profile_file)

        # Validate filament profiles
        filament_dir = self.profile_dir / "filament"
        if filament_dir.exists():
            print("\n=== Validating Filament Profiles ===")
            for profile_file in filament_dir.glob("*.json"):
                self.validate_filament_profile(profile_file)

        # Validate process profiles
        process_dir = self.profile_dir / "process"
        if process_dir.exists():
            print("\n=== Validating Process Profiles ===")
            for profile_file in process_dir.glob("*.json"):
                self.validate_process_profile(profile_file)

        # Print summary
        self.print_summary()

        return len(self.errors) == 0

    def find_vendor_json(self) -> Path:
        """Find vendor JSON file"""
        for json_file in self.profile_dir.glob("*.json"):
            if json_file.stem != "blacklist":
                return json_file
        return None

    def validate_vendor_json(self, vendor_json: Path):
        """Validate vendor JSON manifest"""
        print(f"\n=== Validating Vendor JSON: {vendor_json.name} ===")
        try:
            with open(vendor_json, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Check required fields
            required = ["name", "version", "machine_model_list", "machine_list",
                       "filament_list", "process_list"]
            for field in required:
                if field not in data:
                    self.errors.append(f"Vendor JSON missing required field: {field}")
                else:
                    print(f"  ✓ {field}: {len(data[field]) if isinstance(data[field], list) else 'present'}")

            # Check version format
            if "version" in data:
                version = data["version"]
                if not version.startswith("02.05.00"):
                    self.warnings.append(f"Version {version} may not match Pandaforge 2.5.0.66")

        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in {vendor_json.name}: {e}")
        except Exception as e:
            self.errors.append(f"Error reading {vendor_json.name}: {e}")

    def validate_machine_profile(self, profile_path: Path):
        """Validate machine profile"""
        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                profile = json.load(f)

            name = profile.get("name", profile_path.stem)
            is_instantiation = profile.get("instantiation") == "true"

            if not is_instantiation:
                print(f"  ⊘ Skipping base profile: {name}")
                return

            print(f"  → Validating: {name}")

            # Check required fields
            required = ["type", "name", "from"]
            for field in required:
                if field not in profile:
                    self.errors.append(f"{name}: Missing required field '{field}'")

            # Check type
            if profile.get("type") != "machine":
                self.errors.append(f"{name}: Invalid type '{profile.get('type')}', expected 'machine'")

            # Check Klipper-specific settings
            gcode_flavor = profile.get("gcode_flavor")
            if gcode_flavor == "klipper":
                print(f"    ✓ Klipper printer detected")

                # Check for Klipper kinematics
                klipper_fields = [
                    "machine_max_acceleration_x",
                    "machine_max_acceleration_y",
                    "machine_max_speed_x",
                    "machine_max_speed_y"
                ]
                missing_klipper = [f for f in klipper_fields if f not in profile]
                if missing_klipper:
                    self.warnings.append(f"{name}: Missing Klipper fields: {', '.join(missing_klipper)}")

                # Check for start/end gcode
                if "machine_start_gcode" not in profile:
                    self.warnings.append(f"{name}: Missing machine_start_gcode")
                if "machine_end_gcode" not in profile:
                    self.warnings.append(f"{name}: Missing machine_end_gcode")

            elif gcode_flavor:
                self.info.append(f"{name}: Non-Klipper printer (flavor: {gcode_flavor})")

            # Check build volume
            if "printable_area" not in profile:
                self.warnings.append(f"{name}: Missing printable_area")
            if "printable_height" not in profile:
                self.warnings.append(f"{name}: Missing printable_height")

            # Check nozzle diameter
            if "nozzle_diameter" not in profile:
                self.warnings.append(f"{name}: Missing nozzle_diameter")

            print(f"    ✓ Validation passed")

        except json.JSONDecodeError as e:
            self.errors.append(f"{profile_path.name}: Invalid JSON - {e}")
        except Exception as e:
            self.errors.append(f"{profile_path.name}: Validation error - {e}")

    def validate_filament_profile(self, profile_path: Path):
        """Validate filament profile"""
        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                profile = json.load(f)

            name = profile.get("name", profile_path.stem)
            is_instantiation = profile.get("instantiation") == "true"

            if not is_instantiation:
                print(f"  ⊘ Skipping base profile: {name}")
                return

            print(f"  → Validating: {name}")

            # Check required fields
            required = ["type", "name", "from"]
            for field in required:
                if field not in profile:
                    self.errors.append(f"{name}: Missing required field '{field}'")

            # Check type
            if profile.get("type") != "filament":
                self.errors.append(f"{name}: Invalid type '{profile.get('type')}', expected 'filament'")

            # Check temperatures
            if "nozzle_temperature" not in profile:
                self.warnings.append(f"{name}: Missing nozzle_temperature")
            if "hot_plate_temp" not in profile and "bed_temperature" not in profile:
                self.warnings.append(f"{name}: Missing hot_plate_temp/bed_temperature")

            # Check pressure advance for Klipper
            if "enable_pressure_advance" in profile:
                pa_enabled = profile["enable_pressure_advance"]
                if pa_enabled == ["1"] or pa_enabled == "1":
                    print(f"    ✓ Pressure advance enabled")
                    if "pressure_advance" not in profile:
                        self.warnings.append(f"{name}: Pressure advance enabled but no value set")
                    else:
                        pa_value = profile["pressure_advance"]
                        if isinstance(pa_value, list):
                            pa_value = pa_value[0]
                        try:
                            pa_float = float(pa_value)
                            if pa_float < 0 or pa_float > 0.2:
                                self.warnings.append(f"{name}: Unusual pressure advance value: {pa_float}")
                        except ValueError:
                            self.errors.append(f"{name}: Invalid pressure advance value: {pa_value}")

            # Check compatible printers
            if "compatible_printers" not in profile:
                self.warnings.append(f"{name}: Missing compatible_printers list")

            print(f"    ✓ Validation passed")

        except json.JSONDecodeError as e:
            self.errors.append(f"{profile_path.name}: Invalid JSON - {e}")
        except Exception as e:
            self.errors.append(f"{profile_path.name}: Validation error - {e}")

    def validate_process_profile(self, profile_path: Path):
        """Validate process profile"""
        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                profile = json.load(f)

            name = profile.get("name", profile_path.stem)
            is_instantiation = profile.get("instantiation") == "true"

            if not is_instantiation:
                print(f"  ⊘ Skipping base profile: {name}")
                return

            print(f"  → Validating: {name}")

            # Check required fields
            required = ["type", "name", "from"]
            for field in required:
                if field not in profile:
                    self.errors.append(f"{name}: Missing required field '{field}'")

            # Check type
            if profile.get("type") != "process":
                self.errors.append(f"{name}: Invalid type '{profile.get('type')}', expected 'process'")

            # Check layer height
            if "layer_height" not in profile:
                self.warnings.append(f"{name}: Missing layer_height")

            # Check speeds
            speed_fields = ["outer_wall_speed", "inner_wall_speed", "sparse_infill_speed"]
            missing_speeds = [f for f in speed_fields if f not in profile]
            if missing_speeds:
                self.warnings.append(f"{name}: Missing speed settings: {', '.join(missing_speeds)}")

            # Check compatible printers
            if "compatible_printers" not in profile:
                self.warnings.append(f"{name}: Missing compatible_printers list")

            print(f"    ✓ Validation passed")

        except json.JSONDecodeError as e:
            self.errors.append(f"{profile_path.name}: Invalid JSON - {e}")
        except Exception as e:
            self.errors.append(f"{profile_path.name}: Validation error - {e}")

    def print_summary(self):
        """Print validation summary"""
        print("\n" + "=" * 70)
        print("VALIDATION SUMMARY")
        print("=" * 70)

        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  • {error}")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  • {warning}")

        if self.info:
            print(f"\nℹ️  INFO ({len(self.info)}):")
            for info in self.info:
                print(f"  • {info}")

        print("\n" + "=" * 70)
        if not self.errors:
            print("✅ VALIDATION PASSED")
        else:
            print("❌ VALIDATION FAILED")
        print("=" * 70)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_profiles.py <profile_dir>")
        print("\nExample:")
        print("  python3 validate_profiles.py ~/Pandaforge/resources/profiles/Creality")
        sys.exit(1)

    profile_dir = Path(sys.argv[1])
    if not profile_dir.exists():
        print(f"❌ Error: Directory not found: {profile_dir}")
        sys.exit(1)

    validator = ProfileValidator(profile_dir)
    success = validator.validate_all()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
