"""
Hardening Steps Module
Contains security hardening recommendations for OS security improvement
"""

from typing import List, Dict, Any


class HardeningSteps:
    """Provides security hardening recommendations and implementation steps"""
    
    def __init__(self):
        self.steps = self._initialize_steps()
    
    def _initialize_steps(self) -> List[Dict[str, Any]]:
        """Initialize all hardening steps"""
        return [
            {
                "id": 1,
                "title": "Enable Windows Firewall",
                "description": "Windows Firewall provides a first line of defense against unauthorized access. It monitors incoming and outgoing network connections.",
                "priority": "Critical",
                "difficulty": "Easy",
                "steps": [
                    "Open Windows Security (search for 'Windows Security')",
                    "Click on 'Firewall & network protection'",
                    "Verify all three profiles (Domain, Private, Public) show 'Firewall is on'",
                    "If off, click the profile and toggle the switch to On"
                ],
                "windows": True,
                "linux": False,
                "macos": False
            },
            {
                "id": 2,
                "title": "Enable Windows Defender Real-time Protection",
                "description": "Real-time protection scans files and programs as they run, detecting malware and viruses in real-time.",
                "priority": "Critical",
                "difficulty": "Easy",
                "steps": [
                    "Open Windows Security",
                    "Click on 'Virus & threat protection'",
                    "Under 'Virus & threat protection settings', click 'Manage settings'",
                    "Toggle 'Real-time protection' to On",
                    "Restart your computer if prompted"
                ],
                "windows": True,
                "linux": False,
                "macos": False
            },
            {
                "id": 3,
                "title": "Install Critical Security Updates",
                "description": "Regular security updates patch vulnerabilities that could be exploited by attackers. Critical updates should be installed immediately.",
                "priority": "Critical",
                "difficulty": "Easy",
                "steps": [
                    "Click Windows Start menu",
                    "Search for 'Check for updates'",
                    "Click 'Check for updates'",
                    "If updates are available, click 'Download and install now'",
                    "Allow all recommended and optional updates",
                    "Restart your computer when prompted"
                ],
                "windows": True,
                "linux": True,
                "macos": True
            },
            {
                "id": 4,
                "title": "Enable User Account Control (UAC)",
                "description": "UAC prompts for admin approval before programs can make system changes, preventing unauthorized modifications.",
                "priority": "High",
                "difficulty": "Medium",
                "steps": [
                    "Open Control Panel",
                    "Go to 'User Accounts' > 'User Accounts' > 'Change User Account Control settings'",
                    "Move the slider to 'Always notify'",
                    "Click OK and confirm with your admin password"
                ],
                "windows": True,
                "linux": False,
                "macos": False
            },
            {
                "id": 5,
                "title": "Enable BitLocker Disk Encryption",
                "description": "Encrypts your entire hard drive, making data inaccessible without the encryption key even if the device is stolen.",
                "priority": "High",
                "difficulty": "Medium",
                "steps": [
                    "Ensure you have a Microsoft account with admin rights",
                    "Open Control Panel > System and Security > BitLocker Drive Encryption",
                    "Click 'Turn on BitLocker'",
                    "Save your recovery key to OneDrive or print it",
                    "Select 'Run BitLocker System Check'",
                    "Allow the drive to finish encryption (can take hours)"
                ],
                "windows": True,
                "linux": False,
                "macos": False
            },
            {
                "id": 6,
                "title": "Set Strong Password Policy",
                "description": "Strong passwords are essential to prevent unauthorized account access. Enforce minimum password complexity and length.",
                "priority": "High",
                "difficulty": "Easy",
                "steps": [
                    "Open Settings > Accounts > Sign-in options",
                    "Under 'Password', click 'Change'",
                    "Create a password with at least 12 characters",
                    "Include uppercase, lowercase, numbers, and special characters",
                    "Avoid using personal information or dictionary words",
                    "For all accounts, follow the same strong password guidelines"
                ],
                "windows": True,
                "linux": True,
                "macos": True
            },
            {
                "id": 7,
                "title": "Disable Unnecessary Services",
                "description": "Disabling unused services reduces attack surface and improves performance by eliminating unnecessary background processes.",
                "priority": "Medium",
                "difficulty": "Hard",
                "steps": [
                    "Press Windows + R and type 'services.msc'",
                    "Review services and identify those not needed",
                    "Right-click on unnecessary services and set to 'Disabled'",
                    "Services to consider disabling: Bluetooth, Fax, HomeGroup",
                    "Do not disable critical services like Windows Update, Firewall, Security"
                ],
                "windows": True,
                "linux": False,
                "macos": False
            },
            {
                "id": 8,
                "title": "Configure Windows Defender Antivirus Scans",
                "description": "Schedule regular automatic scans to proactively detect malware before it causes damage.",
                "priority": "High",
                "difficulty": "Easy",
                "steps": [
                    "Open Windows Security",
                    "Go to 'Virus & threat protection'",
                    "Click 'Manage settings'",
                    "Under 'Scan options', set to 'Full scan'",
                    "Click 'Schedule a scan' and set to weekly",
                    "Ensure 'Quarantine' is set to automatically remove threats"
                ],
                "windows": True,
                "linux": False,
                "macos": False
            },
            {
                "id": 9,
                "title": "Enable Windows Sandbox (Optional)",
                "description": "Windows Sandbox provides an isolated environment to test suspicious files and programs safely.",
                "priority": "Medium",
                "difficulty": "Medium",
                "steps": [
                    "Open Control Panel > Programs > Programs and Features",
                    "Click 'Turn Windows features on or off'",
                    "Check 'Windows Sandbox'",
                    "Click OK and allow the system to install the feature",
                    "Restart your computer",
                    "Search for and open Windows Sandbox to run suspicious programs safely"
                ],
                "windows": True,
                "linux": False,
                "macos": False
            },
            {
                "id": 10,
                "title": "Configure Firewall Rules",
                "description": "Fine-tune firewall rules to allow only necessary connections and block unexpected traffic.",
                "priority": "Medium",
                "difficulty": "Hard",
                "steps": [
                    "Open Windows Defender Firewall > Advanced Settings",
                    "Review inbound and outbound rules",
                    "Block applications you don't recognize or trust",
                    "Create custom rules for applications that need network access",
                    "Enable logging to monitor blocked connections",
                    "Regularly review and clean up unused rules"
                ],
                "windows": True,
                "linux": False,
                "macos": False
            },
            {
                "id": 11,
                "title": "Set Up Automatic Backup",
                "description": "Regular backups ensure you can recover from ransomware attacks, hardware failures, or data loss.",
                "priority": "High",
                "difficulty": "Easy",
                "steps": [
                    "Connect external storage (USB drive or external drive)",
                    "Open Settings > System > Storage > Advanced storage options > Backups",
                    "Click 'Backup now'",
                    "Or use File History for automatic backups",
                    "Configure File History to backup hourly",
                    "Test recovery by restoring a file from backup"
                ],
                "windows": True,
                "linux": True,
                "macos": True
            },
            {
                "id": 12,
                "title": "Enable Secure Boot",
                "description": "Secure Boot prevents unauthorized software from loading during startup, protecting your system from malware.",
                "priority": "High",
                "difficulty": "Hard",
                "steps": [
                    "Restart your computer and enter BIOS/UEFI (usually F2, F10, or Del during startup)",
                    "Navigate to Security settings",
                    "Find 'Secure Boot' option",
                    "Change from 'Disabled' to 'Enabled'",
                    "Save settings and exit BIOS",
                    "Your system will restart with Secure Boot enabled"
                ],
                "windows": True,
                "linux": True,
                "macos": False
            },
            {
                "id": 13,
                "title": "Implement VPN for Remote Connections",
                "description": "VPN encrypts your internet traffic, protecting sensitive data when using public WiFi or remote connections.",
                "priority": "Medium",
                "difficulty": "Medium",
                "steps": [
                    "Evaluate VPN providers (ProtonVPN, ExpressVPN, Mullvad recommended)",
                    "Install the VPN application",
                    "Create an account with a strong password",
                    "Connect to VPN servers (preferably with strong encryption)",
                    "Verify your IP address is masked",
                    "Enable 'Kill Switch' to disconnect if VPN drops"
                ],
                "windows": True,
                "linux": True,
                "macos": True
            },
            {
                "id": 14,
                "title": "Set Up Two-Factor Authentication (2FA)",
                "description": "2FA adds an extra layer of security to your accounts by requiring a second verification method.",
                "priority": "High",
                "difficulty": "Easy",
                "steps": [
                    "Go to your Microsoft Account settings (account.microsoft.com)",
                    "Click 'Security' > 'Advanced security options'",
                    "Under 'Two-step verification', click 'Set up two-step verification'",
                    "Add a phone number or authenticator app",
                    "Confirm with a code sent to your registered device",
                    "Repeat for other important accounts (email, cloud storage, banking)"
                ],
                "windows": True,
                "linux": True,
                "macos": True
            },
            {
                "id": 15,
                "title": "Configure Browser Security",
                "description": "Harden your web browser to protect against phishing, malicious sites, and tracking.",
                "priority": "Medium",
                "difficulty": "Easy",
                "steps": [
                    "Install uBlock Origin and uMatrix extensions",
                    "Enable 'Enhanced Tracking Protection' (Firefox) or 'Enhanced Protection' (Chrome)",
                    "Disable third-party cookies",
                    "Enable HTTPS-only mode",
                    "Keep browser updated to the latest version",
                    "Avoid installing unnecessary browser extensions"
                ],
                "windows": True,
                "linux": True,
                "macos": True
            },
            {
                "id": 16,
                "title": "Review and Restrict User Permissions",
                "description": "Limit user account privileges to reduce the impact of compromised accounts.",
                "priority": "Medium",
                "difficulty": "Medium",
                "steps": [
                    "Open Settings > Accounts > Other users",
                    "Review all user accounts on your system",
                    "Convert unnecessary admin accounts to standard users",
                    "Remove accounts that are no longer in use",
                    "Set strong password policies for all accounts",
                    "Enable password expiration policies"
                ],
                "windows": True,
                "linux": True,
                "macos": True
            },
            {
                "id": 17,
                "title": "Monitor Network Connections",
                "description": "Regularly check network activity to detect unauthorized connections or suspicious traffic.",
                "priority": "Medium",
                "difficulty": "Hard",
                "steps": [
                    "Open Task Manager > Performance > Open Resource Monitor",
                    "Go to Network tab to see active connections",
                    "Check for unfamiliar IP addresses or domains",
                    "Use 'netstat -an' in Command Prompt to view all connections",
                    "Cross-reference with installed applications",
                    "Block suspicious connections in your firewall"
                ],
                "windows": True,
                "linux": True,
                "macos": True
            },
            {
                "id": 18,
                "title": "Harden SSH Configuration (Linux/macOS)",
                "description": "SSH hardening reduces risk of unauthorized remote access.",
                "priority": "High",
                "difficulty": "Hard",
                "steps": [
                    "Edit /etc/ssh/sshd_config with root privileges",
                    "Set 'PermitRootLogin no' to disable root login",
                    "Set 'PasswordAuthentication no' to use keys only",
                    "Change default port 22 to a non-standard port",
                    "Enable 'PubkeyAuthentication yes'",
                    "Restart SSH service: sudo service ssh restart"
                ],
                "windows": False,
                "linux": True,
                "macos": True
            },
            {
                "id": 19,
                "title": "Implement Host-Based Firewall (Linux)",
                "description": "UFW provides an easy-to-use firewall interface for managing network security rules.",
                "priority": "High",
                "difficulty": "Medium",
                "steps": [
                    "Install UFW: sudo apt-get install ufw",
                    "Enable UFW: sudo ufw enable",
                    "Set default policies: sudo ufw default deny incoming",
                    "Allow SSH: sudo ufw allow 22/tcp",
                    "Allow HTTP/HTTPS: sudo ufw allow 80/tcp && sudo ufw allow 443/tcp",
                    "View status: sudo ufw status"
                ],
                "windows": False,
                "linux": True,
                "macos": False
            },
            {
                "id": 20,
                "title": "Keep Software Up to Date",
                "description": "Regular software updates patch security vulnerabilities and ensure you have the latest protections.",
                "priority": "High",
                "difficulty": "Easy",
                "steps": [
                    "Enable automatic updates for your OS",
                    "Regularly check manufacturer websites for driver updates",
                    "Keep all applications updated (browsers, office, antivirus)",
                    "Remove outdated or unsupported software",
                    "Use package managers to simplify updates on Linux",
                    "Create a calendar reminder for monthly security patches"
                ],
                "windows": True,
                "linux": True,
                "macos": True
            }
        ]
    
    def get_all_steps(self) -> List[Dict[str, Any]]:
        """Get all hardening steps"""
        return self.steps
    
    def get_critical_steps(self) -> List[Dict[str, Any]]:
        """Get only critical priority steps"""
        return [s for s in self.steps if s["priority"] == "Critical"]
    
    def get_steps_by_os(self, os_type: str) -> List[Dict[str, Any]]:
        """Get hardening steps for specific OS"""
        os_key = os_type.lower()
        if os_type == "Windows":
            return [s for s in self.steps if s.get("windows", False)]
        elif os_type == "Linux":
            return [s for s in self.steps if s.get("linux", False)]
        elif os_type == "Darwin":  # macOS
            return [s for s in self.steps if s.get("macos", False)]
        return self.steps
    
    def get_steps_by_difficulty(self, difficulty: str) -> List[Dict[str, Any]]:
        """Get hardening steps by difficulty level"""
        return [s for s in self.steps if s["difficulty"] == difficulty]
    
    def get_step_by_id(self, step_id: int) -> Dict[str, Any]:
        """Get specific hardening step by ID"""
        for step in self.steps:
            if step["id"] == step_id:
                return step
        return None
    
    def estimate_security_improvement(self, completed_steps: List[int]) -> Dict[str, Any]:
        """Estimate security score improvement from completed steps"""
        improvement = {
            "critical_completed": 0,
            "high_completed": 0,
            "medium_completed": 0,
            "estimated_score_increase": 0
        }
        
        for step_id in completed_steps:
            step = self.get_step_by_id(step_id)
            if step:
                if step["priority"] == "Critical":
                    improvement["critical_completed"] += 1
                    improvement["estimated_score_increase"] += 8
                elif step["priority"] == "High":
                    improvement["high_completed"] += 1
                    improvement["estimated_score_increase"] += 5
                else:
                    improvement["medium_completed"] += 1
                    improvement["estimated_score_increase"] += 3
        
        return improvement
