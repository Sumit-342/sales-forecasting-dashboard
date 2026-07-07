import streamlit as st

from utils import (
    inject_css, page_hero, kpi_card, panel_start, panel_end,
    fmt_money, load_segment_actual, load_segment_forecast, load_segment_metrics,
)
from charts import forecast_chart

st.set_page_config(page_title="Sales Intelligence · Forecast Explorer", page_icon="📈", layout="wide")
inject_css()

page_hero(
    "SALES INTELLIGENCE · PAGE 2",
    "Forecast Explorer",
    "Prophet forecasts by category or region, already generated in the notebook.",
)

CATEGORY_OPTIONS = ["Furniture", "Technology", "Office Supplies"]
REGION_OPTIONS = ["West", "East", "Central", "South"]

with st.sidebar:
    st.markdown("### 🧭 Forecast Controls")
    dimension = st.radio("Dimension", ["Category", "Region"], horizontal=True)
    options = CATEGORY_OPTIONS if dimension == "Category" else REGION_OPTIONS
    selection = st.selectbox(dimension, options)
    horizon_label = st.select_slider("Forecast Horizon", options=["1 Month", "2 Months", "3 Months"], value="3 Months")
    horizon = {"1 Month": 1, "2 Months": 2, "3 Months": 3}[horizon_label]
    st.markdown("---")
    st.caption("Forecasts use the existing per-segment Prophet models — not retrained here.")

actual_df = load_segment_actual(selection)
forecast_df = load_segment_forecast(selection)
metrics = load_segment_metrics()[selection]

badge_class = "blue" if dimension == "Category" else "cyan"
st.markdown(
    f'<span class="badge {badge_class}">{dimension.upper()}: {selection}</span> '
    f'<span class="badge violet">HORIZON: {horizon_label.upper()}</span>',
    unsafe_allow_html=True,
)
st.write("")

c1, c2, c3 = st.columns(3)
with c1:
    kpi_card("Model MAE", fmt_money(metrics["mae"], compact=False), icon="📐", accent=("#3B82F6", "#06B6D4"))
with c2:
    kpi_card("Model RMSE", fmt_money(metrics["rmse"], compact=False), icon="📏", accent=("#06B6D4", "#8B5CF6"))
with c3:
    next_val = forecast_df.tail(horizon)["yhat"].iloc[0]
    kpi_card("Next Period Forecast", fmt_money(next_val, compact=False), icon="🔮", accent=("#8B5CF6", "#3B82F6"))

st.write("")
panel_start(f"{selection} — Forecast vs Actual", f"Prophet forecast with confidence interval, {horizon_label.lower()} ahead")
st.plotly_chart(
    forecast_chart(actual_df, forecast_df, horizon, selection),
    width="stretch", config={"displayModeBar": False},
)
panel_end()

panel_start("Forecast Table")
fc_table = forecast_df.tail(horizon).copy()
fc_table["ds"] = fc_table["ds"].dt.strftime("%b %Y")
fc_table = fc_table.rename(columns={
    "ds": "Period", "yhat": "Forecast", "yhat_lower": "Lower Bound", "yhat_upper": "Upper Bound",
})
st.dataframe(
    fc_table.style.format({"Forecast": "${:,.0f}", "Lower Bound": "${:,.0f}", "Upper Bound": "${:,.0f}"}),
    width="stretch", hide_index=True,
)
panel_end()
