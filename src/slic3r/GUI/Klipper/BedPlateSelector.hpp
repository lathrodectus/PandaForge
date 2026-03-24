#ifndef BED_PLATE_SELECTOR_HPP
#define BED_PLATE_SELECTOR_HPP

#include <wx/wx.h>
#include <wx/combobox.h>
#include <wx/arrstr.h>
#include "../I18N.hpp"

namespace Slic3r { namespace GUI {

enum BedPlateType {
    BED_COOL_PLATE = 0,
    BED_ENGINEERING_PLATE,
    BED_HIGH_TEMP_PLATE,
    BED_TEXTURED_PEI,
    BED_CUSTOM
};

class BedPlateSelector : public wxComboBox {
public:
    BedPlateSelector(wxWindow* parent);
    
    BedPlateType GetSelectedBedPlate() const;
    void SetBedPlate(BedPlateType type);
    wxString GetGCodeVariable() const;
    
    // Get bed temperature recommendation for selected plate
    int GetBedTemp(bool is_first_layer = false) const;
    
private:
    void OnSelectionChanged(wxCommandEvent& evt);
    
    wxArrayString m_choices;
    
    // Bed temperature recommendations (first_layer, other_layers)
    const int m_temps[5][2] = {
        {35, 35},   // Cool Plate
        {100, 100}, // Engineering Plate
        {110, 110}, // High Temp Plate
        {60, 60},   // Textured PEI
        {60, 60}    // Custom
    };
};

}} // namespace Slic3r::GUI

#endif // BED_PLATE_SELECTOR_HPP
