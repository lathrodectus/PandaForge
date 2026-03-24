#include "FanControlPanel.hpp"
#include <wx/sizer.h>
#include <wx/stattext.h>
#include <curl/curl.h>
#include <nlohmann/json.hpp>
#include "../I18N.hpp"

namespace Slic3r { namespace GUI {

std::map<wxString, PrinterProfile> FanControlPanel::s_profiles;

static size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp) {
    ((wxString*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

void FanControlPanel::InitializeProfiles() {
    if (!s_profiles.empty()) return;
    
    // Creality K1/K1 Max
    {
        PrinterProfile p;
        p.model = "Creality K1";
        p.moonraker_url = "http://printer.local";
        p.supports_moonraker = true;
        p.supports_chamber_fan = false;
        p.supports_aux_fan = false;
        p.fans[FAN_PART_COOLING] = {"Part Cooling", true, 0, 100, "fan", "M106 S{speed}"};
        p.fans[FAN_AUX] = {"Aux Fan", false, 0, 100, "", ""};
        s_profiles["K1"] = p;
        s_profiles["K1 Max"] = p;
        s_profiles["K1C"] = p;
    }
    
    // Qidi Q2/Max4
    {
        PrinterProfile p;
        p.model = "Qidi Q2";
        p.moonraker_url = "http://printer.local";
        p.supports_moonraker = true;
        p.supports_chamber_fan = true;
        p.supports_aux_fan = true;
        p.fans[FAN_PART_COOLING] = {"Part Cooling", true, 0, 100, "fan", "SET_FAN_SPEED FAN=part_cooling SPEED={speed}"};
        p.fans[FAN_CHAMBER] = {"Chamber", true, 0, 100, "fan_generic chamber_fan", "SET_FAN_SPEED FAN=chamber SPEED={speed}"};
        p.fans[FAN_AUX] = {"Aux", false, 0, 100, "", ""};
        s_profiles["Q2"] = p;
        s_profiles["Max4"] = p;
        s_profiles["Q1 Pro"] = p;
    }
    
    // Flashforge Adventurer 5M Pro
    {
        PrinterProfile p;
        p.model = "Flashforge Adventurer 5M Pro";
        p.moonraker_url = "http://printer.local";
        p.supports_moonraker = true;
        p.supports_chamber_fan = false;
        p.supports_aux_fan = false;
        p.fans[FAN_PART_COOLING] = {"Part Cooling", true, 0, 100, "fan", "M106 S{speed}"};
        s_profiles["Adventurer 5M"] = p;
        s_profiles["Adventurer 5M Pro"] = p;
    }
    
    // Two Trees Centauri Carbon
    {
        PrinterProfile p;
        p.model = "Centauri Carbon";
        p.moonraker_url = "http://printer.local";
        p.supports_moonraker = true;
        p.supports_chamber_fan = true;
        p.supports_aux_fan = true;
        p.fans[FAN_PART_COOLING] = {"Part Cooling", true, 0, 100, "fan", "SET_FAN_SPEED FAN=part_cooling SPEED={speed}"};
        p.fans[FAN_CHAMBER] = {"Chamber", true, 0, 100, "fan_generic chamber", "SET_FAN_SPEED FAN=chamber SPEED={speed}"};
        p.fans[FAN_AUX] = {"Aux", true, 0, 100, "fan_generic aux", "SET_FAN_SPEED FAN=aux SPEED={speed}"};
        s_profiles["Centauri"] = p;
        s_profiles["Centauri Carbon"] = p;
    }
}

FanControlPanel::FanControlPanel(wxWindow* parent)
    : wxPanel(parent, wxID_ANY)
{
    InitializeProfiles();
    CreateUI();
}

FanControlPanel::~FanControlPanel() {
    StopPolling();
}

void FanControlPanel::CreateUI() {
    wxBoxSizer* mainSizer = new wxBoxSizer(wxVERTICAL);
    
    // Title and printer model
    wxBoxSizer* titleSizer = new wxBoxSizer(wxHORIZONTAL);
    wxStaticText* title = new wxStaticText(this, wxID_ANY, _L("Klipper Fan Control"));
    wxFont titleFont = title->GetFont();
    titleFont.SetPointSize(titleFont.GetPointSize() + 2);
    title->SetFont(titleFont);
    titleSizer->Add(title, 0, wxALIGN_CENTER_VERTICAL);
    titleSizer->AddStretchSpacer(1);
    
    m_lblPrinterModel = new wxStaticText(this, wxID_ANY, _L("No printer connected"));
    titleSizer->Add(m_lblPrinterModel, 0, wxALIGN_CENTER_VERTICAL | wxRIGHT, 10);
    mainSizer->Add(titleSizer, 0, wxEXPAND | wxALL, 10);
    
    // Fan controls grid
    wxFlexGridSizer* fanSizer = new wxFlexGridSizer(2, 10, 10);
    fanSizer->AddGrowableCol(1, 1);
    
    // Part cooling fan
    m_lblPartFan = new wxStaticText(this, wxID_ANY, _L("Part Cooling:"));
    m_spinPartFan = new wxSpinCtrl(this, wxID_ANY, "0", wxDefaultPosition, wxSize(80, -1), 
                                   wxSP_ARROW_KEYS, 0, 100, 0);
    // m_spinPartFan->SetSuffix("%"); // Not available in wx 3.1
    fanSizer->Add(m_lblPartFan, 0, wxALIGN_CENTER_VERTICAL);
    fanSizer->Add(m_spinPartFan, 0, wxEXPAND);
    
    // Chamber fan
    m_lblChamberFan = new wxStaticText(this, wxID_ANY, _L("Chamber Fan:"));
    m_spinChamberFan = new wxSpinCtrl(this, wxID_ANY, "0", wxDefaultPosition, wxSize(80, -1),
                                      wxSP_ARROW_KEYS, 0, 100, 0);
    // m_spinChamberFan->SetSuffix("%"); // Not available in wx 3.1
    fanSizer->Add(m_lblChamberFan, 0, wxALIGN_CENTER_VERTICAL);
    fanSizer->Add(m_spinChamberFan, 0, wxEXPAND);
    
    // Aux fan
    m_lblAuxFan = new wxStaticText(this, wxID_ANY, _L("Aux Fan:"));
    m_spinAuxFan = new wxSpinCtrl(this, wxID_ANY, "0", wxDefaultPosition, wxSize(80, -1),
                                  wxSP_ARROW_KEYS, 0, 100, 0);
    // m_spinAuxFan->SetSuffix("%"); // Not available in wx 3.1
    fanSizer->Add(m_lblAuxFan, 0, wxALIGN_CENTER_VERTICAL);
    fanSizer->Add(m_spinAuxFan, 0, wxEXPAND);
    
    // Exhaust fan
    m_lblExhaustFan = new wxStaticText(this, wxID_ANY, _L("Exhaust Fan:"));
    m_spinExhaustFan = new wxSpinCtrl(this, wxID_ANY, "0", wxDefaultPosition, wxSize(80, -1),
                                      wxSP_ARROW_KEYS, 0, 100, 0);
    // m_spinExhaustFan->SetSuffix("%"); // Not available in wx 3.1
    fanSizer->Add(m_lblExhaustFan, 0, wxALIGN_CENTER_VERTICAL);
    fanSizer->Add(m_spinExhaustFan, 0, wxEXPAND);
    
    mainSizer->Add(fanSizer, 0, wxEXPAND | wxLEFT | wxRIGHT, 15);
    
    // Buttons
    wxBoxSizer* btnSizer = new wxBoxSizer(wxHORIZONTAL);
    m_btnApply = new wxButton(this, wxID_ANY, _L("Apply"));
    m_btnRefresh = new wxButton(this, wxID_ANY, _L("Refresh"));
    m_chkAutoRefresh = new wxCheckBox(this, wxID_ANY, _L("Auto-refresh"));
    
    btnSizer->Add(m_btnApply, 0, wxRIGHT, 5);
    btnSizer->Add(m_btnRefresh, 0, wxRIGHT, 10);
    btnSizer->Add(m_chkAutoRefresh, 0, wxALIGN_CENTER_VERTICAL);
    btnSizer->AddStretchSpacer(1);
    
    m_lblStatus = new wxStaticText(this, wxID_ANY, _L("Status: Ready"));
    btnSizer->Add(m_lblStatus, 0, wxALIGN_CENTER_VERTICAL);
    
    mainSizer->Add(btnSizer, 0, wxEXPAND | wxALL, 10);
    
    SetSizer(mainSizer);
    
    // Bind events
    m_btnApply->Bind(wxEVT_BUTTON, &FanControlPanel::OnApplyClicked, this);
    m_btnRefresh->Bind(wxEVT_BUTTON, [this](wxCommandEvent&) { UpdateFanSpeedsFromPrinter(); });
    m_chkAutoRefresh->Bind(wxEVT_CHECKBOX, &FanControlPanel::OnAutoRefreshToggle, this);
    
    m_spinPartFan->Bind(wxEVT_SPINCTRL, &FanControlPanel::OnPartFanChange, this);
    m_spinChamberFan->Bind(wxEVT_SPINCTRL, &FanControlPanel::OnChamberFanChange, this);
    m_spinAuxFan->Bind(wxEVT_SPINCTRL, &FanControlPanel::OnAuxFanChange, this);
    m_spinExhaustFan->Bind(wxEVT_SPINCTRL, &FanControlPanel::OnExhaustFanChange, this);
    
    // Initially disable controls until printer is set
    EnableFanControls(false);
}

void FanControlPanel::EnableFanControls(bool enable) {
    m_spinPartFan->Enable(enable);
    m_spinChamberFan->Enable(enable && m_profile.supports_chamber_fan);
    m_spinAuxFan->Enable(enable && m_profile.supports_aux_fan);
    m_spinExhaustFan->Enable(enable);
    m_btnApply->Enable(enable);
    m_btnRefresh->Enable(enable);
    m_chkAutoRefresh->Enable(enable);
}

void FanControlPanel::SetPrinterProfile(const PrinterProfile& profile) {
    m_profile = profile;
    m_lblPrinterModel->SetLabel(profile.model);
    
    // Update UI based on profile capabilities
    m_lblChamberFan->Enable(profile.supports_chamber_fan);
    m_spinChamberFan->Enable(profile.supports_chamber_fan);
    m_lblAuxFan->Enable(profile.supports_aux_fan);
    m_spinAuxFan->Enable(profile.supports_aux_fan);
    
    EnableFanControls(profile.supports_moonraker);
    UpdateStatus(_L("Printer profile loaded: ") + profile.model);
}

void FanControlPanel::SetPrinterURL(const wxString& url) {
    m_profile.moonraker_url = url;
    UpdateStatus(_L("URL set: ") + url);
}

void FanControlPanel::SetPrinterModel(const wxString& model) {
    // Find matching profile
    for (const auto& pair : s_profiles) {
        if (model.Contains(pair.first) || pair.first.Contains(model)) {
            SetPrinterProfile(pair.second);
            return;
        }
    }
    
    // Default profile if no match
    PrinterProfile defaultProfile;
    defaultProfile.model = model.IsEmpty() ? _L("Generic Klipper") : model;
    defaultProfile.supports_moonraker = true;
    defaultProfile.fans[FAN_PART_COOLING] = {"Part Cooling", true, 0, 100, "fan", "M106 S{speed}"};
    SetPrinterProfile(defaultProfile);
}

void FanControlPanel::SetFanSpeed(FanType fan, int speed_percent) {
    speed_percent = std::clamp(speed_percent, 0, 100);
    
    switch(fan) {
        case FAN_PART_COOLING:
            m_spinPartFan->SetValue(speed_percent);
            break;
        case FAN_CHAMBER:
            m_spinChamberFan->SetValue(speed_percent);
            break;
        case FAN_AUX:
            m_spinAuxFan->SetValue(speed_percent);
            break;
        case FAN_EXHAUST:
            m_spinExhaustFan->SetValue(speed_percent);
            break;
    }
    
    m_cached_speeds[fan] = speed_percent;
}

int FanControlPanel::GetFanSpeed(FanType fan) const {
    switch(fan) {
        case FAN_PART_COOLING: return m_spinPartFan->GetValue();
        case FAN_CHAMBER: return m_spinChamberFan->GetValue();
        case FAN_AUX: return m_spinAuxFan->GetValue();
        case FAN_EXHAUST: return m_spinExhaustFan->GetValue();
    }
    return 0;
}

bool FanControlPanel::SendGCode(const wxString& gcode) {
    if (m_profile.moonraker_url.IsEmpty()) {
        UpdateStatus(_L("Error: No printer URL configured"));
        return false;
    }
    
    wxString endpoint = "/printer/gcode/script";
    wxString data = "{\"script\":\"" + gcode + "\"}";
    
    wxString response;
    bool success = MoonrakerRequest(endpoint, "POST", data, &response);
    
    if (!success) {
        UpdateStatus(_L("Error: Failed to send command"));
    }
    
    return success;
}

bool FanControlPanel::MoonrakerRequest(const wxString& endpoint, const wxString& method,
                                       const wxString& data, wxString* response) {
    CURL* curl = curl_easy_init();
    if (!curl) return false;
    
    wxString url = m_profile.moonraker_url + endpoint;
    wxString response_data;
    
    curl_easy_setopt(curl, CURLOPT_URL, url.ToUTF8().data());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response_data);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT, 5L);
    curl_easy_setopt(curl, CURLOPT_CONNECTTIMEOUT, 3L);
    
    struct curl_slist* headers = nullptr;
    headers = curl_slist_append(headers, "Content-Type: application/json");
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    
    if (method == "POST") {
        curl_easy_setopt(curl, CURLOPT_POST, 1L);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data.ToUTF8().data());
    }
    
    CURLcode res = curl_easy_perform(curl);
    
    long http_code = 0;
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &http_code);
    
