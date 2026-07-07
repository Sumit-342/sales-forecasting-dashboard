import streamlit as st

from utils import inject_css, page_hero, panel_start, panel_end, load_cluster_features, load_cluster_labels
from charts import pca_scatter

st.set_page_config(page_title="Sales Intelligence · Product Demand Segments", page_icon="🎯", layout="wide")
inject_css()

page_hero(
    "SALES INTELLIGENCE · PAGE 4",
    "Product Demand Segments",
    "K-Means clusters of sub-categories, visualized via existing PCA components.",
)

cluster_df = load_cluster_features()
cluster_labels = load_cluster_labels()

panel_start("Cluster Map (PCA)", "Each point is a sub-category, positioned by its top 2 principal components")
st.plotly_chart(pca_scatter(cluster_df, cluster_labels), width="stretch", config={"displayModeBar": False})
panel_end()

badge_colors = ["blue", "cyan", "violet", "red"]
cols = st.columns(len(cluster_labels))
for i, (cid, meta) in enumerate(sorted(cluster_labels.items())):
    with cols[i % len(cols)]:
        st.markdown(f'<span class="badge {badge_colors[cid % len(badge_colors)]}">{meta["name"].upper()}</span>', unsafe_allow_html=True)

st.write("")
panel_start("Sub-Category Breakdown", "Cluster assignment, business interpretation, and stocking strategy")

table = cluster_df.copy()
table["Cluster Name"] = table["Cluster"].map(lambda c: cluster_labels[c]["name"])
table["Stocking Strategy"] = table["Cluster"].map(lambda c: cluster_labels[c]["strategy"])
table = table[[
    "Sub-Category", "Cluster Name", "Total_Sales", "Sales_Growth_Rate",
    "Average_Order_Value", "Stocking Strategy",
]].rename(columns={
    "Total_Sales": "Total Sales", "Sales_Growth_Rate": "Avg. Growth Rate",
    "Average_Order_Value": "Avg. Order Value",
}).sort_values("Total Sales", ascending=False)

st.dataframe(
    table.style.format({
        "Total Sales": "${:,.0f}",
        "Avg. Growth Rate": "{:+.1%}",
        "Avg. Order Value": "${:,.2f}",
    }),
    width="stretch", hide_index=True, height=420,
)
panel_end()

with st.expander("What do these segments mean?"):
    for cid, meta in sorted(cluster_labels.items()):
        st.markdown(f"**{meta['name']}** — {meta['strategy']}")
