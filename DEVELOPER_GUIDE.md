"""
Technical Architecture & Developer Guide
For developers extending or maintaining the OS Security Posture Monitor
"""

# TECHNICAL ARCHITECTURE & DEVELOPER GUIDE

## Project Overview

**OS Security Posture Monitor** is a PyQt5-based desktop application for comprehensive OS security assessment and hardening guidance.

### Technology Stack
- **Framework**: PySide6 6.5.0+
- **Language**: Python 3.8+
- **GUI**: Custom PySide6 components with Segoe UI
- **System Integration**: subprocess for PowerShell queries
- **Data Format**: JSON for configuration and reports

## Architecture

### Modular Design

```
main.py (Entry Point)
    ├─ imports → security_scanner.py
    ├─ imports → hardening_steps.py
    ├─ imports → ui_components.py
    ├─ imports → config.py
    │
    └─ SecurityDashboardApp (Main Window)
        ├─ ScannerThread (Background scanning)
        │   └─ SecurityScanner
        │       ├─ scan_windows()
        │       ├─ scan_linux()
        │       └─ scan_macos()
        │
        ├─ Dashboard Tab
        │   ├─ SecurityCard components
        │   └─ Issues list
        │
        ├─ Security Status Tab
        │   └─ Individual check items
        │
        ├─ Hardening Guide Tab
        │   └─ HardeningCard components
        │
        └─ Settings Tab

Config.py (Constants)
    └─ Application settings, colors, fonts
```

### Module Dependencies

```
                   main.py
                     |
        ┌────────────┼────────────┐
        |            |            |
   security_    hardening_    ui_
   scanner.py   steps.py   components.py
        |            |            |
        └────────────┼────────────┘
                     |
                  config.py
```

## Core Modules

### 1. main.py

**Purpose**: Application entry point and main UI window

**Key Classes**:
- `ScannerThread(QThread)`: Background scanning thread
  - Emits `scan_complete` signal when done
  - Emits `progress_update` for status messages
  
- `SecurityDashboardApp(QMainWindow)`: Main application window
  - Manages all tabs and UI components
  - Handles scan results and updates
  - Exports security reports

**Key Methods**:
```python
setup_ui()              # Initialize UI
create_dashboard_tab()  # Build dashboard
create_status_tab()     # Build status tab
create_hardening_tab()  # Build hardening tab
create_settings_tab()   # Build settings tab
start_scan()            # Launch background scan
on_scan_complete()      # Handle scan results
update_dashboard()      # Refresh UI with results
show_implementation_guide()  # Show step details
export_report()         # Save JSON report
```

### 2. security_scanner.py

**Purpose**: Windows security scanning using PowerShell queries

**Key Classes**:
- `SecurityScanner`: Main scanner class
  - Checks admin privileges
  - Executes PowerShell commands in background
  - Returns UI-compatible data format

**Key Methods**:
```python
_run_ps(command: str, timeout: int) -> str
    # Executes PowerShell command silently with timeout
    # Uses STARTUPINFO to hide window without deadlock

get_security_status() -> dict
    # Performs 5 core security checks:
    # - _check_antivirus()
    # - _check_firewall()
    # - _check_bitlocker()
    # - _check_tpm()
    # - _check_secure_boot()

_check_updates() -> dict
    # Checks for pending Windows updates

_check_user_accounts() -> dict
    # Checks User Account Control (UAC) status

_check_network_settings() -> dict
    # Checks network profile (Private/Public)

run_full_scan() -> dict
    # Main interface - returns UI-formatted data
    # Maps raw checks to category names
    # Calculates overall security score
```

**Return Format**:
```python
{
    "overall_score": 75,  # 0-100
    "timestamp": "2026-04-13T10:30:00",
    "Antivirus": {"status": "Enabled"},
    "Firewall": {"status": "Disabled"},
    "Encryption": {"status": "Enabled"},
    "Updates": {"status": "Unknown"},
    "User Accounts": {"status": "Enabled"},
    "Network Security": {"status": "Private"},
    "issues": [
        {
            "title": "Firewall: Disabled",
            "severity": "critical",
            "recommendation": "Firewall is OFF"
        }
    ],
    "categories": { ... }
}
}
```

### 3. hardening_steps.py

**Purpose**: Security hardening recommendations

**Key Classes**:
- `HardeningSteps`: Contains hardening recommendations
  - Stores 20+ hardening steps with instructions
  - Filters by priority, difficulty, OS
  - Tracks completion and calculates improvements

**Data Structure**:
```python
{
    "id": 1,
    "title": "Enable Windows Firewall",
    "description": "...",
    "priority": "Critical",  # Critical, High, Medium, Low
    "difficulty": "Easy",    # Easy, Medium, Hard
    "steps": [
        "Step 1: Open Windows Security",
        "Step 2: ...",
        ...
    ],
    "windows": True,
    "linux": False,
    "macos": False
}
```