    curl_slist_free_all(headers);
    curl_easy_cleanup(curl);
    
    if (response) {
        *response = response_data;
    }
    
    return (res == CURLE_OK && http_code == 200);
}

void FanControlPanel::UpdateFanSpeedsFromPrinter() {
    if (!m_profile.supports_moonraker || m_profile.moonraker_url.IsEmpty()) {
        return;
    }
    
    wxString response;
    if (!MoonrakerRequest("/printer/objects/query?heater=fan", "GET", wxEmptyString, &response)) {
        UpdateStatus(_L("Error: Cannot connect to printer"));
        return;
    }
    
    try {
        auto json = nlohmann::json::parse(response.ToUTF8().data());
        
        // Parse fan speeds from response
        // This is a simplified parsing - actual Moonraker response format may vary
        if (json.contains("result") && json["result"].contains("status")) {
            auto status = json["result"]["status"];
            
            if (status.contains("fan") && m_profile.fans.count(FAN_PART_COOLING)) {
                double speed = status["fan"]["speed"].get<double>();
                SetFanSpeed(FAN_PART_COOLING, static_cast<int>(speed * 100));
            }
            
            // Parse additional fans based on printer profile
            // ...
        }
        
        UpdateStatus(_L("Fan speeds updated"));
    } catch (...) {
        UpdateStatus(_L("Error: Invalid response from printer"));
    }
}

