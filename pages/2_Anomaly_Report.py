import streamlit as st

from utils import inject_css, page_hero, kpi_card, panel_start, panel_end, fmt_money, load_weekly_anomaly
from charts import anomaly_chart

st.set_page_config(page_title="Sales Intelligence · Anomaly Report", page_icon="🚨", layout="wide")
inject_css()

page_hero(
    "SALES INTELLIGENCE · PAGE 3",
    "Anomaly Report",
    "Weekly sales anomalies from the existing Isolation Forest and Z-Score analysis.",
)

weekly_df = load_weekly_anomaly()

with st.sidebar:
    st.markdown("### 🧭 Detection Method")
    method_label = st.radio("Method", ["Isolation Forest", "Z-Score"])
    method = "isolation_forest" if method_label == "Isolation Forest" else "z_score"
    st.markdown("---")
    st.caption("Both anomaly sets were already computed in the notebook.")

if method == "isolation_forest":
    anomalies = weekly_df[weekly_df["Anomaly"] == -1]
else:
    anomalies = weekly_df[weekly_df["Z_Anomaly"] == True]  # noqa: E712

n_anomalies = len(anomalies)
highest = anomalies["Sales"].max() if n_anomalies else 0
lowest = anomalies["Sales"].min() if n_anomalies else 0

st.markdown(f'<span class="badge red">METHOD: {method_label.upper()}</span>', unsafe_allow_html=True)
st.write("")

c1, c2, c3 = st.columns(3)
with c1:
    kpi_card("Number of Anomalies", f"{n_anomalies}", icon="⚠️", accent=("#F87171", "#FBBF24"))
with c2:
    kpi_card("Highest Anomaly", fmt_money(highest, compact=False), icon="🔺", accent=("#FBBF24", "#F87171"))
with c3:
    kpi_card("Lowest Anomaly", fmt_money(lowest, compact=False), icon="🔻", accent=("#3B82F6", "#F87171"))

st.write("")
panel_start("Weekly Sales with Flagged Anomalies", f"Detected via {method_label}")
st.plotly_chart(anomaly_chart(weekly_df, method), width="stretch", config={"displayModeBar": False})
panel_end()

panel_start("Anomaly Table")
table = anomalies[["Order Date", "Sales"]].sort_values("Order Date", ascending=False).copy()
table["Order Date"] = table["Order Date"].dt.strftime("%d %b %Y")
st.dataframe(
    table.rename(columns={"Order Date": "Week Of"}).style.format({"Sales": "${:,.0f}"}),
    width="stretch", hide_index=True, height=320,
)
panel_end()
