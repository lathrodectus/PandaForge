#!/usr/bin/env python3
"""Validate vendor bundles against the strict first-run loader rules.

This script is intentionally static: it checks the resource bundles under
`resources/profiles/` for the same classes of failures that break the Config
Wizard on a clean config folder, without changing runtime behavior.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
PRINT_CONFIG_CPP = PROJECT_ROOT / "src" / "libslic3r" / "PrintConfig.cpp"

VENDOR_LIST_KEYS = (
    "machine_model_list",
    "process_list",
    "filament_list",
    "machine_list",
)

SKIPPED_MANIFEST_STEMS = {
    "Custom",
    "TestF5T",
}

ENUM_ADD_RE = re.compile(r'def = this->add\("([^"]+)",\s*(coEnum|coEnums)\);')
ENUM_VALUE_RE = re.compile(r'def->enum_values\.push_back\("([^"]*)"\);')
ENUM_MAP_RE = re.compile(r's_keys_map_(\w+)\s*(?:=)?\s*\{')
ENUM_MAP_VALUE_RE = re.compile(r'\{\s*"([^"]+)"\s*,')
ENUM_TYPE_RE = re.compile(r'def->enum_keys_map = &ConfigOptionEnum<(\w+)>::get_enum_values\(\);')


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_static_enum_types(lines: list[str]) -> dict[str, set[str]]:
    enum_types: dict[str, set[str]] = {}
    current_type: str | None = None
    current_values: set[str] = set()

    for line in lines:
        map_match = ENUM_MAP_RE.search(line)
        if map_match:
            if current_type is not None:
                enum_types[current_type] = current_values
            current_type = map_match.group(1)
            current_values = set()
            continue

        if current_type is None:
            continue

        if line.strip() == "};":
            enum_types[current_type] = current_values
            current_type = None
            current_values = set()
            continue

        value_match = ENUM_MAP_VALUE_RE.search(line)
        if value_match:
            current_values.add(value_match.group(1))

    if current_type is not None:
        enum_types[current_type] = current_values

    return enum_types


def parse_enum_options() -> dict[str, set[str]]:
    lines = PRINT_CONFIG_CPP.read_text(encoding="utf-8").splitlines()
    enum_types = parse_static_enum_types(lines)

    enum_options: dict[str, set[str]] = {}
    current_key: str | None = None
    current_values: set[str] = set()

    for line in lines:
        add_match = ENUM_ADD_RE.search(line)
        if add_match:
            if current_key is not None:
                enum_options[current_key] = current_values
            current_key = add_match.group(1)
            current_values = set()
            continue

        if current_key is None:
            continue

        type_match = ENUM_TYPE_RE.search(line)
        if type_match:
            current_values.update(enum_types.get(type_match.group(1), set()))
            continue

        enum_value_match = ENUM_VALUE_RE.search(line)
        if enum_value_match:
            current_values.add(enum_value_match.group(1))

    if current_key is not None:
        enum_options[current_key] = current_values

    return enum_options


def normalize_legacy_key_value(key: str, value: Any) -> tuple[str, Any]:
    def normalize_string(item: str) -> str:
        if key == "support_type":
            if item == "normal":
                return "normal(auto)"
            if item == "tree":
                return "tree(manual)"
            if item == "hybrid(auto)":
                return "tree(auto)"
        elif key == "support_base_pattern" and item == "none":
            return "hollow"
        elif key == "extruder_type" and item == "DirectDrive":
            return "Direct Drive"
        elif key == "ensure_vertical_shell_thickness":
            if item == "1":
                return "enabled"
            if item == "0":
                return "partial"
        elif key == "filament_map_mode" and item == "Auto":
            return "Auto For Flush"
        elif key in {
            "nozzle_volume_type",
            "default_nozzle_volume_type",
            "printer_extruder_variant",
            "print_extruder_variant",
            "filament_extruder_variant",
            "extruder_variant_list",
        }:
            return item.replace("Normal", "Standard").replace("Big Traffic", "High Flow")
        return item

    if key == "infill_anchor":
        key = "sparse_infill_anchor"
    elif key == "infill_anchor_max":
        key = "sparse_infill_anchor_max"
    elif key == "wall_infill_order":
        key = "wall_sequence"
        if value == "inner wall/outer wall/infill" or value == "infill/inner wall/outer wall":
            value = "inner wall/outer wall"
        elif value == "outer wall/inner wall/infill" or value == "infill/outer wall/inner wall":
            value = "outer wall/inner wall"
        elif value == "inner-outer-inner wall/infill":
            value = "inner-outer-inner wall"

    if isinstance(value, str):
        return key, normalize_string(value)
    if isinstance(value, list):
        normalized_list = [normalize_string(item) if isinstance(item, str) else item for item in value]
        return key, normalized_list
    return key, value


def validate_enum_value(
    path: Path,
    raw_key: str,
    raw_value: Any,
    enum_options: dict[str, set[str]],
    errors: list[str],
) -> None:
    key, value = normalize_legacy_key_value(raw_key, raw_value)
    if key not in enum_options:
        return

    allowed = enum_options[key]
    if not allowed:
        return

    if isinstance(value, str):
        if value and value not in allowed:
            errors.append(
                f"{path}: invalid enum value for {raw_key}: {raw_value!r} "
                f"(normalized as {key}={value!r}, allowed: {sorted(allowed)})"
            )
        return

    if isinstance(value, list):
        for item in value:
            if not isinstance(item, str):
                errors.append(f"{path}: non-string enum list item for {raw_key}: {item!r}")
                continue
            if item and item not in allowed:
                errors.append(
                    f"{path}: invalid enum list value for {raw_key}: {item!r} "
                    f"(normalized key {key}, allowed: {sorted(allowed)})"
                )
        return

    errors.append(f"{path}: unsupported enum payload for {raw_key}: {type(value).__name__}")


def parse_variants(nozzle_value: str | None) -> set[str]:
    if not nozzle_value:
        return set()
    return {item.strip() for item in nozzle_value.split(";") if item.strip()}


def parse_includes(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value] if value else []
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str) and item]
    return []


def validate_collection(
    manifest_path: Path,
    vendor_dir: Path,
    list_name: str,
    items: list[dict[str, Any]],
    enum_options: dict[str, set[str]],
    model_variants: dict[str, set[str]],
    errors: list[str],
) -> None:
    loaded_names: set[str] = set()
    loaded_effective: dict[str, dict[str, Any]] = {}

    for item in items:
        manifest_name = item.get("name")
        sub_path = item.get("sub_path")

        if not manifest_name or not sub_path:
            errors.append(f"{manifest_path}: malformed {list_name} entry: {item!r}")
            continue

        preset_path = vendor_dir / sub_path
        if not preset_path.exists():
            errors.append(f"{manifest_path}: missing {list_name} sub_path target {preset_path}")
            continue

        try:
            preset = load_json(preset_path)
        except json.JSONDecodeError as exc:
            errors.append(f"{preset_path}: invalid JSON ({exc})")
            continue

        preset_name = preset.get("name") or manifest_name
        if preset_name in loaded_names:
            errors.append(f"{preset_path}: duplicate loaded preset name {preset_name!r} in {list_name}")

        inherits = preset.get("inherits")
        if inherits and inherits not in loaded_names:
            errors.append(f"{preset_path}: parent {inherits!r} loads after child or is missing from {list_name}")

        effective: dict[str, Any] = {}
        if inherits in loaded_effective:
            effective = copy.deepcopy(loaded_effective[inherits])

        for include in parse_includes(preset.get("includes")):
            if include not in loaded_names:
                errors.append(f"{preset_path}: include {include!r} loads after child or is missing from {list_name}")
            elif include in loaded_effective:
                effective.update(copy.deepcopy(loaded_effective[include]))

        effective.update(copy.deepcopy(preset))

        if list_name == "machine_list" and preset.get("instantiation") != "false":
            printer_model = effective.get("printer_model")
            printer_variant = effective.get("printer_variant")
            if not printer_model:
                errors.append(f"{preset_path}: missing printer_model")
            elif printer_model not in model_variants:
                errors.append(f"{preset_path}: printer_model {printer_model!r} not found in machine_model_list")

            if not printer_variant:
                errors.append(f"{preset_path}: missing printer_variant")
            elif printer_model in model_variants and printer_variant not in model_variants[printer_model]:
                errors.append(
                    f"{preset_path}: printer_variant {printer_variant!r} not present in {printer_model!r} nozzle_diameter"
                )

        if list_name == "filament_list" and preset.get("instantiation") != "false":
            filament_id = effective.get("filament_id")
            if not filament_id:
                errors.append(f"{preset_path}: visible system filament missing filament_id")

        for key, value in preset.items():
            validate_enum_value(preset_path, key, value, enum_options, errors)

        loaded_names.add(preset_name)
        loaded_effective[preset_name] = effective


def validate_vendor_manifest(manifest_path: Path, enum_options: dict[str, set[str]]) -> list[str]:
    errors: list[str] = []

    try:
        manifest = load_json(manifest_path)
    except json.JSONDecodeError as exc:
        return [f"{manifest_path}: invalid JSON ({exc})"]

    if not all(key in manifest for key in VENDOR_LIST_KEYS):
        return []

    vendor_dir = SCRIPT_DIR / manifest_path.stem
    if not vendor_dir.exists():
        errors.append(f"{manifest_path}: vendor directory {vendor_dir} is missing")
        return errors

    model_variants: dict[str, set[str]] = {}
    for item in manifest["machine_model_list"]:
        manifest_name = item.get("name")
        sub_path = item.get("sub_path")
        if not manifest_name or not sub_path:
            errors.append(f"{manifest_path}: malformed machine_model_list entry: {item!r}")
            continue

        model_path = vendor_dir / sub_path
        if not model_path.exists():
            errors.append(f"{manifest_path}: missing machine_model_list sub_path target {model_path}")
            continue

        try:
            model_json = load_json(model_path)
        except json.JSONDecodeError as exc:
            errors.append(f"{model_path}: invalid JSON ({exc})")
            continue

        model_name = model_json.get("name") or manifest_name
        if model_name in model_variants:
            errors.append(f"{model_path}: duplicate loaded machine model name {model_name!r}")
        model_variants[model_name] = parse_variants(model_json.get("nozzle_diameter"))

        for key, value in model_json.items():
            validate_enum_value(model_path, key, value, enum_options, errors)

    for list_name in ("process_list", "filament_list", "machine_list"):
        validate_collection(
            manifest_path,
            vendor_dir,
            list_name,
            manifest.get(list_name, []),
            enum_options,
            model_variants,
            errors,
        )

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate resource vendor bundles against strict first-run loader rules."
    )
    parser.add_argument(
        "vendors",
        nargs="*",
        help="Optional vendor manifest stems to validate, for example: Anycubic Flashforge",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    enum_options = parse_enum_options()

    manifests = sorted(SCRIPT_DIR.glob("*.json"))
    if args.vendors:
        requested = {name.lower() for name in args.vendors}
        manifests = [path for path in manifests if path.stem.lower() in requested]
    else:
        manifests = [path for path in manifests if path.stem not in SKIPPED_MANIFEST_STEMS]

    checked = 0
    errors: list[str] = []
    for manifest_path in manifests:
        vendor_errors = validate_vendor_manifest(manifest_path, enum_options)
        if not vendor_errors:
            manifest_json = load_json(manifest_path)
            if not all(key in manifest_json for key in VENDOR_LIST_KEYS):
                continue
        checked += 1
        errors.extend(vendor_errors)

    if checked == 0:
        print("No vendor manifests matched the requested scope.")
        return 1

    if errors:
        print(f"Strict vendor bundle validation failed for {checked} manifest(s):")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Strict vendor bundle validation passed for {checked} manifest(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