void FanControlPanel::StartPolling(int interval_ms) {
    if (m_polling.load()) return;
    
    m_stop_polling = false;
    m_polling = true;
    m_poll_thread = std::thread(&FanControlPanel::PollThreadFunc, this);
}

void FanControlPanel::StopPolling() {
    m_stop_polling = true;
    if (m_poll_thread.joinable()) {
        m_poll_thread.join();
    }
    m_polling = false;
}

void FanControlPanel::PollThreadFunc() {
    while (!m_stop_polling.load()) {
        wxTheApp->CallAfter([this]() {
            UpdateFanSpeedsFromPrinter();
        });
        
        // Sleep for 2 seconds
        for (int i = 0; i < 20 && !m_stop_polling.load(); i++) {
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }
    }
}

void FanControlPanel::UpdateStatus(const wxString& status) {
    m_lblStatus->SetLabel(_L("Status: ") + status);
}

// Event handlers
void FanControlPanel::OnPartFanChange(wxSpinEvent& evt) {
    int speed = evt.GetValue();
    wxString cmd = wxString::Format("M106 S%d", speed * 255 / 100);
    SendGCode(cmd);
}

void FanControlPanel::OnChamberFanChange(wxSpinEvent& evt) {
    if (m_profile.fans.count(FAN_CHAMBER)) {
        int speed = evt.GetValue();
        float speed_ratio = speed / 100.0f;
        wxString cmd = wxString::Format("SET_FAN_SPEED FAN=chamber SPEED=%.2f", speed_ratio);
        SendGCode(cmd);
    }
}

