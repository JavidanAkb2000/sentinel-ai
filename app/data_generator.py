"""
data_generator.py – Generates realistic mock system-log data.

If a real dataset is uploaded, load it via load_dataset() instead.
"""

from __future__ import annotations

import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


# ── Constants ──────────────────────────────────────────────────────────────────
HOSTS = ["web-1", "web-2", "db-1", "db-2", "api-1", "worker-1", "worker-2", "cache-1"]
SOURCES = ["firewall", "ssh", "system", "application", "kernel", "nginx", "auth"]
SEVERITIES = ["info", "warning", "error", "critical"]
EVENT_TYPES = [
    "login_success", "login_failed", "port_scan", "permission_denied",
    "config_change", "service_restart", "file_access", "network_timeout",
    "disk_full", "memory_spike", "cpu_spike", "user_created", "user_deleted",
]
ANOMALOUS_EVENTS = ["login_failed", "port_scan", "permission_denied",
                    "config_change", "service_restart"]
MESSAGES = {
    "login_failed":      "Failed password attempt from {ip}",
    "port_scan":         "Port scan detected from external IP {ip}",
    "permission_denied": "Permission denied for {user} on sensitive path",
    "config_change":     "Configuration file modified unexpectedly",
    "service_restart":   "Unexpected service restart detected",
    "login_success":     "Successful login from {ip}",
    "file_access":       "Sensitive file accessed by {user}",
    "network_timeout":   "Connection timeout to upstream {ip}",
    "disk_full":         "Disk usage exceeded 95% threshold",
    "memory_spike":      "Memory usage spike detected: >90%",
    "cpu_spike":         "CPU usage spike: >95% for 60s",
    "user_created":      "New user account created: {user}",
    "user_deleted":      "User account deleted",
}

_RNG = random.Random(42)


def _random_ip() -> str:
    return f"{_RNG.randint(1,254)}.{_RNG.randint(1,254)}.{_RNG.randint(1,254)}.{_RNG.randint(1,99)}"


def _random_user() -> str:
    users = ["admin", "root", "deploy", "svc_account", "jdoe", "msmith", "-", "-", "-"]
    return _RNG.choice(users)


def generate_mock_data(
    n_logs: int = 10_000,
    days: int = 30,
    anomaly_rate: float = 0.022,
) -> pd.DataFrame:
    """Generate *n_logs* synthetic log records over *days* days."""
    np.random.seed(42)

    end_ts = datetime(2025, 1, 30, 23, 59, 59)
    start_ts = end_ts - timedelta(days=days - 1)

    # Random timestamps (sorted)
    total_seconds = int((end_ts - start_ts).total_seconds())
    offsets = sorted(np.random.randint(0, total_seconds, n_logs))
    timestamps = [start_ts + timedelta(seconds=int(o)) for o in offsets]

    rows = []
    for ts in timestamps:
        host = _RNG.choice(HOSTS)
        is_anomaly = _RNG.random() < anomaly_rate

        if is_anomaly:
            event_type = _RNG.choice(ANOMALOUS_EVENTS)
            severity   = _RNG.choice(["warning", "error", "critical"])
            score      = round(_RNG.uniform(0.65, 1.0), 4)
        else:
            event_type = _RNG.choice(EVENT_TYPES)
            severity   = _RNG.choices(SEVERITIES, weights=[70, 20, 8, 2])[0]
            score      = round(_RNG.uniform(0.0, 0.64), 4)

        user = _random_user()
        ip   = _random_ip()
        msg  = MESSAGES.get(event_type, "System event occurred").format(
            ip=ip, user=user
        )

        rows.append(
            {
                "timestamp":          ts,
                "host":               host,
                "source":             _RNG.choice(SOURCES),
                "severity":           severity,
                "event_type":         event_type,
                "user":               user,
                "ip_address":         ip,
                "message":            msg,
                "is_injected_anomaly": int(is_anomaly),
                "anomaly_score":      score,
            }
        )

    df = pd.DataFrame(rows)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def load_dataset(path: str) -> pd.DataFrame:
    """Load a CSV/Parquet dataset and coerce the timestamp column."""
    if path.endswith(".parquet"):
        df = pd.read_parquet(path)
    else:
        df = pd.read_csv(path)

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # If anomaly_score is missing, add a placeholder
    if "anomaly_score" not in df.columns:
        df["anomaly_score"] = np.nan

    return df