**Key Methods**:
```python
get_all_steps()              # Get all recommendations
get_critical_steps()         # Get only critical items
get_steps_by_os()            # Filter by OS type
get_steps_by_difficulty()    # Filter by difficulty
get_step_by_id()             # Get specific step
estimate_security_improvement()  # Score improvement estimate
```

### 4. ui_components.py

**Purpose**: Reusable PyQt5 UI components

**Key Components**:

- `SecurityCard`: Status card for individual security categories
  - Shows title, status, color indicator
  - Supports dynamic status updates
  
- `StatusIndicator`: Simple on/off indicator
  - Visual dot indicator
  - Color coded
  
- `HardeningCard`: Hardening step display
  - Shows title, description, priority
  - Action buttons (Learn More, Implement)
  - Emits signals when clicked
  
- `ProgressIndicator`: Progress bar with percentage
  - Shows completion percentage
  - Updates dynamically
  
- `ThreatIndicator`: Threat level display
  - Shows threat level with color
  - 4 levels: critical, high, medium, low
  
- `MetricCard`: Metric display
  - Large value + unit
  - Color coded by metric

**Common Pattern**:
```python
class CustomComponent(QFrame):
    # PyQt5 signals if needed
    signal_name = pyqtSignal(type)
    
    def __init__(self, parameters):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        # Create layout
        layout = QVBoxLayout(self)
        # Add widgets
        # Set stylesheet
        self.setStyleSheet(...)
    
    def update_data(self, new_data):
        # Update component display
        pass
```

### 5. config.py

**Purpose**: Application configuration and constants

**Contents**:
- Application metadata (name, version, author)
- UI settings (window size, colors, fonts)
- Security thresholds
- Scan settings
- File paths
- Feature flags
- OS-specific settings

## Threading Model

### Main Thread
- Runs PyQt5 event loop
- Handles UI updates
- Processes user interactions

### Scanner Thread
- Background security scanning
- Emits signals to main thread
- Non-blocking long operations

```python
# Signal-based threading pattern
class ScannerThread(QThread):
    scan_complete = pyqtSignal(dict)
    progress_update = pyqtSignal(str)
    
    def run(self):
        self.progress_update.emit("Starting...")
        try:
            results = self.scanner.run_full_scan()
            self.scan_complete.emit(results)
        except Exception as e:
            self.progress_update.emit(f"Error: {e}")

# Main thread connects signals
self.scan_thread = ScannerThread()
self.scan_thread.scan_complete.connect(self.on_scan_complete)
self.scan_thread.start()
```

## Security Scanning Flow

```
User clicks "🔄 Refresh Scan"
    ↓
Main thread creates ScannerThread
    ↓
Thread starts background scan
    ↓
SecurityScanner.run_full_scan()
    ├─ Detect OS type
    ├─ Get OS version
    ├─ Run OS-specific checks
    │   ├─ Check firewall
    │   ├─ Check antivirus
    │   ├─ Check updates
    │   ├─ Check UAC
    │   ├─ Check network
    │   └─ Check encryption
    └─ Collect results
    ↓
Calculate overall security score
    ↓
Generate issues list
    ↓
Emit scan_complete signal with results
    ↓
Main thread receives signal
    ↓
update_dashboard() is called
    ↓
UI updates with new data
```

## How to Extend

### Adding a New Security Check

**Step 1**: Add check method to SecurityScanner
```python
def check_ssl_certificates(self) -> str:
    """Check for valid SSL certificates"""
    try:
        # Platform-specific implementation
        result = subprocess.run([...])
        return "Valid" if result.returncode == 0 else "Invalid"
    except:
        return "Unknown"
```

**Step 2**: Add to scan results
```python
def scan_windows(self):
    results = { ... }
    results["SSL Certificates"] = self.check_ssl_certificates()
    return results
```

**Step 3**: Add UI card in main.py
```python
categories = [
    ("Firewall", "🔥"),
    ("Antivirus", "🛡️"),
    ("SSL Certificates", "🔒"),  # NEW
    ...
]
```

### Adding a New Hardening Step

**Step 1**: Add to hardening_steps.py list
```python
{
    "id": 21,
    "title": "Enable Event Log Forwarding",
    "description": "...",
    "priority": "Medium",
    "difficulty": "Hard",
    "steps": [
        "Step 1: ...",
        "Step 2: ...",
    ],
    "windows": True,
    "linux": False,
    "macos": False
}
```

**Step 2**: No other changes needed - automatically appears in UI

### Creating a Custom UI Component

**Pattern**:
```python
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont

class MyCustomComponent(QFrame):
    def __init__(self, title: str, value: str):
        super().__init__()
        self.title = title
        self.value = value
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        title_label = QLabel(self.title)
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(title_label)
        
        value_label = QLabel(self.value)
        layout.addWidget(value_label)
        
        self.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
            }
        """)
```

## Error Handling

