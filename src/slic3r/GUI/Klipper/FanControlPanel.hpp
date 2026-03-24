#ifndef FAN_CONTROL_PANEL_HPP
#define FAN_CONTROL_PANEL_HPP

#include <wx/wx.h>
#include <wx/spinctrl.h>
#include <thread>
#include <atomic>
#include <mutex>
#include <functional>
#include <map>

namespace Slic3r { namespace GUI {

enum FanType {
    FAN_PART_COOLING = 0,
    FAN_CHAMBER,
    FAN_AUX,
    FAN_EXHAUST
};

struct PrinterFanConfig {
    wxString name;
    bool available;
    int min_speed;
    int max_speed;
    wxString moonraker_fan_name; // For Moonraker API
    wxString klipper_gcode_cmd;  // For direct Klipper/Moonraker G-code
};

struct PrinterProfile {
    wxString model;
    wxString moonraker_url;
    std::map<FanType, PrinterFanConfig> fans;
    bool supports_moonraker;
    bool supports_chamber_fan;
    bool supports_aux_fan;
};

class FanControlPanel : public wxPanel {
public:
    FanControlPanel(wxWindow* parent);
    ~FanControlPanel();
    
    // Set printer configuration
    void SetPrinterProfile(const PrinterProfile& profile);
    void SetPrinterURL(const wxString& url);
    void SetPrinterModel(const wxString& model);
    
    // Manual fan control
    void SetFanSpeed(FanType fan, int speed_percent);
    int GetFanSpeed(FanType fan) const;
    
    // Auto-polling from Moonraker
    void StartPolling(int interval_ms = 2000);
    void StopPolling();
    bool IsPolling() const { return m_polling.load(); }
    
    // Send command to printer
    bool SendGCode(const wxString& gcode);
    
    // Update UI from printer state
    void UpdateFanSpeedsFromPrinter();
    
private:
    void CreateUI();
    void EnableFanControls(bool enable);
    void OnPartFanChange(wxSpinEvent& evt);
    void OnChamberFanChange(wxSpinEvent& evt);
    void OnAuxFanChange(wxSpinEvent& evt);
    void OnExhaustFanChange(wxSpinEvent& evt);
    void OnApplyClicked(wxCommandEvent& evt);
    void OnAutoRefreshToggle(wxCommandEvent& evt);
    
    void PollThreadFunc();
    void UpdateStatus(const wxString& status);
    
    // HTTP request to Moonraker
    bool MoonrakerRequest(const wxString& endpoint, const wxString& method = "GET", 
                          const wxString& data = wxEmptyString, wxString* response = nullptr);
    
    // UI Components
    wxSpinCtrl* m_spinPartFan = nullptr;
    wxSpinCtrl* m_spinChamberFan = nullptr;
    wxSpinCtrl* m_spinAuxFan = nullptr;
    wxSpinCtrl* m_spinExhaustFan = nullptr;
    
    wxStaticText* m_lblPartFan = nullptr;
    wxStaticText* m_lblChamberFan = nullptr;
    wxStaticText* m_lblAuxFan = nullptr;
    wxStaticText* m_lblExhaustFan = nullptr;
    
    wxButton* m_btnApply = nullptr;
    wxButton* m_btnRefresh = nullptr;
    wxCheckBox* m_chkAutoRefresh = nullptr;
    wxStaticText* m_lblStatus = nullptr;
    wxStaticText* m_lblPrinterModel = nullptr;
    
    // State
    PrinterProfile m_profile;
    std::atomic<bool> m_polling{false};
    std::atomic<bool> m_stop_polling{false};
    std::thread m_poll_thread;
    std::mutex m_mutex;
    
    // Fan speed cache
    std::map<FanType, int> m_cached_speeds;
    
    // Predefined profiles
    static std::map<wxString, PrinterProfile> s_profiles;
    static void InitializeProfiles();
};

}} // namespace Slic3r::GUI

#endif // FAN_CONTROL_PANEL_HPP
