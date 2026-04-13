import subprocess
import platform
import re
import os
import ctypes

class SecurityScanner:
    def __init__(self):
        self.is_admin = self._check_admin()

    def _check_admin(self) -> bool:
        """Check if the script is running with administrative privileges."""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False

    def _run_ps(self, command: str, timeout: int = 15) -> str:
        """Runs a PowerShell command with a strict timeout to prevent freezing."""
        try:
            # Proper way to hide PowerShell window on Windows without deadlock
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            
            result = subprocess.run(
                [
                    "powershell", 
                    "-NoProfile", 
                    "-ExecutionPolicy", "Bypass", 
                    "-Command", command
                ],
                capture_output=True,
                text=True,
                timeout=timeout,
                startupinfo=startupinfo,
                check=False
            )
            return result.stdout.strip().lower()
        except subprocess.TimeoutExpired:
            print(f"Command timed out after {timeout}s: {command}")
            return "timeout"
        except Exception as e:
            print(f"PowerShell Error: {e}")
            return ""

    def get_security_status(self) -> dict:
        """Gathers all security metrics."""
        if not self.is_admin:
            return {
                "antivirus": {"text": "Unknown", "desc": "Needs Admin Mode", "status": "warning"},
                "firewall": {"text": "Unknown", "desc": "Needs Admin Mode", "status": "warning"},
                "bitlocker": {"text": "Unknown", "desc": "Needs Admin Mode", "status": "warning"},
                "tpm": {"text": "Unknown", "desc": "Needs Admin Mode", "status": "warning"},
                "secure_boot": {"text": "Unknown", "desc": "Needs Admin Mode", "status": "warning"}
            }

        return {
            "antivirus": self._check_antivirus(),
            "firewall": self._check_firewall(),
            "bitlocker": self._check_bitlocker(),
            "tpm": self._check_tpm(),
            "secure_boot": self._check_secure_boot()
        }

    def _check_antivirus(self) -> dict:
        cmd = "Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntiVirusProduct | Select-Object -ExpandProperty displayName"
        out = self._run_ps(cmd)
        if out:
            return {"text": "Active", "desc": out.title(), "status": "secure"}
        return {"text": "At Risk", "desc": "No AV detected", "status": "danger"}

    def _check_firewall(self) -> dict:
        cmd = "Get-NetFirewallProfile | Select-Object -ExpandProperty Enabled"
        out = self._run_ps(cmd)
        if "true" in out:
            return {"text": "Enabled", "desc": "Network protected", "status": "secure"}
        return {"text": "Disabled", "desc": "Firewall is OFF", "status": "danger"}

    def _check_bitlocker(self) -> dict:
        cmd = "Get-BitLockerVolume -MountPoint 'C:' | Select-Object -ExpandProperty ProtectionStatus"
        out = self._run_ps(cmd)
        if "on" in out or "1" in out:
            return {"text": "Encrypted", "desc": "Drive C: Protected", "status": "secure"}
        return {"text": "Decrypted", "desc": "No Encryption", "status": "danger"}

    def _check_tpm(self) -> dict:
        cmd = "Get-Tpm | Select-Object -ExpandProperty TpmPresent"
        out = self._run_ps(cmd)
        if "true" in out:
            return {"text": "Present", "desc": "TPM 2.0/1.2 Active", "status": "secure"}
        return {"text": "Missing", "desc": "TPM not found", "status": "danger"}

    def _check_secure_boot(self) -> dict:
        cmd = "Confirm-SecureBootUEFI"
        out = self._run_ps(cmd)
        if "true" in out:
            return {"text": "Enabled", "desc": "UEFI Secure Boot", "status": "secure"}
        return {"text": "Disabled", "desc": "Secure Boot OFF", "status": "danger"}

    def _check_updates(self) -> dict:
        """Check for pending Windows updates."""
        cmd = "$(New-Object -ComObject Microsoft.Update.AutoUpdate).Results.LastSuccessfulSearchTime | Out-String"
        out = self._run_ps(cmd, timeout=20)
        if out and out != "timeout":
            return {"text": "Up to Date", "desc": "System is current", "status": "secure"}
        return {"text": "Pending", "desc": "Updates may be available", "status": "warning"}

    def _check_user_accounts(self) -> dict:
        """Check User Account Control (UAC) status."""
        cmd = "Get-ItemProperty -Path 'HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Name 'EnableLUA' | Select-Object -ExpandProperty EnableLUA"
        out = self._run_ps(cmd)
        if "1" in out or "true" in out:
            return {"text": "Enabled", "desc": "UAC protection active", "status": "secure"}
        return {"text": "Disabled", "desc": "UAC is OFF", "status": "danger"}

    def _check_network_settings(self) -> dict:
        """Check network profile security."""
        cmd = "Get-NetConnectionProfile | Select-Object -ExpandProperty NetworkCategory"
        out = self._run_ps(cmd)
        if "private" in out:
            return {"text": "Private", "desc": "Network is Private", "status": "secure"}
        elif "public" in out:
            return {"text": "Public", "desc": "Network is Public", "status": "warning"}
        return {"text": "Unknown", "desc": "Could not determine network type", "status": "neutral"}

    def run_full_scan(self) -> dict:
        """Main scan interface - returns data in UI-compatible format."""
        # Get all security checks
        raw = self.get_security_status()
        
        # Add the new checks to raw data
        if self.is_admin:
            raw["updates"] = self._check_updates()
            raw["user_accounts"] = self._check_user_accounts()
            raw["network"] = self._check_network_settings()
        else:
            raw["updates"] = {"text": "Unknown", "desc": "Needs Admin", "status": "warning"}
            raw["user_accounts"] = {"text": "Unknown", "desc": "Needs Admin", "status": "warning"}
            raw["network"] = {"text": "Unknown", "desc": "Needs Admin", "status": "warning"}
        
        # Map security checks to UI category names
        mapping = {
            "antivirus": "Antivirus",
            "firewall": "Firewall",
            "bitlocker": "Encryption",
            "updates": "Updates",
            "user_accounts": "User Accounts",
            "network": "Network Security",
        }
        
        # Transform the data
        issues = []
        score = 100
        formatted = {}
        
        for key, label in mapping.items():
            if key not in raw:
                continue
            check = raw[key]
            status = check.get("status", "neutral")
            text = check.get("text", "Unknown")
            
            # Map status to standardized format
            if status == "secure":
                formatted[label] = {"status": "Enabled"}
            elif status == "danger":
                formatted[label] = {"status": "Disabled"}
                issues.append({
                    "title": f"{label}: {text}",
                    "severity": "critical",
                    "recommendation": check.get("desc", "")
                })
                score -= 15
            elif status == "warning":
                formatted[label] = {"status": "Warning"}
                issues.append({
                    "title": f"{label}: {text}",
                    "severity": "high",
                    "recommendation": check.get("desc", "")
                })
                score -= 8
            else:
                formatted[label] = {"status": "Unknown"}
        
        return {
            "overall_score": max(0, score),
            "timestamp": __import__("datetime").datetime.now().isoformat(),
            "Antivirus": formatted.get("Antivirus", {"status": "Unknown"}),
            "Firewall": formatted.get("Firewall", {"status": "Unknown"}),
            "Encryption": formatted.get("Encryption", {"status": "Unknown"}),
            "Updates": formatted.get("Updates", {"status": "Unknown"}),
            "User Accounts": formatted.get("User Accounts", {"status": "Unknown"}),
            "Network Security": formatted.get("Network Security", {"status": "Unknown"}),
            "issues": issues,
            "categories": formatted
        }