### Exception Handling Pattern
```python
try:
    result = subprocess.run(command, timeout=5)
    return parse_result(result)
except subprocess.TimeoutExpired:
    return "Timeout"
except PermissionError:
    return "Permission Denied"
except Exception as e:
    return f"Error: {str(e)}"
```

### User-Facing Errors
```python
QMessageBox.warning(self, "Error Title", 
                    "User-friendly error description")
```

## Testing

### Unit Test Example
```python
import unittest
from security_scanner import SecurityScanner

class TestSecurityScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = SecurityScanner()
    
    def test_firewall_check(self):
        result = self.scanner.check_windows_firewall()
        self.assertIn(result, ["Enabled", "Disabled", "Unknown"])
    
    def test_scan_complete(self):
        results = self.scanner.run_full_scan()
        self.assertIn("overall_score", results)
        self.assertIn(0, results["overall_score"], 100)

if __name__ == '__main__':
    unittest.main()
```

### Manual Testing Checklist
- [ ] Application launches without errors
- [ ] Scan completes successfully
- [ ] Dashboard updates with results
- [ ] All tabs are accessible
- [ ] Hardening guide displays all steps
- [ ] Implementation guides display correctly
- [ ] Export function creates valid JSON
- [ ] No crashes on invalid OS
- [ ] Error messages are user-friendly
- [ ] Performance is acceptable (scan < 5 min)

## Performance Optimization

### Current Bottlenecks
1. **System calls**: Each check runs a separate subprocess
2. **Network checks**: May timeout if network is slow
3. **First launch**: Initial scan can take 3-5 minutes

### Optimization Opportunities
1. **Parallelization**: Run independent checks simultaneously
2. **Caching**: Store results and check only for changes
3. **Lazy loading**: Load details only when requested
4. **Async operations**: Use more background threads

### Suggested Improvements
```python
# Parallel scanning (Python 3.8+)
from concurrent.futures import ThreadPoolExecutor

def run_full_scan_parallel(self):
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(self.check_firewall): "Firewall",
            executor.submit(self.check_antivirus): "Antivirus",
            executor.submit(self.check_updates): "Updates",
        }
        return {name: future.result() 
                for future, name in futures.items()}
```

## Platform-Specific Considerations

### Windows
- Requires Windows 10/11 Pro or Enterprise for BitLocker
- Some checks need admin privileges
- PowerShell cmdlets require execution policy adjustment
- WMI may be disabled on some systems

### Linux
- Ubuntu/Debian commands differ from RHEL
- Sudo password required for root commands
- Package manager varies (apt vs yum)
- Some distros have security hardening variations

### macOS
- Requires full disk access in System Preferences
- Some security settings require T2 chip
- Gatekeeper configuration is unique to macOS
- SIP prevents some system modifications

## Deployment

### Creating Executable (PyInstaller)
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
# Creates: dist/main.exe (Windows) or dist/main (Linux/Mac)
```

### Configuration Files
- Store user settings in ~/.security_monitor/config.json
- Log files in ~/.security_monitor/logs/
- Reports in ~/.security_monitor/reports/

## Security Best Practices

1. **Input Validation**: Sanitize all command inputs
2. **Privilege Escalation**: Only request admin when needed
3. **Secure Storage**: Don't store sensitive data in code
4. **Error Messages**: Don't leak system information
5. **Subprocess Safety**: Use `shell=False` to prevent injection

## Future Enhancements

### Phase 2 Features
- Cloud sync of security data
- Multi-machine management
- Real-time threat intelligence
- Automated remediation

### Phase 3 Features
- AI-powered recommendations
- Compliance reporting (CIS, NIST)
- Integration with SIEM
- Mobile app companion

## Code Quality Guidelines

### Style Guide
- PEP 8 compliance
- Type hints for functions (Python 3.5+)
- Docstrings for all classes and methods
- Comments for complex logic

### Example
```python
def calculate_security_score(
    self, scan_results: Dict[str, Any]
) -> int:
    """
    Calculate overall security score from scan results.
    
    Args:
        scan_results: Dictionary containing scan results
    
    Returns:
        Security score between 0-100
    
    Raises:
        ValueError: If scan_results is empty
    """
    if not scan_results:
        raise ValueError("Scan results cannot be empty")
    
    score = 0
    # Implementation...
    return max(0, min(100, score))
```

## Resources

### PyQt5 Documentation
- https://doc.qt.io/qt-5/
- https://www.riverbankcomputing.com/static/Docs/PyQt5/

### Python Security
- https://owasp.org/www-community/
- https://python.readthedocs.io/en/latest/

### Windows Security
- https://docs.microsoft.com/security/
- https://www.cisecurity.org/

### Linux Security  
- https://www.kernel.org/doc/
- https://www.redhat.com/en/topics/security

---

**Happy coding! 🚀**

For questions or issues, refer to the main README.md or create detailed reports for debugging.
