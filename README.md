# 🔒 OS Security Posture Monitor

A comprehensive desktop application designed to monitor your operating system's security posture and guide you through hardening steps to reduce exposure to cyber threats.

## Features

### 🎯 Core Features

- **Real-time Security Dashboard** - Visual overview of your system's security status
- **Comprehensive Security Scanning** - Automated checks for critical security components:
  - Firewall status and configuration
  - Antivirus/Antimalware protection
  - System updates detection
  - User Account Control (UAC)
  - Network security profile
  - Disk encryption (BitLocker)
  - TPM 2.0 status
  - Secure Boot status

- **Hardening Guide** - Step-by-step recommendations for improving security:
  - 20+ hardening steps with detailed instructions
  - Priority-based recommendations (Critical → High → Medium)
  - Difficulty ratings to help plan implementation
  - OS-specific guidance (Windows, Linux, macOS)

- **Security Scoring** - Real-time calculation of overall security score (0-100)

- **Issue Tracking** - Identifies and prioritizes security vulnerabilities

- **Report Export** - Generate and export security reports in JSON format

- **Progress Tracking** - Monitor which hardening steps have been implemented

## System Requirements

### Supported Operating Systems
- **Windows 10/11** (Pro or Enterprise - Optimized)
- Ubuntu/Debian-based Linux (Limited support)
- macOS 10.15+ (Limited support)

### Minimum Hardware
- 1 GHz processor
- 2 GB RAM
- 200 MB disk space
- Administrator/sudo access for full scanning

### Software Requirements
- Python 3.8+
- PySide6 for GUI
- Administrative privileges for security scanning

## Installation

### Prerequisites
```bash
python --version  # Requires Python 3.8+
```

### Step 1: Clone or download the repository
```bash
git clone https://github.com/YOUR_USERNAME/OS-Security-Monitor.git
cd OS-Security-Monitor
```

### Step 2: Create a virtual environment (recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the application

**Windows (Run as Administrator - required):**
```bash
python main.py
```

**Or use the prebuilt executable:**
```bash
GreenPaint.exe
```

**Linux/macOS:**
```bash
python3 main.py
```

## Project Structure

```
security-monitor/
├── main.py                  # Main application entry point
├── security_scanner.py      # OS security scanning module
├── hardening_steps.py       # Security hardening recommendations
├── ui_components.py         # Reusable PyQt5 UI components
├── config.py               # Configuration and constants
├── requirements.txt        # Python package dependencies
└── README.md              # This file
```

## Usage Guide

### Dashboard Tab

The dashboard provides an at-a-glance view of your security status:

1. **Security Score** - Shows overall security health (0-100)
2. **Security Cards** - Visual indicators for each security category:
   - 🔥 Firewall
   - 🛡️ Antivirus
   - 📦 Updates
   - 👤 User Accounts
   - 🌐 Network Security
   - 🔐 Encryption

3. **Recent Issues** - Lists identified security vulnerabilities with severity levels

### Security Status Tab

Detailed breakdown of individual security checks:
- Windows Firewall status
- Antivirus/Antimalware
- Windows Updates
- User Account Control (UAC)
- Secure Boot
- TPM 2.0
- Disk Encryption
- Network Settings

### Hardening Guide Tab

Step-by-step hardening recommendations:

1. **View All Steps** - Browse 20+ security hardening recommendations
2. **Priority Levels**:
   - 🔴 Critical - Implement immediately
   - 🟠 High - Implement within 1 week
   - 🟡 Medium - Implement within 1 month

3. **Difficulty Levels**:
   - Easy - 5-10 minutes
   - Medium - 15-30 minutes
   - Hard - 30+ minutes or requires technical knowledge

4. **Implementation Guide** - Click "Implement Now" to see step-by-step instructions

### Settings Tab

- Enable/disable automatic security scans
- Configure scan intervals
- Export security reports
- Notification preferences

## Real-Time Security Checks

The application performs 8 comprehensive real-time checks:

### Antivirus Protection
- Detects installed antivirus products via WMI
- Reports real-time protection status

### Windows Firewall
- Verifies Windows Firewall is enabled
- Checks firewall profile configuration

### BitLocker Encryption
- Checks C: drive encryption status
- Reports protection level (On/Off)

### TPM 2.0/1.2
- Detects TPM presence and status
- Verifies hardware security module availability

### Secure Boot
- Checks UEFI Secure Boot configuration
- Verifies bootloader protection is enabled

### Windows Updates
- Detects pending system updates
- Shows last successful update check timestamp

### User Account Control (UAC)
- Verifies UAC is enabled in registry
- Checks privilege escalation protection

### Network Profile
- Determines network type (Private/Public)
- Reports network discovery status

## Security Hardening Steps

The application includes comprehensive guidance for 20+ security hardening measures:

### Critical Priority (Implement Immediately)

1. **Enable Windows Firewall** - Essential network protection
2. **Enable Real-time Antivirus Protection** - Malware defense
3. **Install Critical Security Updates** - Patch vulnerabilities

### High Priority (Implement This Week)

4. **Enable User Account Control (UAC)** - Prevent unauthorized changes
5. **Enable BitLocker Encryption** - Protect data at rest
6. **Set Strong Password Policy** - Prevent unauthorized access
7. **Configure Antivirus Scans** - Regular malware detection
8. **Set Up Automatic Backups** - Disaster recovery
9. **Enable Secure Boot** - Prevent bootloader tampering

### Medium Priority (Implement This Month)

