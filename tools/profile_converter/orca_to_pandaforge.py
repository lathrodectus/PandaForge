#!/usr/bin/env python3
"""
OrcaSlicer to Pandaforge Profile Converter

Converts Klipper printer profiles from OrcaSlicer format to Pandaforge (BambuStudio) format.
Handles machine profiles, filament profiles, and process profiles with proper inheritance chains.

Usage:
    python3 orca_to_pandaforge.py <orca_profile_dir> <output_dir> [options]

Example:
    python3 orca_to_pandaforge.py \
        ~/OrcaSlicer/resources/profiles/Creality \
        ~/Pandaforge/BambuStudio-2.5.0.66/resources/profiles/Creality \
        --vendor "Creality" \
        --printer "K1 Max"
"""

import json
import os
import sys
import argparse
import shutil
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class ProfileConverter:
    """Converts OrcaSlicer profiles to Pandaforge format"""

    # Field mappings from OrcaSlicer to Pandaforge
    FIELD_MAPPINGS = {
        # Machine settings
        "bed_temperature": "hot_plate_temp",
        "bed_temperature_initial_layer": "hot_plate_temp_initial_layer",

        # Filament settings (most are compatible)
        "filament_type": "filament_type",
        "filament_colour": "filament_colour",

        # Process settings
        "layer_height": "layer_height",
        "first_layer_height": "initial_layer_height",
        "perimeters": "wall_loops",
        "top_solid_layers": "top_shell_layers",
        "bottom_solid_layers": "bottom_shell_layers",
    }

    # Settings that need special handling for Klipper
    KLIPPER_SPECIFIC = [
        "enable_pressure_advance",
        "pressure_advance",
        "gcode_flavor",
        "machine_max_acceleration_x",
        "machine_max_acceleration_y",
        "machine_max_jerk_x",
        "machine_max_jerk_y",
    ]

    def __init__(self, orca_dir: Path, output_dir: Path, vendor: str):
        self.orca_dir = Path(orca_dir)
        self.output_dir = Path(output_dir)
        self.vendor = vendor
        self.converted_profiles = {
            "machine": [],
            "filament": [],
            "process": []
        }
        self.converted_machine_models = []

    def convert_all(self):
        """Convert all profiles in the OrcaSlicer directory"""
        print(f"Converting profiles from {self.orca_dir} to {self.output_dir}")
        print(f"Vendor: {self.vendor}")

        # Create output directory structure
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "machine").mkdir(exist_ok=True)
        (self.output_dir / "filament").mkdir(exist_ok=True)
        (self.output_dir / "process").mkdir(exist_ok=True)

        # Convert machine profiles
        machine_dir = self.orca_dir / "machine"
        if machine_dir.exists():
            print("\n=== Converting Machine Profiles ===")
            for profile_file in machine_dir.glob("*.json"):
                self.convert_machine_profile(profile_file)

        # Convert filament profiles
        filament_dir = self.orca_dir / "filament"
        if filament_dir.exists():
            print("\n=== Converting Filament Profiles ===")
            for profile_file in filament_dir.glob("*.json"):
                self.convert_filament_profile(profile_file)

        # Convert process profiles
        process_dir = self.orca_dir / "process"
        if process_dir.exists():
            print("\n=== Converting Process Profiles ===")
            for profile_file in process_dir.glob("*.json"):
                self.convert_process_profile(profile_file)

        # Generate vendor JSON
        self.generate_vendor_json()

        # Copy assets (images, models)
        self.copy_assets()

        print(f"\n✅ Conversion complete!")
        print(f"   Machines: {len(self.converted_profiles['machine'])}")
        print(f"   Filaments: {len(self.converted_profiles['filament'])}")
        print(f"   Processes: {len(self.converted_profiles['process'])}")

    def convert_machine_profile(self, profile_path: Path):
        """Convert a machine profile"""
        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                orca_profile = json.load(f)

            # Check profile type
            is_machine_model = orca_profile.get("type") == "machine_model"
            is_instantiation = orca_profile.get("instantiation", "false") == "true"
            is_base_profile = not is_instantiation and not is_machine_model

            # Convert ALL profiles: machine_model, instantiation, and base profiles
            # Base profiles are needed for inheritance chain
            print(f"  → Converting: {profile_path.name}")

            # Create Pandaforge profile
            if is_machine_model:
                # For machine_model files, copy all fields as-is
                panda_profile = orca_profile.copy()
                print(f"    ✓ Machine model (base)")
            elif is_base_profile:
                # For base profiles (inheritance chain), copy all fields as-is
                panda_profile = orca_profile.copy()
                print(f"    ✓ Base profile (inheritance)")
            else:
                # For machine (nozzle variant) files, convert normally
                panda_profile = {
                    "type": "machine",
                    "name": orca_profile.get("name"),
                    "inherits": self.convert_inherits(orca_profile.get("inherits", "")),
                    "from": "system",
                    "setting_id": orca_profile.get("setting_id", self.generate_setting_id("machine")),
                    "instantiation": "true",
                }

                # Copy printer model reference
                if "printer_model" in orca_profile:
                    panda_profile["printer_model"] = orca_profile["printer_model"]

                # Copy essential machine settings
                machine_fields = [
                    "gcode_flavor", "nozzle_diameter", "printer_variant",
                    "printable_area", "printable_height", "nozzle_type",
                    "auxiliary_fan", "support_air_filtration", "support_multi_bed_types",
                    "default_print_profile", "default_filament_profile",
                    "machine_max_acceleration_e", "machine_max_acceleration_extruding",
                    "machine_max_acceleration_retracting", "machine_max_acceleration_travel",
                    "machine_max_acceleration_x", "machine_max_acceleration_y", "machine_max_acceleration_z",
                    "machine_max_speed_e", "machine_max_speed_x", "machine_max_speed_y", "machine_max_speed_z",
                    "machine_max_jerk_e", "machine_max_jerk_x", "machine_max_jerk_y", "machine_max_jerk_z",
                    "retraction_length", "retraction_speed", "deretraction_speed",
                    "retraction_minimum_travel", "retract_before_wipe", "z_hop",
                    "machine_start_gcode", "machine_end_gcode", "before_layer_change_gcode",
                    "layer_change_gcode", "change_filament_gcode", "machine_pause_gcode",
                    "max_layer_height", "min_layer_height",
                    "extruder_clearance_radius", "extruder_clearance_height_to_rod", "extruder_clearance_height_to_lid",
                    "thumbnails", "use_relative_e_distances", "wipe_distance",
                    "printer_settings_id", "scan_first_layer", "bed_exclude_area"
                ]

                for field in machine_fields:
                    if field in orca_profile:
                        panda_profile[field] = orca_profile[field]

                # Ensure printer_model exists (required by BambuStudio)
                if "printer_model" not in panda_profile or not panda_profile["printer_model"]:
                    derived_model = self.derive_printer_model(panda_profile.get("name", ""))
                    if derived_model:
                        panda_profile["printer_model"] = derived_model

                # Ensure printer_variant exists (required by BambuStudio)
                if "printer_variant" not in panda_profile or not panda_profile["printer_variant"]:
                    derived_variant = self.derive_printer_variant(orca_profile, panda_profile.get("name", ""))
                    if derived_variant:
                        panda_profile["printer_variant"] = derived_variant

                # Ensure Klipper flavor is set
                if panda_profile.get("gcode_flavor") == "klipper":
                    print(f"    ✓ Klipper printer detected")

            # Write output
            output_path = self.output_dir / "machine" / profile_path.name
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(panda_profile, f, indent=4, ensure_ascii=False)

            if is_machine_model:
                self.converted_machine_models.append({
                    "name": panda_profile.get("name", ""),
                    "sub_path": f"machine/{profile_path.name}"
                })
            else:
                self.converted_profiles["machine"].append({
                    "name": panda_profile.get("name", ""),
                    "sub_path": f"machine/{profile_path.name}",
                    "instantiation": panda_profile.get("instantiation", "")
                })

            print(f"    ✓ Saved to: {output_path.name}")

        except Exception as e:
            print(f"    ✗ Error converting {profile_path.name}: {e}")

    def convert_filament_profile(self, profile_path: Path):
        """Convert a filament profile"""
        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                orca_profile = json.load(f)

            # Convert ALL profiles including base profiles for inheritance
            is_instantiation = orca_profile.get("instantiation", "false") == "true"
            is_base_profile = not is_instantiation

            print(f"  → Converting: {profile_path.name}")

            # Create Pandaforge profile
            if is_base_profile:
                # For base profiles, copy all fields as-is
                panda_profile = orca_profile.copy()
                print(f"    ✓ Base profile (inheritance)")
            else:
                # For instantiation profiles, convert normally
                panda_profile = {
                    "type": "filament",
                    "name": orca_profile.get("name"),
                    "inherits": self.convert_inherits(orca_profile.get("inherits", "")),
                    "from": "system",
                    "setting_id": orca_profile.get("setting_id", self.generate_setting_id("filament")),
                    "filament_id": orca_profile.get("filament_id", self.generate_filament_id()),
                    "instantiation": "true",
                }

                # Copy filament settings
                filament_fields = [
                    "filament_type", "filament_colour", "filament_diameter",
                    "filament_flow_ratio", "filament_max_volumetric_speed",
                    "nozzle_temperature", "nozzle_temperature_initial_layer",
                    "nozzle_temperature_range_low", "nozzle_temperature_range_high",
                    "hot_plate_temp", "hot_plate_temp_initial_layer",
                    "enable_pressure_advance", "pressure_advance",
                    "filament_retraction_length", "filament_retraction_speed",
                    "filament_deretraction_speed", "filament_retract_before_wipe",
                    "filament_wipe_distance", "filament_retraction_minimum_travel",
                    "slow_down_layer_time", "slow_down_min_speed",
                    "fan_min_speed", "fan_max_speed", "additional_cooling_fan_speed",
                    "support_material_interface_fan_speed",
                    "filament_start_gcode", "filament_end_gcode",
                    "compatible_printers", "compatible_prints"
                ]

                for field in filament_fields:
                    if field in orca_profile:
                        panda_profile[field] = orca_profile[field]

                # Handle bed temperature field mapping
                if "bed_temperature" in orca_profile and "hot_plate_temp" not in panda_profile:
                    panda_profile["hot_plate_temp"] = orca_profile["bed_temperature"]
                if "bed_temperature_initial_layer" in orca_profile and "hot_plate_temp_initial_layer" not in panda_profile:
                    panda_profile["hot_plate_temp_initial_layer"] = orca_profile["bed_temperature_initial_layer"]

                # Ensure pressure advance is enabled for Klipper
                if "enable_pressure_advance" not in panda_profile:
                    panda_profile["enable_pressure_advance"] = ["1"]
                if "pressure_advance" not in panda_profile:
                    panda_profile["pressure_advance"] = ["0.025"]  # Conservative default

            # Write output
            output_path = self.output_dir / "filament" / profile_path.name
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(panda_profile, f, indent=4, ensure_ascii=False)

            self.converted_profiles["filament"].append({
                "name": panda_profile.get("name", ""),
                "sub_path": f"filament/{profile_path.name}",
                "instantiation": panda_profile.get("instantiation", "")
            })

            print(f"    ✓ Saved to: {output_path.name}")

        except Exception as e:
            print(f"    ✗ Error converting {profile_path.name}: {e}")

    def convert_process_profile(self, profile_path: Path):
        """Convert a process (print) profile"""
        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                orca_profile = json.load(f)

            # Convert ALL profiles including base profiles for inheritance
            is_instantiation = orca_profile.get("instantiation", "false") == "true"
            is_base_profile = not is_instantiation

            print(f"  → Converting: {profile_path.name}")

            # Create Pandaforge profile
            if is_base_profile:
                # For base profiles, copy all fields as-is
                panda_profile = orca_profile.copy()
                print(f"    ✓ Base profile (inheritance)")
            else:
                # For instantiation profiles, convert normally
                panda_profile = {
                    "type": "process",
                    "name": orca_profile.get("name"),
                    "inherits": self.convert_inherits(orca_profile.get("inherits", "")),
                    "from": "system",
                    "setting_id": orca_profile.get("setting_id", self.generate_setting_id("process")),
                    "instantiation": "true",
                }

                # Copy description if present
                if "description" in orca_profile:
                    panda_profile["description"] = orca_profile["description"]

                # Copy process settings (extensive list)
                process_fields = [
                    "layer_height", "initial_layer_height", "line_width",
                    "outer_wall_line_width", "inner_wall_line_width",
                    "top_surface_line_width", "initial_layer_line_width",
                    "wall_loops", "top_shell_layers", "bottom_shell_layers",
                    "sparse_infill_density", "sparse_infill_pattern",
                    "outer_wall_speed", "inner_wall_speed", "sparse_infill_speed",
                    "internal_solid_infill_speed", "top_surface_speed",
                    "initial_layer_speed", "travel_speed", "bridge_speed",
                    "default_acceleration", "outer_wall_acceleration",
                    "inner_wall_acceleration", "top_surface_acceleration",
                    "travel_acceleration", "initial_layer_acceleration",
                    "support_speed", "support_interface_speed",
                    "enable_support", "support_type", "support_threshold_angle",
                    "support_on_build_plate_only", "support_top_z_distance",
                    "support_bottom_z_distance", "support_interface_spacing",
                    "tree_support_branch_angle", "tree_support_wall_count",
                    "brim_width", "brim_type", "skirt_loops", "skirt_distance",
                    "enable_prime_tower", "prime_tower_width",
                    "detect_overhang_wall", "overhang_1_4_speed", "overhang_2_4_speed",
                    "overhang_3_4_speed", "overhang_4_4_speed",
                    "seam_position", "seam_gap", "role_based_wipe_speed",
                    "wipe_on_loops", "wipe_speed",
                    "enable_arc_fitting", "arc_fitting_tolerance",
                    "filename_format", "compatible_printers"
                ]

                for field in process_fields:
                    if field in orca_profile:
                        panda_profile[field] = orca_profile[field]

            # Write output
            output_path = self.output_dir / "process" / profile_path.name
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(panda_profile, f, indent=4, ensure_ascii=False)

            self.converted_profiles["process"].append({
                "name": panda_profile.get("name", ""),
                "sub_path": f"process/{profile_path.name}",
                "instantiation": panda_profile.get("instantiation", "")
            })

            print(f"    ✓ Saved to: {output_path.name}")

        except Exception as e:
            print(f"    ✗ Error converting {profile_path.name}: {e}")

    def convert_inherits(self, inherits: str) -> str:
        """Convert inheritance chain, adapting to Pandaforge naming"""
        if not inherits:
            return ""

        # Map common base profiles
        mappings = {
            "fdm_creality_common": "fdm_klipper_common",
            "fdm_voron_common": "fdm_klipper_common",
        }

        return mappings.get(inherits, inherits)

    def generate_setting_id(self, profile_type: str) -> str:
        """Generate a unique setting ID"""
        import random
        prefix_map = {
            "machine": "GM",
            "filament": "GF",
            "process": "GP"
        }
        prefix = prefix_map.get(profile_type, "GX")
        return f"{prefix}{random.randint(1000, 9999)}"

    def generate_filament_id(self) -> str:
        """Generate a unique filament ID"""
        import random
        return f"GFL{random.randint(100, 999)}"

    def generate_vendor_json(self):
        """Generate the vendor.json file"""
        print("\n=== Generating Vendor JSON ===")

        # Machine models should ONLY include type=machine_model files
        machine_models = sorted(
            [{"name": m["name"], "sub_path": m["sub_path"]} for m in self.converted_machine_models],
            key=lambda x: x["name"].lower()
        )

        def sort_profiles(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
            # Load base profiles first to satisfy inheritance chains
            def sort_key(item: Dict[str, Any]) -> tuple:
                inst = item.get("instantiation", "")
                is_instantiation = (inst == "true")
                return (is_instantiation, item.get("name", "").lower())
            sorted_items = sorted(items, key=sort_key)
            return [{"name": i["name"], "sub_path": i["sub_path"]} for i in sorted_items]

        vendor_json = {
            "name": self.vendor,
            "version": "02.05.00.66",
            "force_update": "0",
            "description": f"{self.vendor} configurations for Klipper printers",
            "machine_model_list": machine_models,
            "process_list": sort_profiles(self.converted_profiles["process"]),
            "filament_list": sort_profiles(self.converted_profiles["filament"]),
            "machine_list": sort_profiles(self.converted_profiles["machine"])
        }

        # Write vendor JSON to parent directory (profiles root), not inside brand directory
        output_path = self.output_dir.parent / f"{self.vendor}.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(vendor_json, f, indent=4, ensure_ascii=False)

        print(f"  ✓ Generated: {output_path.name} (in profiles root)")

    def copy_assets(self):
        """Copy image assets and 3D models"""
        print("\n=== Copying Assets ===")

        # Copy cover images
        for img_file in self.orca_dir.glob("*_cover.png"):
            dest = self.output_dir / img_file.name
            shutil.copy2(img_file, dest)
            print(f"  ✓ Copied: {img_file.name}")

        # Copy buildplate textures and models
        for asset_file in self.orca_dir.glob("*buildplate*"):
            if asset_file.suffix in ['.png', '.stl', '.STL']:
                dest = self.output_dir / asset_file.name
                shutil.copy2(asset_file, dest)
                print(f"  ✓ Copied: {asset_file.name}")

        # Copy hotend models
        for asset_file in self.orca_dir.glob("*hotend*"):
            if asset_file.suffix in ['.stl', '.STL']:
                dest = self.output_dir / asset_file.name
                shutil.copy2(asset_file, dest)
                print(f"  ✓ Copied: {asset_file.name}")

    def derive_printer_variant(self, orca_profile: Dict[str, Any], name: str) -> Optional[str]:
        nozzle = orca_profile.get("nozzle_diameter")
        if isinstance(nozzle, list) and nozzle:
            return str(nozzle[0])
        if isinstance(nozzle, str) and nozzle:
            return nozzle.split(";")[0] if ";" in nozzle else nozzle
        match = re.search(r"(\d+(?:\.\d+)?)\s*(?:mm\s*)?nozzle$", name, re.IGNORECASE)
        if match:
            return match.group(1)
        return None

    def derive_printer_model(self, name: str) -> str:
        if not name:
            return ""
        # Strip trailing nozzle/variant suffixes (e.g., " 0.4 nozzle", " 0.4 Nozzle", " 0.4mm nozzle")
        model = re.sub(r"\s+\d+(?:\.\d+)?\s*(?:mm\s*)?nozzle$", "", name, flags=re.IGNORECASE)
        return model.strip()


def main():
    parser = argparse.ArgumentParser(
        description="Convert OrcaSlicer Klipper profiles to Pandaforge format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert Creality K1 profiles
  python3 orca_to_pandaforge.py \\
      ~/OrcaSlicer/resources/profiles/Creality \\
      ~/Pandaforge/resources/profiles/Creality \\
      --vendor "Creality"

  # Convert Voron profiles
  python3 orca_to_pandaforge.py \\
      ~/OrcaSlicer/resources/profiles/Voron \\
      ~/Pandaforge/resources/profiles/Voron \\
      --vendor "Voron"
        """
    )

    parser.add_argument(
        "orca_dir",
        type=str,
        help="Path to OrcaSlicer profile directory (e.g., OrcaSlicer/resources/profiles/Creality)"
    )

    parser.add_argument(
        "output_dir",
        type=str,
        help="Output directory for Pandaforge profiles"
    )

    parser.add_argument(
        "--vendor",
        type=str,
        required=True,
        help="Vendor name (e.g., 'Creality', 'Voron', 'Prusa')"
    )

    args = parser.parse_args()

    # Validate paths
    orca_dir = Path(args.orca_dir)
    if not orca_dir.exists():
        print(f"❌ Error: OrcaSlicer directory not found: {orca_dir}")
        sys.exit(1)

    output_dir = Path(args.output_dir)

    # Run conversion
    print("=" * 70)
    print("OrcaSlicer to Pandaforge Profile Converter")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    converter = ProfileConverter(orca_dir, output_dir, args.vendor)
    converter.convert_all()

    print("\n" + "=" * 70)
    print("Conversion Summary")
    print("=" * 70)
    print(f"Output directory: {output_dir}")
    print(f"Vendor JSON: {output_dir / args.vendor}.json")
    print("\nNext steps:")
    print("1. Review converted profiles for accuracy")
    print("2. Test with actual printer hardware")
    print("3. Adjust pressure advance values if needed")
    print("4. Update machine start/end G-code for your setup")
    print()


if __name__ == "__main__":
    main()
