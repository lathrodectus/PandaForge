#!/usr/bin/env python3
"""
Add Qidi Printer Compatibility to Generic/Esun/Sunlu Filaments

This tool updates existing Generic, Esun, and Sunlu filament profiles in BBL
to add Qidi printers to their compatible_printers list.
"""

import json
import sys
from pathlib import Path
from typing import List, Set


def get_qidi_printers(qidi_machine_dir: Path) -> List[str]:
    """Get list of all Qidi printer names"""
    printers = []

    for profile_file in qidi_machine_dir.glob("*.json"):
        try:
            with open(profile_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Only get instantiation profiles (actual printers, not base profiles)
                if data.get("instantiation") == "true":
                    printer_name = data.get("name")
                    if printer_name:
                        printers.append(printer_name)
        except Exception as e:
            print(f"Error reading {profile_file}: {e}")

    return sorted(printers)


def update_filament_profile(profile_path: Path, qidi_printers: List[str], dry_run: bool = False) -> bool:
    """Update a filament profile to add Qidi printers to compatible_printers"""
    try:
        with open(profile_path, 'r', encoding='utf-8') as f:
            profile = json.load(f)

        # Get current compatible printers
        compatible = profile.get("compatible_printers", [])
        if isinstance(compatible, str):
            compatible = [compatible]

        # Convert to set for easier manipulation
        compatible_set = set(compatible)
        original_count = len(compatible_set)

        # Add Qidi printers
        for printer in qidi_printers:
            compatible_set.add(printer)

        # Check if anything changed
        if len(compatible_set) == original_count:
            return False  # No changes needed

        # Update profile
        profile["compatible_printers"] = sorted(list(compatible_set))

        if not dry_run:
            # Write back
            with open(profile_path, 'w', encoding='utf-8') as f:
                json.dump(profile, f, indent=4, ensure_ascii=False)

        return True  # Changes made

    except Exception as e:
        print(f"Error updating {profile_path}: {e}")
        return False


def main():
    # Paths
    project_root = Path(__file__).parent.parent.parent
    qidi_machine_dir = project_root / "BambuStudio-2.5.0.66" / "resources" / "profiles" / "Qidi" / "machine"
    bbl_filament_dir = project_root / "BambuStudio-2.5.0.66" / "resources" / "profiles" / "BBL" / "filament"

    print("="*70)
    print("Add Qidi Compatibility to Generic/Esun/Sunlu Filaments")
    print("="*70)
    print()

    # Check paths exist
    if not qidi_machine_dir.exists():
        print(f"❌ Error: Qidi machine directory not found: {qidi_machine_dir}")
        sys.exit(1)

    if not bbl_filament_dir.exists():
        print(f"❌ Error: BBL filament directory not found: {bbl_filament_dir}")
        sys.exit(1)

    # Get Qidi printers
    print("Scanning Qidi printers...")
    qidi_printers = get_qidi_printers(qidi_machine_dir)
    print(f"✓ Found {len(qidi_printers)} Qidi printers")
    print()

    # Find Generic, Esun, Sunlu filaments
    print("Scanning BBL filaments...")
    target_patterns = ["Generic", "eSUN", "Sunlu"]
    filament_files = []

    for pattern in target_patterns:
        files = list(bbl_filament_dir.glob(f"{pattern}*.json"))
        filament_files.extend(files)

    print(f"✓ Found {len(filament_files)} filament profiles to update")
    print()

    # Ask for confirmation
    print("This will add the following Qidi printers to compatible_printers:")
    for i, printer in enumerate(qidi_printers, 1):
        print(f"  {i:2d}. {printer}")
    print()

    response = input("Proceed? (y/n): ").strip().lower()
    if response != 'y':
        print("Cancelled.")
        sys.exit(0)

    # Update filaments
    print()
    print("="*70)
    print("Updating Filament Profiles")
    print("="*70)
    print()

    updated_count = 0
    skipped_count = 0

    for filament_file in sorted(filament_files):
        changed = update_filament_profile(filament_file, qidi_printers, dry_run=False)

        if changed:
            print(f"✓ Updated: {filament_file.name}")
            updated_count += 1
        else:
            print(f"⊘ Skipped: {filament_file.name} (already compatible)")
            skipped_count += 1

    print()
    print("="*70)
    print("Summary")
    print("="*70)
    print(f"Updated: {updated_count} profiles")
    print(f"Skipped: {skipped_count} profiles (already compatible)")
    print(f"Total:   {len(filament_files)} profiles")
    print()
    print("✅ Done!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled by user")
        sys.exit(0)
