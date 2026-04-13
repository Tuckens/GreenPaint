"""
OS Security Posture Monitor - Main Application
"""

import sys
import json
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QScrollArea, QPushButton, QLabel,
    QFrame, QGridLayout, QListWidget, QListWidgetItem, QDialog,
    QTextEdit, QMessageBox
)
from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtGui import QColor, QFont, QIcon

from security_scanner import SecurityScanner
from hardening_steps import HardeningSteps
from ui_components import SecurityCard, HardeningCard


# ── Background scanner thread ─────────────────────────────────────────────────

class ScannerThread(QThread):
    scan_complete  = Signal(dict)
    progress_update = Signal(str)

    def __init__(self):
        super().__init__()
        self.scanner = SecurityScanner()

    def run(self):
        self.progress_update.emit("Starting security scan...")
        try:
            self.scan_complete.emit(self.scanner.run_full_scan())
        except Exception as e:
            self.progress_update.emit(f"Scan error: {e}")


# ── Mappings ──────────────────────────────────────────────────────────────────

_CATEGORY_TO_STATUS_ROW = {
    "Firewall":         "Windows Firewall",
    "Antivirus":        "Antivirus / Antimalware",
    "Updates":          "Windows Updates",
    "User Accounts":    "User Account Control",
    "Encryption":       "Disk Encryption",
    "Network Security": "Network Settings",
}

_STATUS_EXPLANATIONS = {
    "Enabled":         "Enabled — properly configured",
    "Running":         "Running — protection is active",
    "Up to Date":      "Up to Date — no pending patches",
    "Secure":          "Secure — settings look good",
    "Disabled":        "Disabled — action required",
    "Pending Updates": "Pending Updates — install soon",
    "Not Available":   "Not Available — feature not present on this edition",
    "Review Needed": (
        "Review Needed — network profile is Public. "
        "Switch to Private: Settings › Network & Internet › your connection › Network profile."
    ),
    "Unknown":         "Unknown — check inconclusive (may need admin rights)",
}

# ── Tiny UI helpers ───────────────────────────────────────────────────────────

def _lbl(text, size=11, bold=False, color="#212121", wrap=False):
    w = QLabel(text)
    w.setFont(QFont("Segoe UI", size, QFont.Bold if bold else QFont.Normal))
    w.setStyleSheet(f"color: {color}; background: transparent;")
    if wrap:
        w.setWordWrap(True)
    return w


def _section_title(text):
    return _lbl(text, size=13, bold=True, color="#1e3a5f")


def _btn(text, bg="#2196F3", hover=None, min_width=0):
    hover = hover or bg
    b = QPushButton(text)
    s = f"""
        QPushButton {{
            background-color: {bg};
            color: #ffffff;
            border: none;
            padding: 8px 18px;
            border-radius: 5px;
            font-size: 11px;
            font-weight: bold;
            font-family: 'Segoe UI';
            {"min-width: " + str(min_width) + "px;" if min_width else ""}
        }}
        QPushButton:hover   {{ background-color: {hover}; }}
        QPushButton:pressed {{ background-color: {hover}; }}
    """
    b.setStyleSheet(s)
    return b


# ── Main window ───────────────────────────────────────────────────────────────

class SecurityDashboardApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("GreenPaint ©")
        
        # Load custom icon for Windows taskbar
        icon_path = self._find_icon_path()
        if icon_path and icon_path.exists():
            try:
                self.setWindowIcon(QIcon(str(icon_path)))
            except Exception:
                pass
        
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1000, 700)

        self.security_data  = {}
        self.hardening_steps = HardeningSteps()
        self._auto_scan_enabled = True

        self._apply_global_stylesheet()
        self.setup_ui()
        self.start_scan()

    def _find_icon_path(self):
        """Find the icon file in application or script directory."""
        icon_name = "greenpaint.ico"
        
        # If running as PyInstaller bundle (--onefile), use sys._MEIPASS
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            meipass_icon = Path(sys._MEIPASS) / icon_name
            if meipass_icon.exists():
                return meipass_icon
        
        # If running as PyInstaller bundle (--onedir), check the _internal folder
        if getattr(sys, 'frozen', False):
            bundle_dir = Path(sys.executable).parent
            
            # Check _internal folder (used by --onedir)
            internal_icon = bundle_dir / "_internal" / icon_name
            if internal_icon.exists():
                return internal_icon
            
            # Check bundle root directory
            icon_path = bundle_dir / icon_name
            if icon_path.exists():
                return icon_path
        
        # Check current working directory
        cwd_icon = Path.cwd() / icon_name
        if cwd_icon.exists():
            return cwd_icon
        
        # Check script directory
        script_dir = Path(__file__).parent
        script_icon = script_dir / icon_name
        if script_icon.exists():
            return script_icon
        
        return None

    # ── Global stylesheet ─────────────────────────────────────────────────────

    def _apply_global_stylesheet(self):
        self.setStyleSheet("""
            QMainWindow, QWidget, QDialog {
                background-color: #f8f9fa;
                color: #212121;
                font-family: 'Segoe UI';
                font-size: 11px;
            }
            QLabel  { color: #212121; background: transparent; }
            QScrollArea { border: none; background-color: #f8f9fa; }
            QScrollArea > QWidget > QWidget { background-color: #f8f9fa; }
            QListWidget {
                border: 1px solid #dee2e6;
                border-radius: 6px;
                background-color: #ffffff;
                color: #212121;
            }
            QListWidget::item          { padding: 6px 10px; color: #212121; }
            QListWidget::item:selected { background-color: #e3f2fd; color: #212121; }
            QTabWidget::pane {
                border: 1px solid #dee2e6;
                border-radius: 0 6px 6px 6px;
                background-color: #ffffff;
            }
            QTabBar { background: transparent; }
            QTabBar::tab {
                background-color: #e9ecef;
                color: #495057;
                border: 1px solid #dee2e6;
                border-bottom: none;
                padding: 10px 22px;
                margin-right: 3px;
                border-radius: 6px 6px 0 0;
                font-size: 11px;
                font-weight: 600;
                min-width: 140px;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                color: #1e3a5f;
                border-bottom: 3px solid #2196F3;
            }
            QTabBar::tab:hover:!selected { background-color: #dde8f5; color: #1e3a5f; }
            QStatusBar { color: #495057; font-size: 10px; }
            QTextEdit  {
                color: #212121; background-color: #ffffff;
                border: 1px solid #dee2e6; border-radius: 4px; font-size: 11px;
            }
            QFrame { color: #212121; }
        """)

    # ── UI scaffold ───────────────────────────────────────────────────────────

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(20, 20, 20, 10)
        root.setSpacing(16)
        root.addWidget(self._build_header())

        tabs = QTabWidget()
        tabs.addTab(self._build_dashboard_tab(),  "Dashboard")
        tabs.addTab(self._build_status_tab(),     "Security Status")
        tabs.addTab(self._build_hardening_tab(),  "Hardening Guide")
        tabs.addTab(self._build_settings_tab(),   "Settings")
        root.addWidget(tabs)

        self.statusBar().showMessage("Ready")

    # ── Header ────────────────────────────────────────────────────────────────

    def _build_header(self):
        header = QFrame()
        header.setStyleSheet("""
            QFrame { background-color: #1e3a5f; border-radius: 8px; }
            QLabel { color: #ffffff; background: transparent; }
        """)
        lay = QHBoxLayout(header)
        lay.setContentsMargins(20, 14, 20, 14)
        title = QLabel("🔒  OS Security Posture Monitor")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        lay.addWidget(title)
        lay.addStretch()
        self.score_label = QLabel("Security Score: —")
        self.score_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.score_label.setStyleSheet("color: #FFD700; background: transparent;")
        lay.addWidget(self.score_label)
        lay.addSpacing(16)
        refresh = _btn("🔄  Refresh Scan", bg="#4CAF50", hover="#388E3C")
        refresh.clicked.connect(self.start_scan)
        lay.addWidget(refresh)
        return header

    # ── Dashboard tab ─────────────────────────────────────────────────────────

    def _build_dashboard_tab(self):
        outer, slay = self._scrollable_tab()
        slay.addWidget(_section_title("Security Overview"))

        grid = QGridLayout()
        grid.setSpacing(12)
        self.security_cards = {}
        for idx, (key, label) in enumerate([
            ("Firewall",         "🔥  Firewall"),
            ("Antivirus",        "🛡  Antivirus"),
            ("Updates",          "📦  Updates"),
            ("User Accounts",    "👤  User Accounts"),
            ("Network Security", "🌐  Network Security"),
            ("Encryption",       "🔐  Encryption"),
        ]):
            card = SecurityCard(label, "Scanning...", "warning")
            self.security_cards[key] = card
            grid.addWidget(card, idx // 3, idx % 3)
        slay.addLayout(grid)

        slay.addSpacing(8)
        slay.addWidget(_section_title("Recent Security Issues"))
        self.issues_list = QListWidget()
        self.issues_list.setFixedHeight(180)
        slay.addWidget(self.issues_list)
        slay.addStretch()
        return outer

    # ── Security Status tab ───────────────────────────────────────────────────

    def _build_status_tab(self):
        outer = QWidget()
        outer.setStyleSheet("background-color: #ffffff;")
        lay = QVBoxLayout(outer)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(10)
        lay.addWidget(_lbl(
            "Detailed breakdown of each security check. "
            "Rows update automatically after every scan.",
            size=10, color="#6c757d", wrap=True
        ))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        inner = QWidget()
        inner.setStyleSheet("background-color: #ffffff;")
        slay = QVBoxLayout(inner)
        slay.setSpacing(8)

        self.status_items = {}
        for name in [
            "Windows Firewall",
            "Antivirus / Antimalware",
            "Windows Updates",
            "User Account Control",
            "Secure Boot",
            "TPM 2.0",
            "Disk Encryption",
            "Network Settings",
        ]:
            frame = QFrame()
            frame.setStyleSheet("""
                QFrame { background-color: #f8f9fa; border-radius: 6px;
                         border-left: 4px solid #adb5bd; }
                QLabel { color: #212121; background: transparent; }
            """)
            row = QHBoxLayout(frame)
            row.setContentsMargins(14, 12, 14, 12)
            name_lbl = _lbl(name, size=11, bold=True)
            name_lbl.setMinimumWidth(230)
            row.addWidget(name_lbl)
            row.addStretch()
            status_lbl = _lbl("Scanning...", size=10, color="#6c757d", wrap=True)
            status_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            row.addWidget(status_lbl)
            slay.addWidget(frame)
            self.status_items[name] = (frame, status_lbl)

        slay.addStretch()
        scroll.setWidget(inner)
        lay.addWidget(scroll)
        return outer

    # ── Hardening Guide tab ───────────────────────────────────────────────────

    def _build_hardening_tab(self):
        outer, slay = self._scrollable_tab()
        slay.addWidget(_section_title("Security Hardening Guide"))

        self.hardening_items = []
        for step in self.hardening_steps.get_all_steps():
            card = HardeningCard(
                step["title"],
                step["description"],
                step["priority"],
                step.get("difficulty", "Medium"),
            )
            # FIX: implement_clicked is a Signal() with no arguments.
            # Previously connected as lambda checked, s=step: ... which
            # expected a 'checked' bool argument that Signal() never sends.
            # Use a zero-argument lambda instead.
            card.implement_clicked.connect(
                lambda s=step: self._show_guide(s)
            )
            # FIX: wire up the "Learn More" button too (was previously unconnected)
            card.learn_more_clicked.connect(
                lambda s=step: self._show_guide(s)
            )
            slay.addWidget(card)
            self.hardening_items.append(card)

        slay.addStretch()
        return outer

    # ── Settings tab ──────────────────────────────────────────────────────────

    def _build_settings_tab(self):
        outer = QWidget()
        outer.setStyleSheet("background-color: #ffffff;")
        lay = QVBoxLayout(outer)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(14)
        lay.addWidget(_section_title("Settings & Preferences"))

        # ── auto-scan toggle ──
        row_frame = QFrame()
        row_frame.setStyleSheet("""
            QFrame { background-color: #f8f9fa; border-radius: 6px; }
            QLabel { color: #212121; background: transparent; }
        """)
        row = QHBoxLayout(row_frame)
        row.setContentsMargins(16, 12, 16, 12)
        row.addWidget(_lbl("Enable automatic security scans every 24 hours", size=11))
        row.addStretch()

        # FIX: toggle actually changes label + colour when clicked
        self._toggle_btn = QPushButton("Enabled")
        self._toggle_btn.setCheckable(True)
        self._toggle_btn.setChecked(True)
        self._toggle_btn.clicked.connect(self._on_toggle_autoscan)
        self._style_toggle(True)
        row.addWidget(self._toggle_btn)
        lay.addWidget(row_frame)

        export = _btn("📊  Export Security Report", bg="#2196F3", hover="#1565C0")
        export.clicked.connect(self.export_report)
        lay.addWidget(export)
        lay.addStretch()
        return outer

    def _style_toggle(self, enabled: bool):
        if enabled:
            self._toggle_btn.setText("Enabled")
            self._toggle_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50; color: #ffffff;
                    border: none; padding: 8px 18px; border-radius: 5px;
                    font-size: 11px; font-weight: bold; min-width: 90px;
                }
                QPushButton:hover { background-color: #388E3C; }
            """)
        else:
            self._toggle_btn.setText("Disabled")
            self._toggle_btn.setStyleSheet("""
                QPushButton {
                    background-color: #9e9e9e; color: #ffffff;
                    border: none; padding: 8px 18px; border-radius: 5px;
                    font-size: 11px; font-weight: bold; min-width: 90px;
                }
                QPushButton:hover { background-color: #616161; }
            """)

    def _on_toggle_autoscan(self, checked: bool):
        self._auto_scan_enabled = checked
        self._style_toggle(checked)

    # ── Scan orchestration ────────────────────────────────────────────────────

    def start_scan(self):
        self.statusBar().showMessage("Scanning system security...")
        self.scan_thread = ScannerThread()
        self.scan_thread.scan_complete.connect(self._on_scan_complete)
        self.scan_thread.progress_update.connect(self.statusBar().showMessage)
        self.scan_thread.start()

    def _on_scan_complete(self, results):
        self.security_data = results
        self._update_dashboard(results)
        self._update_status_tab(results)
        self.statusBar().showMessage("Security scan complete")

    def _update_dashboard(self, data):
        score = data.get("overall_score", 0)
        self.score_label.setText(f"Security Score: {score}/100")

        for key, card in self.security_cards.items():
            if key in data:
                status = data[key].get("status", "Unknown")
                if status in ("Enabled", "Running", "Up to Date", "Secure"):
                    sev = "success"
                elif status == "Disabled":
                    sev = "critical"
                else:
                    sev = "warning"
                card.update_status(status, sev)

        self.issues_list.clear()
        for issue in data.get("issues", []):
            item = QListWidgetItem(f"  {issue['title']}")
            sev = issue.get("severity", "")
            if sev == "critical":
                item.setBackground(QColor("#ffcdd2"))
                item.setForeground(QColor("#b71c1c"))
            elif sev == "high":
                item.setBackground(QColor("#ffe0b2"))
                item.setForeground(QColor("#e65100"))
            else:
                item.setForeground(QColor("#212121"))
            self.issues_list.addItem(item)

    def _update_status_tab(self, data):
        border = {"success": "#4CAF50", "warning": "#FF9800",
                  "critical": "#f44336", "neutral": "#adb5bd"}
        text   = {"success": "#1b5e20", "warning": "#e65100",
                  "critical": "#b71c1c", "neutral": "#495057"}

        for cat_key, row_name in _CATEGORY_TO_STATUS_ROW.items():
            if row_name not in self.status_items:
                continue
            frame, lbl = self.status_items[row_name]
            raw = data.get(cat_key, {}).get("status", "Unknown") \
                  if cat_key in data else "Unknown"

            if raw in ("Enabled", "Running", "Up to Date", "Secure"):
                bucket = "success"
            elif raw == "Disabled":
                bucket = "critical"
            elif raw == "Pending Updates":
                bucket = "warning"
            else:
                bucket = "neutral"

            lbl.setText(_STATUS_EXPLANATIONS.get(raw, raw))
            lbl.setStyleSheet(f"color: {text[bucket]}; background: transparent;")
            frame.setStyleSheet(f"""
                QFrame {{
                    background-color: #f8f9fa; border-radius: 6px;
                    border-left: 4px solid {border[bucket]};
                }}
                QLabel {{ color: #212121; background: transparent; }}
            """)

        # FIX: Secure Boot and TPM 2.0 were stuck on "Scanning..." because
        # they have no matching key in _CATEGORY_TO_STATUS_ROW — the scanner
        # never checks them. Show an honest message instead.
        for row_name in ("Secure Boot", "TPM 2.0"):
            if row_name in self.status_items:
                frame, lbl = self.status_items[row_name]
                lbl.setText("Not checked — requires WMI query (run as Administrator)")
                lbl.setStyleSheet("color: #6c757d; background: transparent;")
                frame.setStyleSheet("""
                    QFrame { background-color: #f8f9fa; border-radius: 6px;
                             border-left: 4px solid #adb5bd; }
                    QLabel { color: #212121; background: transparent; }
                """)

    # ── Implementation guide dialog ───────────────────────────────────────────

    def _show_guide(self, step):
        dlg = QDialog(self)
        dlg.setWindowTitle(f"Implement: {step['title']}")
        dlg.setMinimumSize(620, 500)
        dlg.setStyleSheet("""
            QDialog  { background-color: #ffffff; }
            QLabel   { color: #212121; background: transparent; }
            QTextEdit { color: #212121; background-color: #ffffff;
                        border: 1px solid #dee2e6; border-radius: 4px; }
        """)
        lay = QVBoxLayout(dlg)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(12)

        lay.addWidget(_lbl(step["title"], size=14, bold=True, color="#1e3a5f"))

        # Priority + difficulty badges
        badge_row = QHBoxLayout()
        for text, bg in [
            (f"Priority: {step['priority']}",          "#1e3a5f"),
            (f"Difficulty: {step.get('difficulty','Medium')}", "#546e7a"),
        ]:
            b = QLabel(f"  {text}  ")
            b.setFont(QFont("Segoe UI", 9, QFont.Bold))
            b.setStyleSheet(
                f"color: #ffffff; background-color: {bg}; "
                "padding: 4px 10px; border-radius: 4px;"
            )
            badge_row.addWidget(b)
        badge_row.addStretch()
        lay.addLayout(badge_row)

        content = QTextEdit()
        content.setReadOnly(True)
        body = f"Description:\n{step['description']}\n\nSteps to Implement:\n"
        for i, action in enumerate(step.get("steps", []), 1):
            body += f"  {i}. {action}\n"
        content.setPlainText(body)
        lay.addWidget(content)

        close = _btn("Close", bg="#546e7a", hover="#37474f")
        close.clicked.connect(dlg.close)
        lay.addWidget(close, alignment=Qt.AlignRight)
        dlg.exec()

    # ── Export ────────────────────────────────────────────────────────────────

    def export_report(self):
        report = {
            "overall_score":  self.security_data.get("overall_score", 0),
            "scan_timestamp": self.security_data.get("timestamp", ""),
            "categories":     self.security_data.get("categories", {}),
            "issues":         self.security_data.get("issues", []),
        }
        path = Path("security_report.json")
        with open(path, "w") as f:
            json.dump(report, f, indent=2)
        QMessageBox.information(
            self, "Export Successful",
            f"Report saved to:\n{path.absolute()}"
        )

    # ── Utilities ─────────────────────────────────────────────────────────────

    @staticmethod
    def _scrollable_tab():
        """Return (outer_widget, inner_vbox_layout) for a scrollable tab."""
        outer = QWidget()
        outer.setStyleSheet("background-color: #ffffff;")
        lay = QVBoxLayout(outer)
        lay.setContentsMargins(16, 16, 16, 16)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        inner = QWidget()
        inner.setStyleSheet("background-color: #ffffff;")
        slay = QVBoxLayout(inner)
        slay.setSpacing(12)

        scroll.setWidget(inner)
        lay.addWidget(scroll)
        return outer, slay


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    app = QApplication(sys.argv)
    win = SecurityDashboardApp()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()