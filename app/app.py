"""
Log Anomaly Detection System - Streamlit Dashboard
====================================================
Main entry point for the multi-page application.

Run with:
    streamlit run app.py
"""

import streamlit as st

# ── Page config must be the very first Streamlit call ──────────────────────────
st.set_page_config(
    page_title="Log Anomaly Detection System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Local imports ──────────────────────────────────────────────────────────────
from styles import inject_global_css
from sidebar import render_sidebar
from pages.overview import render_overview

# ── Inject global dark-theme CSS ───────────────────────────────────────────────
inject_global_css()

# ── Session-state defaults ─────────────────────────────────────────────────────
if "active_page" not in st.session_state:
    st.session_state.active_page = "Overview Dashboard"

# ── Sidebar (navigation + filters) ────────────────────────────────────────────
filters = render_sidebar()

# ── Page routing ───────────────────────────────────────────────────────────────
page = st.session_state.active_page

if page == "Overview Dashboard":
    render_overview(filters)

elif page == "Anomaly Explorer":
    st.title("🔍 Anomaly Explorer")
    st.info("This page is under construction. Select **Overview Dashboard** to continue.")

elif page == "Model Insights":
    st.title("📊 Model Insights")
    st.info("This page is under construction. Select **Overview Dashboard** to continue.")

elif page == "About":
    st.title("ℹ️ About")
    st.markdown(
        """
        **Log Anomaly Detection System** is a diploma-project dashboard that applies
        ML-based anomaly detection (Isolation Forest, LOF, One-Class SVM) to
        enterprise system logs.

        **Author:** Diploma candidate  
        **Tech stack:** Python · Streamlit · Plotly · scikit-learn · pandas
        """
    )
