#ifndef NOZZLE_SELECTOR_HPP
#define NOZZLE_SELECTOR_HPP

#include <wx/wx.h>
#include <wx/combobox.h>
#include <vector>
#include <cmath>
#include "../I18N.hpp"

namespace Slic3r {
    class DynamicPrintConfig;
}

namespace Slic3r { namespace GUI {

struct NozzlePreset {
    float diameter;
    wxString label;
    float line_width_factor;
    float speed_factor;
    float retraction_factor;
    float layer_height_max;
    float layer_height_default;
};

class NozzleSelector : public wxComboBox {
public:
    NozzleSelector(wxWindow* parent);
    
    float GetNozzleDiameter() const;
    void SetNozzleDiameter(float diameter);
    
    // Apply scaling to current print settings
    void ApplyScalingToConfig(DynamicPrintConfig& config);
    
    // Get the current preset
    const NozzlePreset* GetCurrentPreset() const;
    
    // Check if auto-scaling should be applied
    bool IsAutoScalingEnabled() const { return m_auto_scaling; }
    void SetAutoScaling(bool enable) { m_auto_scaling = enable; }
    
private:
    void OnNozzleChanged(wxCommandEvent& evt);
    const NozzlePreset* FindPreset(float diameter) const;
    void InitializePresets();
    
    std::vector<NozzlePreset> m_presets;
    bool m_auto_scaling = true;
};

}} // namespace Slic3r::GUI

#endif // NOZZLE_SELECTOR_HPP
