"""
Configuration Module
Application settings and constants
"""

# Application Information
APP_NAME = "OS Security Posture Monitor"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Security Team"

# UI Configuration
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
WINDOW_MIN_WIDTH = 1000
WINDOW_MIN_HEIGHT = 700

# Color Scheme
COLORS = {
    "primary": "#1e3a5f",
    "secondary": "#2196F3",
    "success": "#4CAF50",
    "warning": "#FF9800",
    "danger": "#f44336",
    "light_bg": "#f5f5f5",
    "dark_bg": "#1e3a5f",
    "text_primary": "#212121",
    "text_secondary": "#666666",
    "border": "#e0e0e0"
}

# Threat Levels
THREAT_LEVELS = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3
}

# Security Thresholds
SECURITY_SCORE_CRITICAL = 30
SECURITY_SCORE_HIGH = 60
SECURITY_SCORE_MEDIUM = 80

# Scan Settings
SCAN_TIMEOUT = 60  # seconds
AUTO_SCAN_INTERVAL = 86400  # 24 hours in seconds

# API Endpoints (for future cloud integration)
API_BASE_URL = "https://api.securitymonitor.local"
API_VERSION = "v1"

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FILE = "security_monitor.log"
LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB

# Database
DATABASE_FILE = "security_data.db"

# Supported Platforms
SUPPORTED_OS = ["Windows", "Linux", "Darwin"]  # Darwin is macOS

# Security Categories
SECURITY_CATEGORIES = [
    "Firewall",
    "Antivirus",
    "Updates",
    "User Accounts",
    "Network Security",
    "Encryption",
    "Access Control",
    "Audit & Logging"
]

# Priority Levels
PRIORITY_LEVELS = ["Critical", "High", "Medium", "Low"]

# Difficulty Levels
DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard"]

# Font Settings
FONTS = {
    "header": ("Arial", 24, "Bold"),
    "title": ("Arial", 14, "Bold"),
    "subtitle": ("Arial", 12, "Bold"),
    "body": ("Arial", 11),
    "small": ("Arial", 10),
    "label": ("Arial", 9)
}

# Paths
CONFIG_DIR = "~/.security_monitor"
DATA_DIR = "~/.security_monitor/data"
REPORTS_DIR = "~/.security_monitor/reports"

# Email Notifications (optional)
EMAIL_NOTIFICATIONS_ENABLED = False
NOTIFICATION_EMAIL = ""
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Windows-specific settings
WINDOWS_DEFENDER_PATH = "C:\\Program Files\\Windows Defender"
BITLOCKER_DRIVE = "C:"

# Linux-specific settings
LINUX_AUDIT_PATH = "/var/log/audit"
LINUX_SECURE_LEVEL = "/proc/sys/kernel/sysrq"

# macOS-specific settings
MACOS_GATEKEEPER_ENABLED = True
MACOS_SIP_ENABLED = True

# Features
FEATURES = {
    "dashboard": True,
    "detailed_scan": True,
    "hardening_guide": True,
    "auto_scan": True,
    "notifications": True,
    "reporting": True,
    "cloud_sync": False,  # For future use
    "ai_recommendations": False  # For future use
}

# Report Format Options
REPORT_FORMATS = ["JSON", "PDF", "CSV"]

# Hardening Steps Configuration
HARDENING_CONFIG = {
    "show_critical_first": True,
    "auto_prioritize": True,
    "implementation_tracking": True,
    "step_completion_notifications": True
}

# Security Standards
SECURITY_STANDARDS = {
    "CIS": "CIS Microsoft Windows 10 Enterprise Release 1909 Benchmark",
    "NIST": "NIST Cybersecurity Framework",
    "ISO": "ISO/IEC 27001 Information Security Management"
}
