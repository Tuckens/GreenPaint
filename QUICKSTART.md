# QUICK START GUIDE: OS Security Posture Monitor

## 5-Minute Setup

### Step 1: Clone Repository (1 minute)
```bash
git clone https://github.com/YOUR_USERNAME/OS-Security-Monitor.git
cd OS-Security-Monitor
```

### Step 2: Install Dependencies (1 minute)
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application (30 seconds)
**Run as Administrator** (required for full scanning):
```bash
python main.py
```

Or use the prebuilt executable:
```bash
GreenPaint.exe
```

### Step 4: Wait for Initial Scan (2-3 minutes)
- Application automatically starts scanning on launch
- Progress updates shown in status bar
- Dashboard updates with results once scan completes

### Step 5: Review Your Security Score
- Security Score displayed in header (0-100)
- Security cards show status of each component
- Recent Issues list shows vulnerabilities to address

## Understanding the Dashboard

### Security Score Interpretation
- **0-30**: 🔴 Critical - Immediate hardening needed
- **31-60**: 🟠 High Risk - Multiple vulnerabilities
- **61-80**: 🟡 Fair - Room for improvement
- **81-100**: 🟢 Excellent - Strong security posture

### Security Cards
Each card shows real-time status:
- 🟢 **Green/Enabled**: Properly configured
- 🟡 **Yellow/Warning**: Needs attention
- 🔴 **Red/Disabled**: Critical - action needed

## First 30 Minutes: Critical Actions

### Priority 1: Review Dashboard (5 minutes)
1. After scan completes, review Security Score
2. Check each security category card
3. Read "Recent Security Issues" list

### Priority 2: Enable Firewall (3 minutes)
1. If Firewall shows "Disabled" in dashboard
2. Go to "Hardening Guide" tab
3. Find "Enable Windows Firewall"
4. Click "Implement Now" for instructions

### Priority 3: Enable Antivirus (3 minutes)
1. In "Hardening Guide", find antivirus step
2. Click "Implement Now"
3. Follow step-by-step instructions

### Priority 4: Install Updates (5 minutes)
1. Find "Install Critical Security Updates"
2. Click "Implement Now"
3. Allow system to install updates

### Priority 5: Backup & Plan (9 minutes)
1. Plan your security improvements
2. Note which hardware supports BitLocker/TPM
3. Set up automatic backups before making changes

## First Week: High Priority Actions

After completing critical items, tackle high-priority hardening:

**Day 1-2:**
- Enable User Account Control (UAC)
- Configure Windows Defender scans

**Day 3-4:**
- Set up BitLocker encryption
- Set strong password policy

**Day 5-6:**
- Enable Secure Boot (if available)
- Set up automatic backups

**Day 7:**
- Review combined security score
- Export security report to track progress

## Monitoring Your Progress

### Weekly Checks
```
1. Launch the application (main.py)
2. Click "🔄 Refresh Scan" to get latest status
3. Compare current score to previous week
4. Identify any newly discovered issues
5. Plan next hardening steps
```

### Track Completed Steps
Keep a simple checklist:
- [ ] Enable Firewall
- [ ] Enable Antivirus
- [ ] Install Updates
- [ ] Enable UAC
- [ ] Enable BitLocker
- [ ] Set Strong Passwords
- ...etc

## Common Questions

### Q: Do I need administrator access?
**A:** Yes, most security checks require administrator privileges. Some checks may not work without elevated permissions.

### Q: How long does a scan take?
**A:** First scan: 2-3 minutes | Subsequent scans: 1-2 minutes (varies by system load)

### Q: Will hardening slow down my system?
**A:** Most security features have minimal impact. Some features like disk encryption may slightly affect disk performance, but security gains outweigh the cost.

### Q: Can I undo hardening changes?
**A:** Most changes can be reversed. Always note which settings you changed. The application provides undo instructions for major steps.

### Q: Is encryption safe?
**A:** Yes, BitLocker encryption is secure. Just ensure you save your recovery key in a safe place.

### Q: How often should I run scans?
**A:** Weekly is recommended. After major OS updates, always run a scan.

## Keyboard Shortcuts

(Standard PyQt5 shortcuts)
- `Ctrl+Q`: Exit application
- `Ctrl+R`: Refresh scan (when focus on main window)
- `Tab`: Navigate between tabs
- `Alt+Tab`: Switch between applications

## Feature Overview

### Dashboard Tab ⭐ START HERE
```
┌─────────────────────────────┐
│ Security Posture Monitor    │
│ Score: 65/100               │
└──────────────────┬──────────┘
│
├─ Security Overview
│  ├─ Firewall: Enabled
│  ├─ Antivirus: Running
│  ├─ Updates: Pending
│  ├─ UAC: Enabled
│  ├─ Network: Secure
│  └─ Encryption: Enabled
│
└─ Recent Issues
   ├─ ⚠️ Missing KB update
   ├─ ⚠️ Scheduled scans disabled
   ...
```

### Security Status Tab 📋
Detailed individual checks for each security component

### Hardening Guide Tab 🚀 MAIN WORK HERE
Step-by-step instructions for improving security
Click "Implement Now" for any recommendation

### Settings Tab ⚙️
Configure application preferences and export reports

## Next Steps

1. **Immediate**: Run the scan and review your security score
2. **This Week**: Implement all Critical priority hardening steps
3. **This Month**: Complete all High priority hardening steps
4. **Ongoing**: Run weekly scans and maintain security practices

## Emergency Contacts & Resources

### If You Suspect a Security Breach
1. Disconnect from network (if possible)
2. Run a full system scan with antivirus
3. Change all important passwords
4. Contact your IT support or Microsoft Security Response Center

### Helpful Resources
- Microsoft Security Baselines: https://docs.microsoft.com/security/baselines
- NIST Cybersecurity Framework: https://www.nist.gov/cyberframework
- CIS Benchmarks: https://www.cisecurity.org/cis-benchmarks

## Tips for Success

✅ **Do:**
- Start with Critical priority items
- Follow the step-by-step guides carefully
- Create backups before making changes
- Run weekly scans
- Document your changes
- Share results with IT team (if in corporate environment)

❌ **Don't:**
- Skip the Firewall or Antivirus steps
- Use weak passwords
- Disable security features for convenience
- Ignore critical issues
- Make multiple changes without testing
- Share security reports containing sensitive data

## Support & Troubleshooting

### Application Crashes
1. Close the application
2. Restart your computer
3. Run `python main.py` again

### Elevated Privilege Required
Windows: Right-click main.py → "Run as Administrator"
Linux/Mac: `sudo python3 main.py`

### Missing Features or Errors
1. Check Python version: `python --version` (need 3.8+)
2. Verify dependencies: `pip install -r requirements.txt --upgrade`
3. Check error logs for details

## Giving Feedback

Encountered an issue or have suggestions?
- Note the error message
- Document steps to reproduce
- Include your OS and Python version
- Provide security scan results screenshot

---

**Ready to Secure Your System? Let's Go! 🔒**

Start with the Dashboard tab and follow the recommendations.
Your security journey begins now!