10. **Disable Unnecessary Services** - Reduce attack surface
11. **Enable Windows Sandbox** - Safe testing environment
12. **Configure Firewall Rules** - Fine-tune access control
13. **Implement VPN** - Encrypt internet traffic
14. **Set Up 2FA** - Multi-factor authentication
15. **Harden Browser** - Web protection
16. **Review User Permissions** - Principle of least privilege
17. **Monitor Network Connections** - Detect anomalies
18. **Configure SSH Hardening** (Linux/macOS)
19. **Set Up Host Firewall** (Linux)
20. **Keep Software Updated** - Ongoing maintenance

## Security Scanning

### What Gets Scanned

The application performs comprehensive checks on:

1. **Firewall Configuration**
   - Windows Firewall status
   - Firewall rules
   - Inbound/outbound restrictions

2. **Antivirus/Antimalware**
   - Windows Defender status
   - Real-time protection
   - Engine updates
   - Signature database updates

3. **System Updates**
   - Pending critical updates
   - Feature updates
   - Optional updates
   - Last update date

4. **User Accounts**
   - Administrative accounts
   - User account control settings
   - Password policies
   - Inactive accounts

5. **Network Security**
   - Network profile settings
   - IPv6 configuration
   - Network discovery
   - File sharing settings

6. **Encryption**
   - BitLocker status
   - Drive encryption
   - EFS (Encrypting File System)
   - NTFS encryption

### Scan Results

Each scan generates:
- Overall security score (0-100)
- Per-category status (Enabled/Disabled/Unknown)
- List of identified issues
- Severity classification (Critical/High/Medium/Low)
- Remediation recommendations

## Security Score Calculation

The application calculates real-time security scores based on the 8 core checks:

```
Base Score: 100 points
- Each check starts at full points
- Critical failures (Disabled): -15 points
- High severity issues (Warning): -8 points

Example:
100 (base)
- 15 (Firewall disabled)
- 8 (Updates pending)
= 77 score
```

### Score Interpretation

- 🔴 **0-30**: Critical - Immediate hardening required
- 🟠 **31-60**: High Risk - Multiple vulnerabilities present
- 🟡 **61-80**: Fair - Room for improvement
- 🟢 **81-100**: Excellent - Strong security posture

## Reporting

### Export Security Report

Reports can be exported in JSON format containing:
- Overall security score
- Scan timestamp
- Per-category status
- Identified issues and recommendations
- Compliance mappings

**To Export:**
1. Go to Settings tab
2. Click "Export Security Report"
3. Save the JSON file to your desired location
4. Use for audits, compliance, or sharing with security teams

## Troubleshooting

### Application Won't Start

**Windows:**
```bash
# Run with administrator privileges
python main.py
```

**Linux/macOS:**
```bash
# May need elevated privileges for full functionality
sudo python3 main.py
```

### Scan Takes Too Long

- PowerShell initialization takes 1-2 seconds per command
- First scan: 2-3 minutes (includes PowerShell startup)
- Subsequent scans: 1-2 minutes
- System load and antivirus may slow down PowerShell queries
- Close CPU-intensive applications

### "Permission Denied" Errors

Many security checks require administrative privileges:

**Windows:** Run `python main.py` as Administrator

**Linux/macOS:** Use `sudo`:
```bash
sudo python3 main.py
```

### PySide6 Import Errors

Reinstall PySide6:
```bash
pip uninstall PySide6
pip install -r requirements.txt
```

## Best Practices

### Regular Scans
- Run scans weekly initially
- After implementing hardening steps, run additional scans
- Schedule automatic scans for consistent monitoring

### Implementing Hardening Steps
1. Start with Critical priority steps
2. Test changes in a sandbox environment if possible
3. Keep track of which steps have been completed
4. Verify each change improved security score
5. Document your implementation process

### Maintaining Security
- Keep all software up to date
- Review firewall rules quarterly
- Update antivirus definitions regularly
- Monitor logs for suspicious activity
- Conduct security assessments monthly

### Data Protection
- Back up security reports regularly
- Store reports in a secure location
- Use encrypted storage for sensitive data
- Limit access to security assessment results

## Advanced Features

### Planned Features (Future Versions)
- Cloud synchronization of security data
- AI-powered security recommendations
- Compliance reporting (CIS, NIST, ISO 27001)
- Real-time threat intelligence integration
- Multi-machine monitoring and management
- Automated remediation capabilities

## Contributing

To contribute to this project:

1. Identify areas for improvement
2. Test changes thoroughly
3. Submit detailed reports of issues
4. Suggest enhancements with use cases

## License

This project is provided as-is for security hardening purposes.

## Disclaimer

**Important:**
- Always test security changes in a non-production environment first
- Some hardening steps may affect system functionality
- Consult with your IT security team before implementing changes
- The authors are not responsible for system issues caused by security configuration changes
- Make backups before making security changes

## Support

For issues, questions, or suggestions:
1. Document the issue with steps to reproduce
2. Note your operating system and Python version
3. Include relevant error messages
4. Provide security scan results if applicable

## References

### Security Standards
- CIS Microsoft Windows 10 Enterprise Benchmark
- NIST Cybersecurity Framework
- ISO/IEC 27001 Information Security Management

### Additional Resources
- [Microsoft Security Baselines](https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-security-baselines)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks)
- [OWASP Top 10](https://owasp.org/www-project-top-ten)

---

**Stay Secure! 🔒**

Last Updated: 2026
Version: 1.0.0
