#!/usr/bin/env python3
"""
Pandaforge Profile Converter GUI - Internal Tool

For internal use only. Converts OrcaSlicer profiles from the project to Pandaforge format.
- Uses OrcaSlicer profiles already in the project
- Select brands and specific printers to convert
- No external path configuration needed
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import threading
from pathlib import Path
from typing import Dict, List, Set, Tuple
import sys
import os

# Import the converter
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
                print(f"Error reading {profile_file}: {e}")

        self.models.sort(key=lambda x: x.name)

    @property
    def klipper_count(self):
        return sum(1 for m in self.models if m.is_klipper)


class ProfileConverterGUI:
    """Main GUI application for internal use"""

    def __init__(self, root):
        self.root = root
        self.root.title("Pandaforge Profile Converter - Internal Tool")
        self.root.geometry("1000x750")

        # Fixed paths (internal use)
        self.project_root = Path(__file__).parent.parent.parent
        self.orca_profiles_dir = self.project_root / "OrcaSlicer-main" / "resources" / "profiles"
        self.output_dir = self.project_root / "BambuStudio-2.5.0.66" / "resources" / "profiles"

        # State
        self.brands: Dict[str, PrinterBrand] = {}
        self.selected_items: Set[Tuple[str, str]] = set()  # (brand_name, model_name) or (brand_name, None) for whole brand

        # Setup UI
        self._create_widgets()

        # Auto-scan on startup
        self.root.after(100, self._scan_printers)

    def _create_widgets(self):
        """Create all UI widgets"""

        # Header
        header_frame = ttk.Frame(self.root, padding="10")
        header_frame.pack(fill=tk.X)

        title_label = ttk.Label(
            header_frame,
            text="Pandaforge Profile Converter",
            font=("Helvetica", 16, "bold")
        )
        title_label.pack()

        subtitle_label = ttk.Label(
            header_frame,
            text="Internal Tool - Convert OrcaSlicer profiles to Pandaforge format",
            font=("Helvetica", 10)
        )
        subtitle_label.pack()

        # Info frame
        info_frame = ttk.LabelFrame(self.root, text="Project Paths", padding="10")
        info_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(info_frame, text=f"Source: {self.orca_profiles_dir}",
                  font=("Courier", 9)).pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Output: {self.output_dir}",
                  font=("Courier", 9)).pack(anchor=tk.W)

        # Printer selection
        selection_frame = ttk.LabelFrame(self.root, text="Available Printers", padding="10")
        selection_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Toolbar
        toolbar = ttk.Frame(selection_frame)
        toolbar.pack(fill=tk.X, pady=(0, 5))

        ttk.Button(toolbar, text="Select All Brands", command=self._select_all_brands).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Select All Klipper", command=self._select_all_klipper).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Deselect All", command=self._deselect_all).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Expand All", command=self._expand_all).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Collapse All", command=self._collapse_all).pack(side=tk.LEFT, padx=2)

        ttk.Label(toolbar, text="Filter:").pack(side=tk.LEFT, padx=(10, 2))
        self.filter_var = tk.StringVar()
        self.filter_var.trace("w", self._apply_filter)
        ttk.Entry(toolbar, textvariable=self.filter_var, width=20).pack(side=tk.LEFT)

        # Treeview for brands and models
        tree_frame = ttk.Frame(selection_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(tree_frame, columns=("type", "klipper"), show="tree headings", selectmode="extended")
        self.tree.heading("#0", text="Brand / Printer Model")
        self.tree.heading("type", text="Type")
        self.tree.heading("klipper", text="Klipper")
        self.tree.column("#0", width=500)
        self.tree.column("type", width=100, anchor=tk.CENTER)
        self.tree.column("klipper", width=80, anchor=tk.CENTER)

        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Bind selection
        self.tree.bind("<space>", self._toggle_selection)
        self.tree.bind("<Double-1>", self._toggle_selection)
        self.tree.bind("<Button-1>", self._on_click)

        # Conversion controls
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X)

        self.convert_button = ttk.Button(
            control_frame,
            text="Convert Selected",
            command=self._start_conversion,
            state=tk.DISABLED
        )
        self.convert_button.pack(side=tk.LEFT, padx=5)

        self.progress_var = tk.StringVar(value="Ready - Scanning profiles...")
        ttk.Label(control_frame, textvariable=self.progress_var).pack(side=tk.LEFT, padx=10)

        # Log output
        log_frame = ttk.LabelFrame(self.root, text="Conversion Log", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def _scan_printers(self):
        """Scan for available printer brands and models"""
        if not self.orca_profiles_dir.exists():
            messagebox.showerror("Error", f"OrcaSlicer profiles not found at:\n{self.orca_profiles_dir}")
            return

        self._log("Scanning for printer brands and models...")
        self.brands.clear()
        self.tree.delete(*self.tree.get_children())

        # Scan subdirectories
        for brand_dir in sorted(self.orca_profiles_dir.iterdir()):
            if brand_dir.is_dir() and not brand_dir.name.startswith("."):
                # Check if it has machine profiles
                if (brand_dir / "machine").exists():
                    brand = PrinterBrand(brand_dir.name, brand_dir)
                    if brand.models:
                        self.brands[brand.name] = brand

                        # Add brand to tree
                        brand_id = self.tree.insert(
                            "",
                            tk.END,
                            text=f"📁 {brand.name}",
                            values=(f"{len(brand.models)} models", f"{brand.klipper_count} Klipper"),
                            tags=("brand",)
                        )

                        # Add models under brand
                        for model in brand.models:
                            klipper_text = "✓ Klipper" if model.is_klipper else ""
                            self.tree.insert(
                                brand_id,
                                tk.END,
                                text=f"  🖨️  {model.name}",
                                values=("Printer", klipper_text),
                                tags=("model", "klipper" if model.is_klipper else "non-klipper")
                            )

        total_models = sum(len(b.models) for b in self.brands.values())
        total_klipper = sum(b.klipper_count for b in self.brands.values())

        self._log(f"Found {len(self.brands)} brands with {total_models} models ({total_klipper} Klipper)")
        self.progress_var.set(f"Ready - {len(self.brands)} brands, {total_models} models")
        self.convert_button.config(state=tk.NORMAL)

        # Configure tag colors
        self.tree.tag_configure("selected", background="#cce5ff")
        self.tree.tag_configure("klipper", foreground="#006600")

    def _on_click(self, event):
        """Handle tree click"""
        region = self.tree.identify("region", event.x, event.y)
        if region == "tree":
            item = self.tree.identify_row(event.y)
            if item:
                self._toggle_item(item)

    def _toggle_selection(self, event=None):
        """Toggle selection of focused item"""
        selection = self.tree.selection()
        for item in selection:
            self._toggle_item(item)

    def _toggle_item(self, item):
        """Toggle selection state of an item"""
        tags = self.tree.item(item, "tags")

        if "brand" in tags:
            # Toggle entire brand
            brand_name = self.tree.item(item, "text").replace("📁 ", "")

            # Check if brand is selected
            brand_selected = any(b == brand_name and m is None for b, m in self.selected_items)

            if brand_selected:
                # Deselect brand and all models
                self.selected_items = {(b, m) for b, m in self.selected_items if b != brand_name}
                self.tree.item(item, tags=("brand",))
                # Deselect all children
                for child in self.tree.get_children(item):
                    self.tree.item(child, tags=self.tree.item(child, "tags"))
            else:
                # Select entire brand
                self.selected_items.add((brand_name, None))
                # Remove individual model selections for this brand
                self.selected_items = {(b, m) for b, m in self.selected_items if b != brand_name or m is None}
                self.tree.item(item, tags=("brand", "selected"))
                # Select all children visually
                for child in self.tree.get_children(item):
                    child_tags = list(self.tree.item(child, "tags"))
                    if "selected" not in child_tags:
                        child_tags.append("selected")
                    self.tree.item(child, tags=tuple(child_tags))

        elif "model" in tags:
            # Toggle individual model
            parent = self.tree.parent(item)
            brand_name = self.tree.item(parent, "text").replace("📁 ", "")
            model_name = self.tree.item(item, "text").replace("  🖨️  ", "")

            # Check if whole brand is selected
            brand_selected = (brand_name, None) in self.selected_items

            if brand_selected:
                # Can't deselect individual model when whole brand is selected
                return

            # Toggle individual model
            if (brand_name, model_name) in self.selected_items:
                self.selected_items.remove((brand_name, model_name))
                current_tags = list(self.tree.item(item, "tags"))
                if "selected" in current_tags:
                    current_tags.remove("selected")
                self.tree.item(item, tags=tuple(current_tags))
            else:
                self.selected_items.add((brand_name, model_name))
                current_tags = list(self.tree.item(item, "tags"))
                if "selected" not in current_tags:
                    current_tags.append("selected")
                self.tree.item(item, tags=tuple(current_tags))

        self._update_selection_display()

    def _select_all_brands(self):
        """Select all brands"""
        self.selected_items.clear()
        for brand_name in self.brands:
            self.selected_items.add((brand_name, None))
        self._refresh_tree_selection()
        self._update_selection_display()

    def _select_all_klipper(self):
        """Select all Klipper printers"""
        self.selected_items.clear()
        for brand_name, brand in self.brands.items():
            for model in brand.models:
                if model.is_klipper:
                    self.selected_items.add((brand_name, model.name))
        self._refresh_tree_selection()
        self._update_selection_display()

    def _deselect_all(self):
        """Deselect all"""
        self.selected_items.clear()
        self._refresh_tree_selection()
        self._update_selection_display()

    def _expand_all(self):
        """Expand all tree items"""
        for item in self.tree.get_children():
            self.tree.item(item, open=True)

    def _collapse_all(self):
        """Collapse all tree items"""
        for item in self.tree.get_children():
            self.tree.item(item, open=False)

    def _refresh_tree_selection(self):
        """Refresh visual selection in tree"""
        for item in self.tree.get_children():
            brand_name = self.tree.item(item, "text").replace("📁 ", "")
            brand_selected = (brand_name, None) in self.selected_items

            if brand_selected:
                self.tree.item(item, tags=("brand", "selected"))
            else:
                self.tree.item(item, tags=("brand",))

            # Update children
            for child in self.tree.get_children(item):
                model_name = self.tree.item(child, "text").replace("  🖨️  ", "")
                child_tags = list(self.tree.item(child, "tags"))

                if brand_selected or (brand_name, model_name) in self.selected_items:
                    if "selected" not in child_tags:
                        child_tags.append("selected")
                else:
                    if "selected" in child_tags:
                        child_tags.remove("selected")

                self.tree.item(child, tags=tuple(child_tags))

    def _apply_filter(self, *args):
        """Filter brands by search term"""
        search_term = self.filter_var.get().lower()

        for item in self.tree.get_children():
            brand_name = self.tree.item(item, "text").replace("📁 ", "").lower()
            if search_term in brand_name:
                self.tree.reattach(item, "", tk.END)
            else:
                self.tree.detach(item)

    def _update_selection_display(self):
        """Update the selection display"""
        # Count selected items
        selected_brands = {b for b, m in self.selected_items if m is None}
        selected_models = {(b, m) for b, m in self.selected_items if m is not None}

        total_models = 0
        for brand_name in selected_brands:
            if brand_name in self.brands:
                total_models += len(self.brands[brand_name].models)

        total_models += len(selected_models)

        self.progress_var.set(
            f"Selected: {len(selected_brands)} brands, {len(selected_models)} individual models, {total_models} total models"
        )

    def _start_conversion(self):
        """Start the conversion process"""
        if not self.selected_items:
            messagebox.showwarning("No Selection", "Please select at least one brand or printer")
            return

        # Calculate what will be converted
        brands_to_convert = set()
        for brand_name, model_name in self.selected_items:
            brands_to_convert.add(brand_name)

        total_models = 0
        for brand_name in brands_to_convert:
            if brand_name in self.brands:
                # Check if whole brand or individual models
                if (brand_name, None) in self.selected_items:
                    total_models += len(self.brands[brand_name].models)
                else:
                    # Count individual models
                    total_models += sum(1 for b, m in self.selected_items if b == brand_name and m is not None)

        result = messagebox.askyesno(
            "Confirm Conversion",
            f"Convert {len(brands_to_convert)} brands ({total_models} models)?\n\n"
            f"Output: {self.output_dir}"
        )

        if not result:
            return

        # Disable controls
        self.convert_button.config(state=tk.DISABLED)

        # Clear log
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)

        # Start conversion in background thread
        thread = threading.Thread(target=self._run_conversion, daemon=True)
        thread.start()

    def _run_conversion(self):
        """Run the conversion process (in background thread)"""
        try:
            brands_to_convert = sorted({b for b, m in self.selected_items})

            for i, brand_name in enumerate(brands_to_convert, 1):
                brand = self.brands[brand_name]

                self._log(f"\n{'='*70}")
                self._log(f"[{i}/{len(brands_to_convert)}] Converting {brand_name}")
                self._log(f"{'='*70}")

                self.root.after(0, lambda: self.progress_var.set(
                    f"Converting {brand_name} ({i}/{len(brands_to_convert)})..."
                ))

                # Run converter
                output_path = self.output_dir / brand_name
                converter = ProfileConverter(brand.path, output_path, brand_name)

                # Redirect stdout to log
                import io
                old_stdout = sys.stdout
                sys.stdout = io.StringIO()

                try:
                    converter.convert_all()
                    output = sys.stdout.getvalue()
                    self._log(output)
                except Exception as e:
                    self._log(f"ERROR: {e}")
                finally:
                    sys.stdout = old_stdout

            self._log(f"\n{'='*70}")
            self._log("✅ All conversions complete!")
            self._log(f"{'='*70}")

            self.root.after(0, lambda: messagebox.showinfo(
                "Success",
                f"Successfully converted {len(brands_to_convert)} brands!\n\n"
                f"Output: {self.output_dir}"
            ))

        except Exception as e:
            self._log(f"\n❌ ERROR: {e}")
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))

        finally:
            # Re-enable controls
            self.root.after(0, lambda: self.convert_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self._update_selection_display())

    def _log(self, message):
        """Add message to log"""
        def append():
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, message + "\n")
            self.log_text.see(tk.END)
            self.log_text.config(state=tk.DISABLED)

        if threading.current_thread() is threading.main_thread():
            append()
        else:
            self.root.after(0, append)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = ProfileConverterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
