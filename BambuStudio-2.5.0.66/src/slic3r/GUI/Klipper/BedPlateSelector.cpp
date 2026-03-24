#include "BedPlateSelector.hpp"
#include "slic3r/GUI/GUI.hpp"
#include "libslic3r/AppConfig.hpp"
#include "../GUI_App.hpp"

namespace Slic3r { namespace GUI {

BedPlateSelector::BedPlateSelector(wxWindow* parent)
    : wxComboBox(parent, wxID_ANY, wxEmptyString, 
                 wxDefaultPosition, wxSize(160, -1), 
                 0, nullptr, wxCB_READONLY)
{
    // Initialize choices (can't use initializer list with wxArrayString)
    m_choices.Add(_L("Cool Plate"));
    m_choices.Add(_L("Engineering Plate"));
    m_choices.Add(_L("High Temp Plate"));
    m_choices.Add(_L("Textured PEI Plate"));
    m_choices.Add(_L("Custom"));
    
    Set(m_choices);
    SetSelection(3); // Default to Textured PEI for Klipper printers
    
    // Bind selection change event
    Bind(wxEVT_COMBOBOX, &BedPlateSelector::OnSelectionChanged, this);
    
    // Set tooltip
    SetToolTip(_L("Select bed plate type for optimal first layer adhesion"));
}

BedPlateType BedPlateSelector::GetSelectedBedPlate() const {
    return static_cast<BedPlateType>(GetSelection());
}

void BedPlateSelector::SetBedPlate(BedPlateType type) {
    int idx = static_cast<int>(type);
    if (idx >= 0 && idx < (int)m_choices.GetCount()) {
        SetSelection(idx);
    }
}

wxString BedPlateSelector::GetGCodeVariable() const {
    switch(GetSelectedBedPlate()) {
        case BED_COOL_PLATE:       return "Cool Plate";
        case BED_ENGINEERING_PLATE: return "Engineering Plate";
        case BED_HIGH_TEMP_PLATE:   return "High Temp Plate";
        case BED_TEXTURED_PEI:      return "Textured PEI Plate";
        default:                    return "Custom";
    }
}

int BedPlateSelector::GetBedTemp(bool is_first_layer) const {
    int idx = GetSelection();
    if (idx >= 0 && idx < 5) {
        return m_temps[idx][is_first_layer ? 0 : 1];
    }
    return 60;
}

void BedPlateSelector::OnSelectionChanged(wxCommandEvent& evt) {
    // Store in app config for G-code template access
    wxString plate_type = GetGCodeVariable();
    
    // Use Slic3r's AppConfig instead of wxConfigBase
    AppConfig* config = wxGetApp().app_config;
    if (config) {
        config->set("klipper", "bed_type", plate_type.ToStdString());
        config->set("klipper", "bed_temp_first", std::to_string(GetBedTemp(true)));
        config->set("klipper", "bed_temp_other", std::to_string(GetBedTemp(false)));
    }
    
    evt.Skip();
}

}} // namespace Slic3r::GUI
