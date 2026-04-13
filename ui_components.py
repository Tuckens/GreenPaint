"""
UI Components Module — reusable widgets for the security application.
Every widget sets text colour explicitly to avoid inheriting near-invisible
values from the Windows system palette.
"""

from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QProgressBar
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


# ── helpers ───────────────────────────────────────────────────────────────────

def _lbl(text, size=11, bold=False, color="#212121", wrap=False):
    w = QLabel(text)
    w.setFont(QFont("Segoe UI", size, QFont.Bold if bold else QFont.Normal))
    w.setStyleSheet(f"color: {color}; background: transparent;")
    if wrap:
        w.setWordWrap(True)
    return w


def _action_btn(text, bg, hover):
    b = QPushButton(text)
    b.setStyleSheet(f"""
        QPushButton {{
            background-color: {bg};
            color: #ffffff;
            border: none;
            padding: 7px 14px;
            border-radius: 4px;
            font-size: 10px;
            font-weight: bold;
            font-family: 'Segoe UI';
        }}
        QPushButton:hover   {{ background-color: {hover}; }}
        QPushButton:pressed {{ background-color: {hover}; }}
    """)
    return b


# ── SecurityCard ──────────────────────────────────────────────────────────────

class SecurityCard(QFrame):
    """Dashboard summary card for a single security category."""

    _SEV_COLOR = {"success": "#4CAF50", "warning": "#FF9800", "critical": "#f44336"}

    def __init__(self, title: str, status: str, severity: str = "warning"):
        super().__init__()
        self._severity = severity
        self._apply_frame_style()

        lay = QVBoxLayout(self)
        lay.setContentsMargins(14, 14, 14, 14)
        lay.setSpacing(8)

        self._title_lbl  = _lbl(title,  size=11, bold=True, color="#1e3a5f")
        self._status_lbl = _lbl(status, size=10,
                                color=self._SEV_COLOR.get(severity, "#757575"))
        lay.addWidget(self._title_lbl)
        lay.addWidget(self._status_lbl)

    def _apply_frame_style(self):
        c = self._SEV_COLOR.get(self._severity, "#9e9e9e")
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #ffffff;
                border-left: 4px solid {c};
                border-top: 1px solid #e0e0e0;
                border-right: 1px solid #e0e0e0;
                border-bottom: 1px solid #e0e0e0;
                border-radius: 6px;
            }}
            QLabel {{ color: #212121; background: transparent; }}
        """)

    def update_status(self, new_status: str, severity: str):
        self._severity = severity
        c = self._SEV_COLOR.get(severity, "#757575")
        self._status_lbl.setText(new_status)
        self._status_lbl.setStyleSheet(f"color: {c}; background: transparent;")
        self._apply_frame_style()


# ── StatusIndicator ───────────────────────────────────────────────────────────

class StatusIndicator(QFrame):
    def __init__(self, title: str, enabled: bool = False):
        super().__init__()
        self.setStyleSheet("""
            QFrame { background-color: #f8f9fa; border-radius: 4px; }
            QLabel { color: #212121; background: transparent; }
        """)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(10, 10, 10, 10)
        self._dot = QLabel()
        self._dot.setFont(QFont("Segoe UI", 16))
        lay.addWidget(self._dot)
        lay.addWidget(_lbl(title, size=11))
        lay.addStretch()
        self.set_enabled(enabled)

    def set_enabled(self, enabled: bool):
        if enabled:
            self._dot.setText("●")
            self._dot.setStyleSheet("color: #4CAF50; background: transparent;")
        else:
            self._dot.setText("○")
            self._dot.setStyleSheet("color: #f44336; background: transparent;")


# ── HardeningCard ─────────────────────────────────────────────────────────────

class HardeningCard(QFrame):
    """Card showing one hardening recommendation with two working buttons."""

    # FIX: two separate signals, both with no arguments
    implement_clicked  = Signal()
    learn_more_clicked = Signal()

    _PRIORITY_COLOR = {
        "Critical": "#f44336",
        "High":     "#FF9800",
        "Medium":   "#2196F3",
        "Low":      "#4CAF50",
    }

    def __init__(self, title: str, description: str,
                 priority: str, difficulty: str):
        super().__init__()
        p_color = self._PRIORITY_COLOR.get(priority, "#9e9e9e")
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #ffffff;
                border-left: 4px solid {p_color};
                border-top: 1px solid #e0e0e0;
                border-right: 1px solid #e0e0e0;
                border-bottom: 1px solid #e0e0e0;
                border-radius: 6px;
            }}
            QLabel {{ color: #212121; background: transparent; }}
        """)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(14, 14, 14, 14)
        lay.setSpacing(8)

        # header row: title + priority badge
        header = QHBoxLayout()
        header.addWidget(_lbl(title, size=11, bold=True, color="#1e3a5f"))
        header.addStretch()
        badge = QLabel(f"  {priority}  ")
        badge.setFont(QFont("Segoe UI", 9, QFont.Bold))
        badge.setStyleSheet(
            f"color: #ffffff; background-color: {p_color}; "
            "padding: 3px 8px; border-radius: 3px;"
        )
        header.addWidget(badge)
        lay.addLayout(header)

        # description
        lay.addWidget(_lbl(description, size=10, color="#424242", wrap=True))

        # difficulty chip
        diff_frame = QFrame()
        diff_frame.setStyleSheet("""
            QFrame { background-color: #f0f4f8; border-radius: 4px; }
            QLabel { color: #424242; background: transparent; }
        """)
        diff_lay = QHBoxLayout(diff_frame)
        diff_lay.setContentsMargins(10, 5, 10, 5)
        diff_lay.addWidget(_lbl(f"Difficulty:  {difficulty}", size=9, color="#424242"))
        lay.addWidget(diff_frame)

        # buttons — FIX: each button emits its own dedicated signal (no args)
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        info_btn = _action_btn("ℹ  Learn More", bg="#2196F3", hover="#1565C0")
        info_btn.clicked.connect(self.learn_more_clicked.emit)
        btn_row.addWidget(info_btn)

        impl_btn = _action_btn("🚀  Implement Now", bg="#4CAF50", hover="#2e7d32")
        impl_btn.clicked.connect(self.implement_clicked.emit)
        btn_row.addWidget(impl_btn)

        lay.addLayout(btn_row)


# ── ProgressIndicator ─────────────────────────────────────────────────────────

class ProgressIndicator(QFrame):
    def __init__(self, title: str, current: int, maximum: int):
        super().__init__()
        self.setStyleSheet("""
            QFrame { background-color: #ffffff; border: 1px solid #e0e0e0;
                     border-radius: 6px; }
            QLabel { color: #212121; background: transparent; }
        """)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 12, 12, 12)
        lay.setSpacing(6)

        pct = int(current / maximum * 100) if maximum else 0
        row = QHBoxLayout()
        row.addWidget(_lbl(title, size=11, bold=True))
        row.addStretch()
        row.addWidget(_lbl(f"{pct}%", size=11, bold=True))
        lay.addLayout(row)

        bar = QProgressBar()
        bar.setMaximum(maximum)
        bar.setValue(current)
        bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #e0e0e0; border-radius: 4px;
                text-align: center; height: 18px;
                background-color: #f0f0f0; color: #212121;
            }
            QProgressBar::chunk { background-color: #4CAF50; border-radius: 3px; }
        """)
        lay.addWidget(bar)


# ── ThreatIndicator ───────────────────────────────────────────────────────────

class ThreatIndicator(QFrame):
    _LEVELS = {
        "critical": {"color": "#f44336", "text": "Critical",
                     "desc": "Immediate action required"},
        "high":     {"color": "#FF9800", "text": "High",    "desc": "Action needed soon"},
        "medium":   {"color": "#FFC107", "text": "Medium",  "desc": "Review recommended"},
        "low":      {"color": "#4CAF50", "text": "Low",     "desc": "Good security posture"},
    }

    def __init__(self, threat_level: str = "medium"):
        super().__init__()
        info  = self._LEVELS.get(threat_level, self._LEVELS["medium"])
        color = info["color"]
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #f9f9f9;
                border-left: 5px solid {color};
                border-top: 1px solid #e0e0e0;
                border-right: 1px solid #e0e0e0;
                border-bottom: 1px solid #e0e0e0;
                border-radius: 6px;
            }}
            QLabel {{ color: #212121; background: transparent; }}
        """)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(12, 12, 12, 12)
        lay.addWidget(_lbl(info["text"], size=14, bold=True, color=color))
        lay.addWidget(_lbl(info["desc"], size=10, color="#666666"))
        lay.addStretch()


# ── MetricCard ────────────────────────────────────────────────────────────────

class MetricCard(QFrame):
    def __init__(self, label: str, value: str,
                 unit: str = "", color: str = "#2196F3"):
        super().__init__()
        self.setStyleSheet("""
            QFrame { background-color: #ffffff; border: 1px solid #e0e0e0;
                     border-radius: 6px; }
            QLabel { background: transparent; }
        """)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 12, 12, 12)
        lay.setSpacing(6)
        lay.addWidget(_lbl(label, size=10, color="#666666"))
        row = QHBoxLayout()
        row.addWidget(_lbl(value, size=22, bold=True, color=color))
        if unit:
            row.addWidget(_lbl(unit, size=12, color="#999999"))
        row.addStretch()
        lay.addLayout(row)