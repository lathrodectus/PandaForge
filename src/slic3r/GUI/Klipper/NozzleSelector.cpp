#include "NozzleSelector.hpp"
#include "libslic3r/PrintConfig.hpp"
#include "slic3r/GUI/GUI.hpp"
#include "slic3r/GUI/Plater.hpp"
#include <wx/config.h>

namespace Slic3r { namespace GUI {

void NozzleSelector::InitializePresets() {
    m_presets = {
        {0.20f, _L("0.2mm (Miniatures)"), 0.50f, 0.80f, 0.70f, 0.12f, 0.08f},
        {0.25f, _L("0.25mm (Ultra Detail)"), 0.625f, 0.85f, 0.75f, 0.16f, 0.10f},
        {0.30f, _L("0.3mm (Detail)"), 0.75f, 0.90f, 0.80f, 0.20f, 0.12f},
        {0.40f, _L("0.4mm (Standard)"), 1.0f, 1.0f, 1.0f, 0.28f, 0.20f},
        {0.50f, _L("0.5mm (Speed)"), 1.25f, 1.10f, 1.10f, 0.36f, 0.25f},
        {0.60f, _L("0.6mm (Draft)"), 1.50f, 1.15f, 1.20f, 0.44f, 0.30f},
        {0.80f, _L("0.8mm (Max Draft)"), 2.0f, 1.25f, 1.30f, 0.60f, 0.40f}
    };
}

NozzleSelector::NozzleSelector(wxWindow* parent)
    : wxComboBox(parent, wxID_ANY, wxEmptyString, 
                 wxDefaultPosition, wxSize(150, -1), 
                 0, nullptr, wxCB_READONLY)
{
    InitializePresets();
    
    wxArrayString choices;
    for(const auto& preset : m_presets) {
        choices.Add(preset.label);
    }
    Set(choices);
    SetSelection(3); // Default to 0.4mm
    
    // Bind selection change event
    Bind(wxEVT_COMBOBOX, &NozzleSelector::OnNozzleChanged, this);
    
    // Set tooltip
    SetToolTip(_L("Select nozzle diameter - settings will auto-scale"));
}

float NozzleSelector::GetNozzleDiameter() const {
    int sel = GetSelection();
    if(sel >= 0 && sel < (int)m_presets.size()) {
        return m_presets[sel].diameter;
    }
    return 0.4f;
}

void NozzleSelector::SetNozzleDiameter(float diameter) {
    for(size_t i = 0; i < m_presets.size(); i++) {
        if(std::abs(m_presets[i].diameter - diameter) < 0.01f) {
            SetSelection(i);
            return;
        }
    }
}

const NozzlePreset* NozzleSelector::GetCurrentPreset() const {
    return FindPreset(GetNozzleDiameter());
}

const NozzlePreset* NozzleSelector::FindPreset(float diameter) const {
    for(const auto& preset : m_presets) {
        if(std::abs(preset.diameter - diameter) < 0.01f) {
            return &preset;
        }
    }
    return nullptr;
}

void NozzleSelector::ApplyScalingToConfig(DynamicPrintConfig& config) {
    if (!m_auto_scaling) return;
    
    const NozzlePreset* preset = GetCurrentPreset();
    if(!preset) return;
    
    float base_diameter = 0.4f; // Reference size
    
    // Set nozzle diameter
    ConfigOptionFloats* nozzle_opt = new ConfigOptionFloats(1, preset->diameter);
    config.set_key_value("nozzle_diameter", nozzle_opt);
    
    // Scale line widths
    if(config.option("line_width")) {
        float line_width = preset->diameter * preset->line_width_factor;
        config.set_key_value("line_width", new ConfigOptionFloat(line_width));
    }
    if(config.option("external_perimeter_extrusion_width")) {
        float ext_width = preset->diameter * preset->line_width_factor;
        config.set_key_value("external_perimeter_extrusion_width", new ConfigOptionFloatOrPercent(ext_width, false));
    }
    
    // Scale layer height
    config.set_key_value("layer_height", new ConfigOptionFloat(preset->layer_height_default));
    
    // Scale speeds (conservative approach)
    if(config.option("speed_print")) {
        float base_speed = 150.0f; // Default reference speed
        float speed = base_speed * preset->speed_factor;
        config.set_key_value("speed_print", new ConfigOptionFloat(speed));
    }
    
    // Scale retractions
    if(config.option("retract_length")) {
        float base_retract = 0.8f;
        float retract = base_retract * preset->retraction_factor;
        config.set_key_value("retract_length", new ConfigOptionFloats(1, retract));
    }
    
    // Store nozzle size in config
    wxConfigBase* wxconf = wxConfigBase::Get();
    if (wxconf) {
        wxconf->Write("/klipper/nozzle_diameter", preset->diameter);
        wxconf->Write("/klipper/layer_height_default", preset->layer_height_default);
        wxconf->Write("/klipper/layer_height_max", preset->layer_height_max);
    }
}

void NozzleSelector::OnNozzleChanged(wxCommandEvent& evt) {
    if (m_auto_scaling) {
        // Get current plater and update config
        Plater* plater = wxGetApp().plater();
        if(plater) {
            DynamicPrintConfig cfg = *plater->config();
            ApplyScalingToConfig(cfg);
            plater->on_config_change(cfg);
        }
    }
    evt.Skip();
}

}} // namespace Slic3r::GUI
