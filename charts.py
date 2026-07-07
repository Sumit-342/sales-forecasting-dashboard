import pandas as pd
import plotly.graph_objects as go

from theme import (
    apply_dark_layout, PRIMARY, SECONDARY, ACCENT_VIOLET,
    SUCCESS, DANGER, WARNING, TEXT, TEXT_MUTED, GRID,
)


def sales_by_year_bar(sales_df: pd.DataFrame):
    yearly = sales_df.groupby("Year")["Sales"].sum().reset_index()
    fig = go.Figure(
        go.Bar(
            x=yearly["Year"].astype(str),
            y=yearly["Sales"],
            marker=dict(
                color=yearly["Sales"],
                colorscale=[[0, "#1E3A8A"], [1, PRIMARY]],
                line=dict(width=0),
            ),
            hovertemplate="Year: %{x}<br>Sales: $%{y:,.0f}<extra></extra>",
            marker_line_width=0,
            text=[f"${v/1000:.0f}K" for v in yearly["Sales"]],
            textposition="outside",
            textfont=dict(color=TEXT_MUTED, size=11),
            width=0.5,
        )
    )
    fig.update_traces(marker_cornerradius=8)
    apply_dark_layout(fig, height=340, legend=False)
    # NOTE: previously `title=None` was passed here. Plotly treats an explicit
    # None as "set the title to null" (not "leave unset"), and Plotly.js then
    # renders that null title as the literal text "undefined" next to the
    # axis. Simply not passing `title` at all leaves it correctly blank.
    fig.update_yaxes(tickprefix="$", tickformat=",.0f")
    return fig


def monthly_trend_line(monthly_sales: pd.DataFrame):
    fig = go.Figure(
        go.Scatter(
            x=monthly_sales["Order Date"],
            y=monthly_sales["Sales"],
            mode="lines",
            line=dict(color=SECONDARY, width=2.5, shape="spline"),
            fill="tozeroy",
            fillcolor="rgba(6, 182, 212, 0.12)",
            hovertemplate="Month: %{x|%b %Y}<br>Sales: $%{y:,.0f}<extra></extra>",
        )
    )
    apply_dark_layout(fig, height=340, legend=False)
    fig.update_yaxes(tickprefix="$", tickformat=",.0f")
    return fig


def forecast_chart(actual_df: pd.DataFrame, forecast_df: pd.DataFrame, horizon: int, label: str):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=actual_df["ds"], y=actual_df["y"],
        mode="lines+markers", name="Actual",
        line=dict(color=TEXT_MUTED, width=2),
        marker=dict(size=5),
        hovertemplate="Date: %{x|%b %Y}<br>Actual: $%{y:,.0f}<extra></extra>",
    ))

    fc = forecast_df.tail(horizon)
    last_actual = actual_df.iloc[[-1]]
    bridge_x = pd.concat([last_actual["ds"], fc["ds"]])
    bridge_y = pd.concat([last_actual["y"], fc["yhat"]])

    fig.add_trace(go.Scatter(
        x=fc["ds"], y=fc["yhat_upper"],
        mode="lines", line=dict(width=0), showlegend=False, hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter(
        x=fc["ds"], y=fc["yhat_lower"],
        mode="lines", line=dict(width=0), fill="tonexty",
        fillcolor="rgba(59, 130, 246, 0.15)", name="Confidence Interval",
        hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter(
        x=bridge_x, y=bridge_y,
        mode="lines+markers", name=f"{label} Forecast",
        line=dict(color=PRIMARY, width=2.5, dash="dash"),
        marker=dict(size=6, symbol="diamond"),
        hovertemplate="Date: %{x|%b %Y}<br>Forecast: $%{y:,.0f}<extra></extra>",
    ))

    apply_dark_layout(fig, height=380)
    fig.update_yaxes(tickprefix="$", tickformat=",.0f")
    return fig


def anomaly_chart(weekly_df: pd.DataFrame, method: str):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=weekly_df["Order Date"], y=weekly_df["Sales"],
        mode="lines", name="Weekly Sales",
        line=dict(color=SECONDARY, width=2),
        hovertemplate="Week of: %{x|%d %b %Y}<br>Sales: $%{y:,.0f}<extra></extra>",
    ))

    if method == "isolation_forest":
        anomalies = weekly_df[weekly_df["Anomaly"] == -1]
    else:
        anomalies = weekly_df[weekly_df["Z_Anomaly"] == True]  # noqa: E712

    fig.add_trace(go.Scatter(
        x=anomalies["Order Date"], y=anomalies["Sales"],
        mode="markers", name="Anomaly",
        marker=dict(color=DANGER, size=11, symbol="x", line=dict(width=1, color="#7F1D1D")),
        hovertemplate="Week of: %{x|%d %b %Y}<br>Anomaly: $%{y:,.0f}<extra></extra>",
    ))

    apply_dark_layout(fig, height=380)
    fig.update_yaxes(tickprefix="$", tickformat=",.0f")
    return fig


def pca_scatter(cluster_df: pd.DataFrame, cluster_labels: dict):
    fig = go.Figure()
    palette = [PRIMARY, SECONDARY, ACCENT_VIOLET, WARNING]

    for cid in sorted(cluster_df["Cluster"].unique()):
        sub = cluster_df[cluster_df["Cluster"] == cid]
        name = cluster_labels.get(cid, {}).get("name", f"Cluster {cid}")
        fig.add_trace(go.Scatter(
            x=sub["PCA1"], y=sub["PCA2"],
            mode="markers",
            name=name,
            marker=dict(size=14, color=palette[cid % len(palette)],
                        line=dict(width=1.5, color="rgba(255,255,255,0.25)")),
            hovertemplate="Sub-Category: %{text}<br>PC1: %{x:.2f} · PC2: %{y:.2f}<extra>" + name + "</extra>",
            text=sub["Sub-Category"],
        ))

    apply_dark_layout(fig, height=460)
    fig.update_xaxes(title="Principal Component 1")
    fig.update_yaxes(title="Principal Component 2")
    return fig


def model_comparison_bar(comparison_df: pd.DataFrame, metric: str):
    fig = go.Figure(
        go.Bar(
            x=comparison_df["Model"],
            y=comparison_df[metric],
            marker=dict(color=[PRIMARY, SECONDARY, ACCENT_VIOLET], cornerradius=8),
            text=[f"{v:,.0f}" for v in comparison_df[metric]],
            textposition="outside",
            textfont=dict(color=TEXT_MUTED, size=11),
            width=0.45,
            hovertemplate=f"Model: %{{x}}<br>{metric}: %{{y:,.2f}}<extra></extra>",
        )
    )
    apply_dark_layout(fig, height=280, legend=False)
    return fig