void FanControlPanel::OnAuxFanChange(wxSpinEvent& evt) {
    if (m_profile.fans.count(FAN_AUX)) {
        int speed = evt.GetValue();
        float speed_ratio = speed / 100.0f;
        wxString cmd = wxString::Format("SET_FAN_SPEED FAN=aux SPEED=%.2f", speed_ratio);
        SendGCode(cmd);
    }
}

void FanControlPanel::OnExhaustFanChange(wxSpinEvent& evt) {
    int speed = evt.GetValue();
    wxString cmd = wxString::Format("M106 P3 S%d", speed * 255 / 100);
    SendGCode(cmd);
}

void FanControlPanel::OnApplyClicked(wxCommandEvent& evt) {
    (void)evt;

    const int part_speed = m_spinPartFan->GetValue();
    SendGCode(wxString::Format("M106 S%d", part_speed * 255 / 100));

    if (m_profile.fans.count(FAN_CHAMBER)) {
        const int chamber_speed = m_spinChamberFan->GetValue();
        const float chamber_ratio = chamber_speed / 100.0f;
        SendGCode(wxString::Format("SET_FAN_SPEED FAN=chamber SPEED=%.2f", chamber_ratio));
    }

    if (m_profile.fans.count(FAN_AUX)) {
        const int aux_speed = m_spinAuxFan->GetValue();
        const float aux_ratio = aux_speed / 100.0f;
        SendGCode(wxString::Format("SET_FAN_SPEED FAN=aux SPEED=%.2f", aux_ratio));
    }

    const int exhaust_speed = m_spinExhaustFan->GetValue();
    SendGCode(wxString::Format("M106 P3 S%d", exhaust_speed * 255 / 100));

    UpdateStatus(_L("Fan speeds applied"));
}

void FanControlPanel::OnAutoRefreshToggle(wxCommandEvent& evt) {
    if (evt.IsChecked()) {
        StartPolling();
        UpdateStatus(_L("Auto-refresh enabled"));
    } else {
        StopPolling();
        UpdateStatus(_L("Auto-refresh disabled"));
    }
}

}} // namespace Slic3r::GUI
