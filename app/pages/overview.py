"""
pages/overview.py – Overview Dashboard page.

Sections:
    1. Page header + model badge
    2. KPI cards row
    3. Chart row 1  – Logs Over Time | Anomalies by Host
    4. Chart row 2  – Anomaly Score Distribution | Top Anomalous Event Types
    5. Recent Anomalies table
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ── Plotly dark layout defaults ────────────────────────────────────────────────
_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Syne, sans-serif", color="#94a3b8", size=11),
    margin=dict(l=10, r=10, t=30, b=10),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        bordercolor="rgba(255,255,255,.1)",
        borderwidth=1,
        font=dict(size=10),
    ),
    xaxis=dict(
        gridcolor="rgba(255,255,255,.06)",
        linecolor="rgba(255,255,255,.1)",
        tickfont=dict(size=10),
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,.06)",
        linecolor="rgba(255,255,255,.1)",
        tickfont=dict(size=10),
    ),
)

# Donut / pie charts don't have xaxis/yaxis
_LAYOUT_PIE = {k: v for k, v in _LAYOUT.items() if k not in ("xaxis", "yaxis")}

# Host color palette (matches reference screenshot)
_HOST_COLORS = [
    "#3b82f6", "#ef4444", "#22c55e", "#f97316",
    "#a855f7", "#06b6d4", "#eab308", "#ec4899",
]

_SEVERITY_COLORS = {
    "error":    "#ef4444",
    "warning":  "#f97316",
    "critical": "#a855f7",
    "info":     "#3b82f6",
}


# ── helpers ────────────────────────────────────────────────────────────────────

def _apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """Return a filtered copy of *df* based on sidebar selections."""
    mask = (
        (df["timestamp"].dt.date >= filters["start_date"])
        & (df["timestamp"].dt.date <= filters["end_date"])
    )
    if filters["host"] != "All Hosts":
        mask &= df["host"] == filters["host"]
    if filters["severity"] != "All":
        mask &= df["severity"] == filters["severity"]
    return df[mask].copy()


def _kpi_card(icon: str, label: str, value: str, sub: str, color: str = "") -> str:
    """Return HTML for a single KPI card."""
    return f"""
    <div class="kpi-card">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value {color}">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>
    """


def _chart_card_open(title: str) -> None:
    st.markdown(
        f'<div class="chart-card"><div class="chart-title">{title}</div>',
        unsafe_allow_html=True,
    )


def _chart_card_close() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


# ── chart builders ─────────────────────────────────────────────────────────────

def _fig_logs_over_time(df: pd.DataFrame) -> go.Figure:
    """Line chart: total logs vs anomalies per day."""
    daily = (
        df.set_index("timestamp")
        .resample("D")
        .agg(total=("anomaly_score", "count"), anomalies=("anomaly_score", lambda s: (s >= 0.65).sum()))
        .reset_index()
    )

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=daily["timestamp"], y=daily["total"],
            name="Total Logs", mode="lines",
            line=dict(color="#3b82f6", width=2),
            fill="tozeroy",
            fillcolor="rgba(59,130,246,.08)",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=daily["timestamp"], y=daily["anomalies"],
            name="Anomalies", mode="lines",
            line=dict(color="#ef4444", width=2),
        )
    )
    fig.update_layout(**_LAYOUT, height=260)
    return fig


def _fig_anomalies_by_host(anomalies: pd.DataFrame) -> go.Figure:
    """Donut chart: anomaly count per host."""
    counts = anomalies["host"].value_counts().reset_index()
    counts.columns = ["host", "count"]

    fig = go.Figure(
        go.Pie(
            labels=counts["host"],
            values=counts["count"],
            hole=0.55,
            marker=dict(colors=_HOST_COLORS),
            textinfo="percent",
            textfont=dict(size=10),
            hovertemplate="<b>%{label}</b><br>%{value} anomalies (%{percent})<extra></extra>",
        )
    )
    total = counts["count"].sum()
    fig.update_layout(
        **_LAYOUT_PIE,
        height=260,
        annotations=[
            dict(
                text=f"<b>{total}</b><br><span style='font-size:9px'>Total</span>",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=18, color="#e2e8f0", family="IBM Plex Mono"),
            )
        ]
    )
    # Update the legend separately to avoid the "multiple values" conflict
    fig.update_layout(
        legend=dict(
            orientation="v", x=1.0, y=0.5,
            font=dict(size=10),
            bgcolor="rgba(0,0,0,0)",
        )
    )
    return fig


def _fig_score_distribution(df: pd.DataFrame, threshold: float = 0.65) -> go.Figure:
    """Histogram of anomaly scores with threshold line."""
    fig = go.Figure()
    fig.add_trace(
        go.Histogram(
            x=df["anomaly_score"],
            nbinsx=40,
            marker_color="#a855f7",
            opacity=0.85,
            name="Score",
        )
    )
    fig.add_vline(
        x=threshold,
        line_dash="dash",
        line_color="#ef4444",
        line_width=1.5,
        annotation_text=f"Threshold {threshold}",
        annotation_position="top right",
        annotation_font=dict(color="#ef4444", size=10),
    )
    fig.update_layout(
        **_LAYOUT,
        height=260,
        bargap=0.05,
        showlegend=False,
        xaxis_title="Anomaly Score",
        yaxis_title="Count",
    )
    return fig


def _fig_top_event_types(anomalies: pd.DataFrame) -> go.Figure:
    """Horizontal bar chart: top anomalous event types."""
    counts = (
        anomalies["event_type"]
        .value_counts()
        .nlargest(6)
        .sort_values()
        .reset_index()
    )
    counts.columns = ["event_type", "count"]

    colors = [
        f"rgba(239,68,68,{0.6 + 0.4 * (i / max(len(counts) - 1, 1))})"
        for i in range(len(counts))
    ]

    fig = go.Figure(
        go.Bar(
            x=counts["count"],
            y=counts["event_type"],
            orientation="h",
            marker_color=colors,
            text=counts["count"],
            textposition="outside",
            textfont=dict(size=10, color="#e2e8f0"),
        )
    )
    fig.update_layout(
        **_LAYOUT,
        height=260,
        showlegend=False,
        xaxis_title="Count",
        yaxis_title="Event Type",
    )

    # yaxis-i ayrıca yeniləyirik ki, konflikt yaranmasın
    fig.update_layout(
        yaxis=dict(tickfont=dict(size=10), gridcolor="rgba(255,255,255,.06)"),
    )

    return fig


# ── severity badge helper ──────────────────────────────────────────────────────

def _severity_html(sev: str) -> str:
    cls_map = {
        "error":    "badge-error",
        "warning":  "badge-warning",
        "critical": "badge-critical",
        "info":     "badge-info",
    }
    cls = cls_map.get(sev.lower(), "badge-info")
    return f'<span class="badge {cls}">{sev}</span>'


def _score_html(score: float) -> str:
    color = "#ef4444" if score >= 0.65 else "#94a3b8"
    return f'<span style="color:{color};font-family:\'IBM Plex Mono\',monospace;font-weight:700;">{score:.3f}</span>'


# ── main render function ───────────────────────────────────────────────────────

def render_overview(filters: dict) -> None:
    """Render the full Overview Dashboard page."""

    df_raw: pd.DataFrame = st.session_state.raw_df
    df = _apply_filters(df_raw, filters)
    anomalies = df[df["anomaly_score"] >= 0.65]

    # ── Page header ────────────────────────────────────────────────────────────
    col_h, col_badge = st.columns([5, 1])
    with col_h:
        st.markdown(
            """
            <div class="section-header">Overview Dashboard</div>
            <div class="section-sub">Real-time overview of system logs and detected anomalies</div>
            """,
            unsafe_allow_html=True,
        )
    with col_badge:
        st.markdown(
            """
            <div style="text-align:right;padding-top:.3rem;">
                <div style="font-size:.7rem;color:#94a3b8;margin-bottom:.2rem;">Model Selected:</div>
                <div class="model-badge">
                    Isolation Forest
                    <span class="dot"></span>
                    <span style="font-size:.65rem;color:#22c55e;">Loaded</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── KPI row ────────────────────────────────────────────────────────────────
    k1, k2, k3, k4, k5 = st.columns(5)

    total_logs      = len(df)
    n_anomalies     = len(anomalies)
    pct_anomalies   = n_anomalies / total_logs * 100 if total_logs else 0
    avg_score       = df["anomaly_score"].mean() if total_logs else 0
    unique_hosts    = df["host"].nunique()
    unique_users    = df["user"].nunique()
    pct_of_raw      = total_logs / len(df_raw) * 100

    with k1:
        st.markdown(
            _kpi_card("📋", "Total Logs", f"{total_logs:,}", f"{pct_of_raw:.0f}%", "blue"),
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            _kpi_card(
                "⚠️", "Anomalies Detected", f"{n_anomalies:,}",
                f"{pct_anomalies:.2f}% of total", "red",
            ),
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            _kpi_card(
                "📈", "Anomaly Score (Avg)", f"{avg_score:.3f}",
                "(Higher = More Anomalous)", "orange",
            ),
            unsafe_allow_html=True,
        )
    with k4:
        st.markdown(
            _kpi_card("🖥️", "Unique Hosts", str(unique_hosts), f"{pct_of_raw:.0f}%", "green"),
            unsafe_allow_html=True,
        )
    with k5:
        st.markdown(
            _kpi_card("👤", "Unique Users", str(unique_users), f"{pct_of_raw:.0f}%", "blue"),
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)

    # ── Chart row 1 ────────────────────────────────────────────────────────────
    c_left, c_right = st.columns([3, 2])

    with c_left:
        _chart_card_open("Logs Over Time")
        st.plotly_chart(
            _fig_logs_over_time(df),
            use_container_width=True,
            config={"displaylogo": False, "modeBarButtonsToRemove": ["select2d", "lasso2d"]},
        )
        _chart_card_close()

    with c_right:
        _chart_card_open("Anomalies by Host")
        st.plotly_chart(
            _fig_anomalies_by_host(anomalies),
            use_container_width=True,
            config={"displaylogo": False},
        )
        _chart_card_close()

    # ── Chart row 2 ────────────────────────────────────────────────────────────
    c2_left, c2_right = st.columns(2)

    with c2_left:
        _chart_card_open("Anomaly Score Distribution")
        st.plotly_chart(
            _fig_score_distribution(df),
            use_container_width=True,
            config={"displaylogo": False},
        )
        _chart_card_close()

    with c2_right:
        _chart_card_open("Top Anomalous Event Types")
        st.plotly_chart(
            _fig_top_event_types(anomalies),
            use_container_width=True,
            config={"displaylogo": False},
        )
        _chart_card_close()

    # ── Recent Anomalies table ─────────────────────────────────────────────────
    st.markdown(
        "<div class='chart-title' style='font-size:1rem;font-weight:700;margin:.4rem 0 .6rem;'>"
        "Recent Anomalies</div>",
        unsafe_allow_html=True,
    )

    recent = (
        anomalies
        .sort_values("timestamp", ascending=False)
        .head(50)
        .reset_index(drop=True)
    )

    display_cols = [
        "timestamp", "host", "source", "severity",
        "event_type", "user", "ip_address", "message", "anomaly_score",
    ]
    table_df = recent[display_cols].copy()
    table_df["timestamp"] = table_df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
    table_df["anomaly_score"] = table_df["anomaly_score"].round(3)

    # Streamlit native dataframe with column config
    st.dataframe(
        table_df,
        use_container_width=True,
        height=280,
        column_config={
            "timestamp":     st.column_config.TextColumn("Timestamp"),
            "host":          st.column_config.TextColumn("Host"),
            "source":        st.column_config.TextColumn("Source"),
            "severity":      st.column_config.TextColumn("Severity"),
            "event_type":    st.column_config.TextColumn("Event Type"),
            "user":          st.column_config.TextColumn("User"),
            "ip_address":    st.column_config.TextColumn("IP Address"),
            "message":       st.column_config.TextColumn("Message", width="large"),
            "anomaly_score": st.column_config.ProgressColumn(
                "Anomaly Score",
                min_value=0, max_value=1,
                format="%.3f",
            ),
        },
        hide_index=True,
    )

    # View all button
    _, btn_col, _ = st.columns([3, 2, 3])
    with btn_col:
        if st.button("View All Anomalies →", use_container_width=True):
            st.session_state.active_page = "Anomaly Explorer"
            st.rerun()
