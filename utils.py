import json
import re
from pathlib import Path

import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).parent / "data"


def inject_css():
    css_path = Path(__file__).parent / "styles.css"
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)


def page_hero(eyebrow: str, title: str, description: str = ""):
    # Presentation-only cleanup: strips a trailing "· PAGE n" segment so the
    # hero eyebrow reads as a clean section label (no logic/data affected).
    eyebrow = re.sub(r"\s*[·•]\s*PAGE\s*\d+\s*", "", eyebrow, flags=re.IGNORECASE).strip()
    st.markdown(
        f"""
        <div class="page-hero">
            <div class="page-eyebrow">{eyebrow}</div>
            <h1 style="margin-bottom:2px;">{title}</h1>
            {f'<div class="page-desc">{description}</div>' if description else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )


def fmt_money(value: float, compact: bool = True) -> str:
    v = float(value)
    sign = "-" if v < 0 else ""
    v = abs(v)
    if not compact:
        return f"{sign}${v:,.2f}"
    if v >= 1_000_000:
        return f"{sign}${v/1_000_000:.2f}M"
    if v >= 1_000:
        return f"{sign}${v/1_000:.1f}K"
    return f"{sign}${v:,.0f}"


def kpi_card(label: str, value: str, delta: str = "", direction: str = "flat",
             icon: str = "", accent: tuple = ("#3B82F6", "#06B6D4")):
    arrow = {"up": "▲", "down": "▼", "flat": "•"}[direction]
    delta_html = f'<div class="kpi-delta {direction}">{arrow} {delta}</div>' if delta else ""
    st.markdown(
        f"""
        <div class="kpi-card" style="--accent-a:{accent[0]}; --accent-b:{accent[1]};">
            <div class="kpi-label">{icon} {label}</div>
            <div class="kpi-value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def panel_start(title: str, subtitle: str = ""):
    st.markdown(
        f"""<div class="glass-panel"><div class="panel-title">{title}</div>
        {f'<div class="panel-subtitle">{subtitle}</div>' if subtitle else ""}""",
        unsafe_allow_html=True,
    )


def panel_end():
    st.markdown("</div>", unsafe_allow_html=True)


# ---------------- data loaders (cached) ----------------

@st.cache_data
def load_sales_df():
    df = pd.read_csv(DATA_DIR / "sales_df.csv", parse_dates=["Order Date", "Ship Date"])
    return df


@st.cache_data
def load_monthly_sales():
    return pd.read_csv(DATA_DIR / "monthly_sales.csv", parse_dates=["Order Date"])


@st.cache_data
def load_category_revenue():
    return pd.read_csv(DATA_DIR / "category_revenue.csv")


@st.cache_data
def load_region_sales():
    return pd.read_csv(DATA_DIR / "region_sales.csv")


@st.cache_data
def load_comparison_df():
    return pd.read_csv(DATA_DIR / "comparison_df.csv")


@st.cache_data
def load_sarima_forecast():
    return pd.read_csv(DATA_DIR / "sarima_forecast.csv", parse_dates=["ds"])


@st.cache_data
def load_sarima_history():
    return pd.read_csv(DATA_DIR / "sarima_history.csv", parse_dates=["ds"])


@st.cache_data
def load_prophet_overall_forecast():
    return pd.read_csv(DATA_DIR / "prophet_overall_forecast.csv", parse_dates=["ds"])


@st.cache_data
def load_prophet_overall_actual():
    return pd.read_csv(DATA_DIR / "prophet_overall_actual.csv", parse_dates=["ds"])


@st.cache_data
def load_xgb_forecast():
    return pd.read_csv(DATA_DIR / "xgb_forecast.csv", parse_dates=["ds"])


@st.cache_data
def load_xgb_test():
    return pd.read_csv(DATA_DIR / "xgb_test.csv", parse_dates=["ds"])


@st.cache_data
def load_segment_actual(name: str):
    fname = name.replace(" ", "_")
    return pd.read_csv(DATA_DIR / f"segment_actual_{fname}.csv", parse_dates=["ds"])


@st.cache_data
def load_segment_forecast(name: str):
    fname = name.replace(" ", "_")
    return pd.read_csv(DATA_DIR / f"segment_forecast_{fname}.csv", parse_dates=["ds"])


@st.cache_data
def load_segment_metrics():
    with open(DATA_DIR / "segment_metrics.json") as f:
        return json.load(f)


@st.cache_data
def load_weekly_anomaly():
    return pd.read_csv(DATA_DIR / "weekly_sales_anomaly.csv", parse_dates=["Order Date"])


@st.cache_data
def load_cluster_features():
    return pd.read_csv(DATA_DIR / "cluster_features.csv")


@st.cache_data
def load_cluster_labels():
    with open(DATA_DIR / "cluster_labels.json") as f:
        raw = json.load(f)
    return {int(k): v for k, v in raw.items()}


@st.cache_data
def load_metrics():
    with open(DATA_DIR / "metrics.json") as f:
        return json.load(f)
