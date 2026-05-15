"""
styles.py – Global CSS injection for the dark enterprise theme.
"""

import streamlit as st


def inject_global_css() -> None:
    """Inject all custom CSS into the Streamlit app."""
    st.markdown(
        """
        <style>
        /* ── Google Fonts ─────────────────────────────────────────────────── */
        

        /* ── CSS Variables ───────────────────────────────────────────────── */
        :root {
            --bg-primary:    #0d1117;
            --bg-secondary:  #161b22;
            --bg-card:       #1c2230;
            --bg-card-hover: #232c3d;
            --border:        #2d3748;
            --accent-blue:   #3b82f6;
            --accent-green:  #22c55e;
            --accent-red:    #ef4444;
            --accent-orange: #f97316;
            --accent-purple: #a855f7;
            --text-primary:  #e2e8f0;
            --text-muted:    #94a3b8;
            --text-dim:      #64748b;
            --radius:        12px;
            --shadow:        0 4px 24px rgba(0,0,0,.45);
        }

        /* ── Base overrides ──────────────────────────────────────────────── */
        html, body {
        font-family: 'Syne', sans-serif !important;
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        }

        .stApp {
            background-color: var(--bg-primary) !important;
        }

        /* ── Sidebar ─────────────────────────────────────────────────────── */
        section[data-testid="stSidebar"] {
            background-color: var(--bg-secondary) !important;
            border-right: 1px solid var(--border) !important;
        }
        section[data-testid="stSidebar"] * {
            font-family: 'Syne', sans-serif !important;
        }

        /* ── Main content padding ────────────────────────────────────────── */
        .block-container {
            padding: 1.5rem 2rem !important;
            max-width: 100% !important;
        }

        /* ── KPI Card ────────────────────────────────────────────────────── */
        .kpi-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 1.2rem 1.4rem;
            box-shadow: var(--shadow);
            transition: background .2s;
        }
        .kpi-card:hover { background: var(--bg-card-hover); }
        .kpi-icon   { font-size: 2rem; margin-bottom: .35rem; }
        .kpi-label  { font-size: .72rem; letter-spacing: .08em; text-transform: uppercase;
                      color: var(--text-muted); margin-bottom: .25rem; }
        .kpi-value  { font-size: 2.2rem; font-weight: 800; line-height: 1;
                      font-family: 'IBM Plex Mono', monospace; }
        .kpi-sub    { font-size: .72rem; color: var(--text-dim); margin-top: .3rem; }
        .kpi-value.blue   { color: var(--accent-blue);   }
        .kpi-value.red    { color: var(--accent-red);    }
        .kpi-value.orange { color: var(--accent-orange); }
        .kpi-value.green  { color: var(--accent-green);  }

        /* ── Chart card wrapper ──────────────────────────────────────────── */
        .chart-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 1rem 1.2rem;
            box-shadow: var(--shadow);
            margin-bottom: 1rem;
        }
        .chart-title {
            font-size: .95rem; font-weight: 700;
            color: var(--text-primary); margin-bottom: .6rem;
        }

        /* ── Section header ──────────────────────────────────────────────── */
        .section-header {
            font-size: 1.45rem; font-weight: 800;
            color: var(--text-primary); margin: 0 0 .1rem 0;
        }
        .section-sub {
            font-size: .78rem; color: var(--text-muted); margin-bottom: 1.2rem;
        }

        /* ── Nav button (sidebar) ────────────────────────────────────────── */
        .nav-btn {
            width: 100%; text-align: left;
            background: transparent; border: none;
            color: var(--text-muted); padding: .55rem .8rem;
            border-radius: 8px; font-size: .88rem; font-weight: 600;
            cursor: pointer; transition: all .18s; display: flex;
            align-items: center; gap: .6rem; margin-bottom: .15rem;
        }
        .nav-btn:hover, .nav-btn.active {
            background: rgba(59,130,246,.15);
            color: var(--accent-blue);
        }
        .nav-btn.active { border-left: 3px solid var(--accent-blue); }

        /* ── System-info box ─────────────────────────────────────────────── */
        .sys-info-box {
            background: rgba(34,197,94,.07);
            border: 1px solid rgba(34,197,94,.25);
            border-radius: var(--radius); padding: 1rem;
            margin-top: 1rem;
        }
        .sys-info-title {
            color: var(--accent-green); font-size: .78rem;
            font-weight: 700; letter-spacing: .1em;
            text-transform: uppercase; margin-bottom: .6rem;
        }
        .sys-info-row {
            display: flex; justify-content: space-between;
            font-size: .8rem; padding: .22rem 0;
            border-bottom: 1px solid rgba(255,255,255,.04);
        }
        .sys-info-row span:first-child { color: var(--text-muted); }
        .sys-info-row span:last-child  { color: var(--text-primary); font-weight: 600;
                                          font-family: 'IBM Plex Mono', monospace; }

        /* ── Severity badges ─────────────────────────────────────────────── */
        .badge {
            display: inline-block; padding: .18rem .55rem;
            border-radius: 20px; font-size: .72rem; font-weight: 700;
            letter-spacing: .04em; text-transform: uppercase;
        }
        .badge-error    { background: rgba(239,68,68,.18);   color: #f87171; }
        .badge-warning  { background: rgba(249,115,22,.18);  color: #fb923c; }
        .badge-info     { background: rgba(59,130,246,.18);  color: #60a5fa; }
        .badge-critical { background: rgba(168,85,247,.18);  color: #c084fc; }

        /* ── Dataframe / table ───────────────────────────────────────────── */
        .stDataFrame { border-radius: var(--radius); overflow: hidden; }
        .stDataFrame thead th {
            background: var(--bg-secondary) !important;
            color: var(--text-muted) !important;
            font-size: .75rem !important;
            letter-spacing: .06em;
        }
        .stDataFrame tbody td {
            background: var(--bg-card) !important;
            color: var(--text-primary) !important;
            font-size: .8rem !important;
        }

        /* ── Streamlit buttons ───────────────────────────────────────────── */
        .stButton > button {
            background: var(--bg-card); border: 1px solid var(--border);
            color: var(--text-primary); border-radius: 8px;
            font-family: 'Syne', sans-serif; font-weight: 600;
            transition: all .18s;
        }
        .stButton > button:hover {
            background: var(--accent-blue); border-color: var(--accent-blue);
            color: #fff;
        }

        /* ── Selectbox / date-input ──────────────────────────────────────── */
        .stSelectbox > div > div,
        .stDateInput > div > div {
            background: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            border-radius: 8px !important;
            color: var(--text-primary) !important;
        }

        /* ── Plotly chart background fix ─────────────────────────────────── */
        .js-plotly-plot .plotly .svg-container { border-radius: 8px; }

        /* ── Scrollbar ───────────────────────────────────────────────────── */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: var(--bg-primary); }
        ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

        /* ── Model badge (top-right) ─────────────────────────────────────── */
        .model-badge {
            display: inline-flex; align-items: center; gap: .4rem;
            background: var(--bg-card); border: 1px solid var(--border);
            border-radius: 8px; padding: .35rem .75rem;
            font-size: .8rem; font-weight: 600; color: var(--text-primary);
        }
        .model-badge .dot {
            width: 8px; height: 8px; border-radius: 50%;
            background: var(--accent-green);
            box-shadow: 0 0 6px var(--accent-green);
        }

        /* hide default Streamlit top header */
        /* Keep header so sidebar toggle button remains visible */
        header[data-testid="stHeader"] {
            background: transparent !important;
            height: 0 !important;
        }
        
        header[data-testid="stHeader"] > div {
            padding: 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
