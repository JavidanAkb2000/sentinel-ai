"""
sidebar.py – Left sidebar: navigation, filters, system info.
"""

from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

from data_generator import generate_mock_data


# ── helpers ────────────────────────────────────────────────────────────────────

def _nav_icon(page: str) -> str:
    icons = {
        "Overview Dashboard": "🛡️",
        "Anomaly Explorer":   "🔍",
        "Model Insights":     "📊",
        "About":              "ℹ️",
    }
    return icons.get(page, "•")


# ── main function ──────────────────────────────────────────────────────────────

def render_sidebar() -> dict:
    """Render the sidebar and return the active filter dict."""

    with st.sidebar:
        # ── Logo / Title ──────────────────────────────────────────────────────
        st.markdown(
            """
            <div style="display:flex;align-items:center;gap:.7rem;margin-bottom:.3rem;margin-top:.2rem;">
                <div style="background:rgba(59,130,246,.18);border:1px solid rgba(59,130,246,.35);
                            border-radius:10px;padding:.45rem .55rem;font-size:1.25rem;line-height:1;">
                    🛡️
                </div>
                <div style="font-size:1rem;font-weight:800;color:#e2e8f0;line-height:1.25;">
                    Log Anomaly<br>Detection System
                </div>
            </div>
            <div style="font-size:.72rem;color:#64748b;margin-bottom:1.1rem;padding-left:.2rem;line-height:1.5;">
                ML-Based Anomaly Detection<br>in System Logs
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Navigation ────────────────────────────────────────────────────────
        pages = ["Overview Dashboard", "Anomaly Explorer", "Model Insights", "About"]
        for page in pages:
            active = st.session_state.get("active_page") == page
            if st.button(
                f"{_nav_icon(page)}  {page}",
                key=f"nav_{page}",
                use_container_width=True,
            ):
                st.session_state.active_page = page
                st.rerun()

        st.markdown("<hr style='border-color:#2d3748;margin:1rem 0;'>", unsafe_allow_html=True)

        # ── Load / cache data ─────────────────────────────────────────────────
        if "raw_df" not in st.session_state:
            with st.spinner("Generating mock data…"):
                st.session_state.raw_df = generate_mock_data()

        df: pd.DataFrame = st.session_state.raw_df
        min_date = df["timestamp"].min().date()
        max_date = df["timestamp"].max().date()

        # ── Filters heading ───────────────────────────────────────────────────
        st.markdown(
            "<div style='font-size:.88rem;font-weight:700;color:#e2e8f0;"
            "margin-bottom:.75rem;'>Filters</div>",
            unsafe_allow_html=True,
        )

        # Date range
        st.markdown(
            "<div style='font-size:.76rem;color:#94a3b8;margin-bottom:.25rem;'>"
            "Select Date Range</div>",
            unsafe_allow_html=True,
        )
        date_range = st.date_input(
            label="date_range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            label_visibility="collapsed",
            key="date_range_input",
        )

        # Host dropdown
        hosts = ["All Hosts"] + sorted(df["host"].unique().tolist())
        st.markdown(
            "<div style='font-size:.76rem;color:#94a3b8;margin:.75rem 0 .25rem;'>"
            "Select Host</div>",
            unsafe_allow_html=True,
        )
        selected_host = st.selectbox(
            "host_select", hosts, label_visibility="collapsed", key="host_select"
        )

        # Severity dropdown
        severities = ["All"] + sorted(df["severity"].unique().tolist())
        st.markdown(
            "<div style='font-size:.76rem;color:#94a3b8;margin:.75rem 0 .25rem;'>"
            "Select Severity</div>",
            unsafe_allow_html=True,
        )
        selected_severity = st.selectbox(
            "sev_select", severities, label_visibility="collapsed", key="sev_select"
        )

        st.markdown("<div style='margin-top:.5rem;'></div>", unsafe_allow_html=True)

        # Apply / Reset buttons — full-width stacked like the screenshot
        apply = st.button("☰  Apply Filters", use_container_width=True, key="apply_btn")
        reset = st.button("↺  Reset Filters", use_container_width=True, key="reset_btn")

        if reset:
            for key in ["date_range_input", "host_select", "sev_select"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

        # ── System Info ───────────────────────────────────────────────────────
        total_logs   = len(df)
        time_range   = f"{(max_date - min_date).days} Days"
        unique_hosts = df["host"].nunique()
        unique_users = df["user"].nunique()

        st.markdown(
            f"""
            <div class="sys-info-box">
                <div class="sys-info-title">System Info</div>
                <div class="sys-info-row">
                    <span>Total Logs</span><span>{total_logs:,}</span>
                </div>
                <div class="sys-info-row">
                    <span>Time Range</span><span>{time_range}</span>
                </div>
                <div class="sys-info-row">
                    <span>Unique Hosts</span><span>{unique_hosts}</span>
                </div>
                <div class="sys-info-row">
                    <span>Unique Users</span><span>{unique_users}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Build filter dict ──────────────────────────────────────────────────────
    start_date = date_range[0] if isinstance(date_range, (list, tuple)) and len(date_range) >= 1 else min_date
    end_date   = date_range[1] if isinstance(date_range, (list, tuple)) and len(date_range) >= 2 else max_date

    return {
        "start_date": start_date,
        "end_date":   end_date,
        "host":       selected_host,
        "severity":   selected_severity,
    }