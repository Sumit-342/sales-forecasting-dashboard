import streamlit as st

from utils import (
    inject_css, page_hero, kpi_card, panel_start, panel_end,
    fmt_money, load_sales_df, load_monthly_sales,
)
from charts import sales_by_year_bar, monthly_trend_line

st.set_page_config(
    page_title="Sales Intelligence · Overview",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

sales_df = load_sales_df()
monthly_sales = load_monthly_sales()

with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-icon">📊</div>
        <div class="brand-title">Sales Intelligence</div>
        <div class="brand-subtitle">Enterprise Dashboard</div>
    </div>
    """, unsafe_allow_html=True)
    categories = st.multiselect(
        "Category", options=sorted(sales_df["Category"].unique()),
        default=list(sorted(sales_df["Category"].unique())),
    )
    regions = st.multiselect(
        "Region", options=sorted(sales_df["Region"].unique()),
        default=list(sorted(sales_df["Region"].unique())),
    )
    st.markdown("---")
    st.info(
    "Dashboard uses the trained models from the notebook.\nNo live retraining is performed."
)

filtered = sales_df[
    sales_df["Category"].isin(categories) & sales_df["Region"].isin(regions)
]

page_hero(
    "Retail Sales Analytics",
    "Sales Overview",
    "Interactive business intelligence dashboard for sales analysis and forecasting.",
)

total_sales = filtered["Sales"].sum()
total_orders = filtered["Order ID"].nunique()
aov = total_sales / total_orders if total_orders else 0
best_category = (
    filtered.groupby("Category")["Sales"].sum().idxmax() if not filtered.empty else "—"
)

c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi_card("Total Sales", fmt_money(total_sales), icon="💰", accent=("#3B82F6", "#06B6D4"))
with c2:
    kpi_card("Average Order Value", fmt_money(aov, compact=False), icon="🧾", accent=("#06B6D4", "#3B82F6"))
with c3:
    kpi_card("Total Orders", f"{total_orders:,}", icon="📦", accent=("#8B5CF6", "#3B82F6"))
with c4:
    kpi_card("Best Category", best_category, icon="🏆", accent=("#FBBF24", "#8B5CF6"))

st.write("")
col1, col2 = st.columns(2)
with col1:
    panel_start("Total Sales by Year", "Aggregated revenue across each calendar year")
    st.plotly_chart(sales_by_year_bar(filtered), use_container_width=True, config={"displayModeBar": False})
    panel_end()
with col2:
    panel_start("Monthly Sales Trend", "Overall monthly revenue trajectory")
    st.plotly_chart(monthly_trend_line(monthly_sales), use_container_width=True, config={"displayModeBar": False})
    panel_end()
    
with st.expander("📄 View Filtered Transactions"):
    st.dataframe(
        filtered[["Order Date", "Category", "Sub-Category", "Region", "Sales"]]
        .sort_values("Order Date", ascending=False),
        use_container_width=True, height=300,
    )
