from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="Morrow",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# Load final project outputs
# -----------------------------
forecast = pd.read_parquet(
    BASE_DIR / "predictions/final_deepar_forecast.parquet"
)
validation = pd.read_parquet(
    BASE_DIR / "predictions/deepar_predictions.parquet"
)

validation["date"] = pd.to_datetime(validation["date"])
validation["store_nbr"] = validation["store_nbr"].astype(int)

replenishment = pd.read_csv(
    BASE_DIR / "outputs/replenishment_recommendations.csv"
)
model_comparison = pd.read_csv(
    BASE_DIR / "outputs/final_model_comparison.csv"
)
pattern_metrics = pd.read_csv(
    BASE_DIR / "outputs/pattern_level_metrics.csv"
)

forecast["date"] = pd.to_datetime(forecast["date"])
forecast["store_nbr"] = forecast["store_nbr"].astype(int)
# -----------------------------
# Theme
# -----------------------------
st.markdown("""
<style>
:root {
    --bg: #0b0f16;
    --panel: #111722;
    --panel2: #151c28;
    --border: #263041;
    --text: #f4f7fb;
    --muted: #94a0b4;
    --blue: #69b9ee;
    --blue2: #3f8fd2;
    --green: #76dda7;
    --red: #ff6f72;
    --purple: #8d83f4;
}

.stApp {
    background:
        radial-gradient(circle at 82% 0%, rgba(71,126,176,.12), transparent 24%),
        #0b0f16;
    color: var(--text);
}

.block-container {
    max-width: 1450px;
    padding-top: 2.6rem;
    padding-bottom: 3rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

.stApp h1, .stApp h2, .stApp h3, .stApp h4 {
    color: var(--text) !important;
    letter-spacing: -.4px;
}
.stApp p, .stApp span, .stApp label {
    color: #d5dbe5;
}
[data-testid="stCaptionContainer"] {
    color: var(--muted) !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0d121b;
    border-right: 1px solid #202938;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 2rem;
}
[data-testid="stSidebar"] h1 {
    color: white !important;
    font-size: 1.7rem !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {
    color: #aab4c5;
}
[data-testid="stSidebar"] [role="radiogroup"] {
    gap: .25rem;
}
[data-testid="stSidebar"] [role="radiogroup"] label {
    padding: .65rem .75rem;
    border-radius: 10px;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: #151d29;
}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: #182536;
}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p {
    color: #7fc5f0 !important;
    font-weight: 700;
}

/* Inputs */
[data-baseweb="select"] > div {
    background: #121923 !important;
    border-color: #2b3546 !important;
    border-radius: 10px !important;
    min-height: 46px;
}
[data-baseweb="select"] span {
    color: #f4f7fb !important;
}
[data-baseweb="select"] svg {
    fill: #aab4c5 !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #121923, #101620);
    border: 1px solid #263041;
    border-radius: 15px;
    padding: 1.1rem 1.25rem;
}
[data-testid="stMetricLabel"] {
    color: #98a5b8 !important;
}
[data-testid="stMetricValue"] {
    color: #f4f7fb !important;
    font-weight: 750;
}

/* Tables */
[data-testid="stDataFrame"] {
    border: 1px solid #263041;
    border-radius: 12px;
    overflow: hidden;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Download */
.stDownloadButton button {
    background: #172334;
    color: #eaf6ff !important;
    border: 1px solid #3c5873;
    border-radius: 9px;
    font-weight: 650;
}
.stDownloadButton button:hover {
    background: #1d3046;
    border-color: #69b9ee;
    color: white !important;
}

/* Hero */
.df-hero {
    position: relative;
    overflow: hidden;
    display: grid;
    grid-template-columns: 1.35fr .65fr;
    gap: 2rem;
    align-items: center;
    padding: 2.5rem 2.7rem;
    margin-bottom: 1.35rem;
    border-radius: 18px;
    background:
        linear-gradient(120deg, #111923 0%, #101720 55%, #101a24 100%);
    border: 1px solid #273243;
    box-shadow: 0 16px 40px rgba(0,0,0,.20);
}
.df-hero:after {
    content: "";
    position: absolute;
    width: 330px;
    height: 330px;
    right: -105px;
    top: -160px;
    border-radius: 50%;
    background: rgba(77,150,205,.09);
}
.df-hero-content, .df-hero-visual {
    position: relative;
    z-index: 2;
}
.df-eyebrow {
    color: #69b9ee !important;
    font-size: .75rem;
    font-weight: 800;
    letter-spacing: 1.7px;
    margin-bottom: .8rem;
}
.df-hero-title {
    color: #f6f8fb !important;
    font-size: 2.85rem;
    line-height: 1.05;
    font-weight: 800;
    letter-spacing: -1.7px;
}
.df-hero-text {
    color: #aeb8c8 !important;
    max-width: 690px;
    font-size: 1rem;
    line-height: 1.65;
    margin-top: 1rem;
}
.df-tags {
    display: flex;
    flex-wrap: wrap;
    gap: .55rem;
    margin-top: 1.25rem;
}
.df-tags span {
    color: #c8d7e5 !important;
    background: #151f2b;
    border: 1px solid #2d3a4d;
    padding: .42rem .72rem;
    border-radius: 100px;
    font-size: .76rem;
    font-weight: 650;
}
.df-visual-box {
    background: #0d141e;
    border: 1px solid #293548;
    border-radius: 15px;
    padding: 1.35rem;
}
.df-visual-small {
    color: #8190a6 !important;
    font-size: .68rem;
    font-weight: 750;
    letter-spacing: 1.2px;
}
.df-visual-number {
    color: #f4f7fb !important;
    font-size: 2.15rem;
    font-weight: 800;
    margin-top: .3rem;
}
.df-visual-label {
    color: #8190a6 !important;
    font-size: .76rem;
}
.df-bars {
    height: 75px;
    display: flex;
    align-items: flex-end;
    gap: 7px;
    margin-top: 1.1rem;
}
.df-bars div {
    flex: 1;
    border-radius: 4px 4px 1px 1px;
    background: linear-gradient(180deg, #76c8f4, #397eb8);
}

/* Custom cards */
.df-kpi {
    min-height: 135px;
    background: linear-gradient(145deg, #121923, #101620);
    border: 1px solid #263041;
    border-radius: 15px;
    padding: 1.15rem 1.25rem;
}
.df-kpi-accent {
    width: 32px;
    height: 5px;
    border-radius: 20px;
    margin-bottom: .95rem;
    background: #69b9ee;
}
.df-kpi-label {
    color: #95a2b5 !important;
    font-size: .8rem;
    font-weight: 600;
}
.df-kpi-value {
    color: #f5f7fb !important;
    font-size: 1.9rem;
    font-weight: 800;
    margin-top: .15rem;
}
.df-kpi-note {
    color: #7f8ba0 !important;
    font-size: .72rem;
    margin-top: .3rem;
}

.df-section {
    margin-top: 2.3rem;
    margin-bottom: .9rem;
}
.df-section-label, .df-panel-label {
    color: #69b9ee !important;
    font-size: .68rem;
    font-weight: 800;
    letter-spacing: 1.25px;
}
.df-section-title, .df-panel-title {
    color: #f1f4f8 !important;
    font-size: 1.55rem;
    font-weight: 750;
    margin-top: .18rem;
}
.df-section-text {
    color: #8f9caf !important;
    font-size: .84rem;
    margin-top: .15rem;
}
.df-panel-heading {
    margin-top: 1.65rem;
    margin-bottom: .15rem;
}
.df-panel-title {
    font-size: 1.35rem;
}
.df-badge {
    display: inline-block;
    color: #8bcdf3 !important;
    background: #132638;
    border: 1px solid #24445e;
    border-radius: 100px;
    padding: .28rem .58rem;
    font-size: .68rem;
    font-weight: 750;
    margin-top: .5rem;
}

/* Inventory action */
.df-order {
    background: linear-gradient(135deg, #122234, #111a26);
    border: 1px solid #29415a;
    border-radius: 14px;
    padding: 1.25rem;
    margin-top: 1rem;
}
.df-order-label {
    color: #9aabc0 !important;
    font-size: .78rem;
}
.df-order-value {
    color: #75c8f4 !important;
    font-size: 2.45rem;
    font-weight: 800;
    line-height: 1.1;
    margin-top: .25rem;
}
.df-order-unit {
    color: #77869a !important;
    font-size: .72rem;
}
.df-mini-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: .65rem;
    margin-top: .8rem;
}
.df-mini {
    background: #101720;
    border: 1px solid #263041;
    border-radius: 10px;
    padding: .8rem;
}
.df-mini span {
    display: block;
    color: #8592a5 !important;
    font-size: .7rem;
}
.df-mini strong {
    color: #eef2f7 !important;
    font-size: .96rem;
}

/* Project story cards */
.df-story {
    background: #111822;
    border: 1px solid #263041;
    border-radius: 14px;
    padding: 1.25rem;
    min-height: 170px;
}
.df-story h4 {
    margin-top: 0;
}
.df-story p {
    color: #9ba7b9 !important;
    line-height: 1.6;
}

/* Footer */
.df-footer {
    color: #778398 !important;
    border-top: 1px solid #202a38;
    margin-top: 2.3rem;
    padding-top: 1.2rem;
    font-size: .73rem;
}

hr {
    border-color: #202a38 !important;
}
footer, #MainMenu {
    visibility: hidden;
}

@media (max-width: 900px) {
    .block-container {
        padding-left: 1.2rem;
        padding-right: 1.2rem;
    }
    .df-hero {
        grid-template-columns: 1fr;
    }
    .df-hero-visual {
        display: none;
    }
    .df-hero-title {
        font-size: 2.25rem;
    }
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("Morrow")
st.sidebar.caption("Retail Demand Forecasting")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Forecast Explorer",
        "Inventory Planner",
        "Model Lab",
        "Project Story"
    ]
)


# ============================================================
# OVERVIEW
# ============================================================
if page == "Overview":

    st.markdown("""
    <div class="df-hero">
        <div class="df-hero-content">
            <div class="df-eyebrow">RETAIL DEMAND FORECASTING</div>
            <div class="df-hero-title">
                Forecast Smarter.<br>Replenish Better.
            </div>
            <div class="df-hero-text">
                Forecast retail demand across different demand patterns
                and turn predictive insights into smarter inventory
                replenishment decisions.
            </div>
            <div class="df-tags">
                <span>DeepAR Final Model</span>
                <span>15-Day Forecast</span>
                <span>1,728 Supported Series</span>
            </div>
        </div>
        <div class="df-hero-visual">
            <div class="df-visual-box">
                <div class="df-visual-small">FINAL FORECAST</div>
                <div class="df-visual-number">25,920</div>
                <div class="df-visual-label">forecast rows</div>
                <div class="df-bars">
                    <div style="height:42%"></div>
                    <div style="height:62%"></div>
                    <div style="height:50%"></div>
                    <div style="height:78%"></div>
                    <div style="height:67%"></div>
                    <div style="height:90%"></div>
                    <div style="height:75%"></div>
                    <div style="height:100%"></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown("""
        <div class="df-kpi">
            <div class="df-kpi-accent"></div>
            <div class="df-kpi-label">Total Stores</div>
            <div class="df-kpi-value">54</div>
            <div class="df-kpi-note">Across the retail network</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown("""
        <div class="df-kpi">
            <div class="df-kpi-accent"></div>
            <div class="df-kpi-label">Product Families</div>
            <div class="df-kpi-value">33</div>
            <div class="df-kpi-note">Across 1,728 supported series</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown("""
        <div class="df-kpi">
            <div class="df-kpi-accent"></div>
            <div class="df-kpi-label">Forecast Horizon</div>
            <div class="df-kpi-value">15 Days</div>
            <div class="df-kpi-note">16 Aug – 30 Aug 2017</div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown("""
        <div class="df-kpi">
            <div class="df-kpi-accent"></div>
            <div class="df-kpi-label">Final Model</div>
            <div class="df-kpi-value">DeepAR</div>
            <div class="df-kpi-note">Overall RMSLE · 0.476</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="df-section">
        <div class="df-section-label">FORECAST EXPLORER</div>
        <div class="df-section-title">Explore the Forecast</div>
        <div class="df-section-text">
            Select a store and product family to explore the final 15-day DeepAR forecast.
        </div>
    </div>
    """, unsafe_allow_html=True)

    f1, f2 = st.columns([1, 2])

    with f1:
        selected_store = st.selectbox(
            "Store",
            sorted(forecast["store_nbr"].unique()),
            key="overview_store"
        )

    with f2:
        family_list = sorted(
            forecast[
                forecast["store_nbr"] == selected_store
            ]["family"].unique()
        )
        selected_family = st.selectbox(
            "Product Family",
            family_list,
            key="overview_family"
        )

    selected_forecast = forecast[
        (forecast["store_nbr"] == selected_store) &
        (forecast["family"] == selected_family)
    ].copy()

    selected_replenishment = replenishment[
        (replenishment["store_nbr"] == selected_store) &
        (replenishment["family"] == selected_family)
    ].copy()

    left, right = st.columns([1.55, 1])

    with left:
        st.markdown("""
        <div class="df-panel-heading">
            <div class="df-panel-label">FORECAST</div>
            <div class="df-panel-title">Sales Forecast</div>
            <div class="df-badge">15 DAYS</div>
        </div>
        """, unsafe_allow_html=True)

        st.caption(
            f"Store {selected_store} · {selected_family} · DeepAR"
        )

            
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=selected_forecast["date"],
                y=selected_forecast["deepar_pred"],
                mode="lines+markers",
                line=dict(color="#69b9ee", width=3),
                marker=dict(size=7, color="#69b9ee"),
                fill="tozeroy",
                fillcolor="rgba(105,185,238,0.10)",
                name="DeepAR Forecast"
            )
        )
        fig.update_layout(
            height=365,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#aeb8c8"),
            showlegend=False,
            hovermode="x unified",
            xaxis=dict(showgrid=False, title=""),
            yaxis=dict(
                title="Forecast Demand",
                gridcolor="#263041",
                zeroline=False
            )
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("""
        <div class="df-panel-heading">
            <div class="df-panel-label">INVENTORY PLANNING</div>
            <div class="df-panel-title">Inventory Action</div>
        </div>
        """, unsafe_allow_html=True)

        st.caption("Replenishment recommendation for the current selection")

        if not selected_replenishment.empty:
            row = selected_replenishment.iloc[0]

            st.markdown(f"""
            <div class="df-order">
                <div class="df-order-label">Recommended Order</div>
                <div class="df-order-value">{row['recommended_order_qty']:,.0f}</div>
                <div class="df-order-unit">units</div>
            </div>
            <div class="df-mini-grid">
                <div class="df-mini">
                    <span>Forecast Demand</span>
                    <strong>{row['forecast_demand']:,.0f}</strong>
                </div>
                <div class="df-mini">
                    <span>Average Daily</span>
                    <strong>{row['average_daily_demand']:,.1f}</strong>
                </div>
                <div class="df-mini">
                    <span>Lead-Time Demand</span>
                    <strong>{row['lead_time_demand']:,.0f}</strong>
                </div>
                <div class="df-mini">
                    <span>Safety Stock</span>
                    <strong>{row['safety_stock']:,.0f}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info(
                "No replenishment recommendation is available for this selection."
            )

    left2, right2 = st.columns([1.15, 1])

    with left2:
        st.markdown("""
        <div class="df-panel-heading">
            <div class="df-panel-label">INVENTORY PRIORITIES</div>
            <div class="df-panel-title">Top Replenishment Priorities</div>
        </div>
        """, unsafe_allow_html=True)
        st.caption("Highest recommended order quantities")

        top = (
            replenishment
            .sort_values("recommended_order_qty", ascending=False)
            .head(5)[["store_nbr", "family", "recommended_order_qty"]]
            .copy()
        )
        top.columns = ["Store", "Product Family", "Recommended Order"]
        st.dataframe(top, use_container_width=True, hide_index=True)

    with right2:
        st.markdown("""
        <div class="df-panel-heading">
            <div class="df-panel-label">MODEL PERFORMANCE</div>
            <div class="df-panel-title">Model Comparison</div>
        </div>
        """, unsafe_allow_html=True)
        st.caption("Overall validation RMSLE · Lower is better")

        model_chart = model_comparison.sort_values(
            "RMSLE", ascending=False
        )

        colors = [
            "#69b9ee" if model == "DeepAR" else "#344154"
            for model in model_chart["Model"]
        ]

        fig_models = go.Figure()
        fig_models.add_trace(
            go.Bar(
                x=model_chart["RMSLE"],
                y=model_chart["Model"],
                orientation="h",
                marker_color=colors,
                text=model_chart["RMSLE"].round(3),
                textposition="outside"
            )
        )
        fig_models.update_layout(
            height=330,
            margin=dict(l=10, r=55, t=10, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#aeb8c8"),
            showlegend=False,
            xaxis=dict(
                title="RMSLE",
                gridcolor="#263041",
                zeroline=False
            ),
            yaxis=dict(title="", showgrid=False)
        )
        st.plotly_chart(fig_models, use_container_width=True)


# ============================================================
# FORECAST EXPLORER
# ============================================================
elif page == "Forecast Explorer":

    st.caption("FORECAST ANALYSIS")
    st.title("Forecast Explorer")
    st.write(
    "Explore DeepAR validation performance and the final 15-day forecast "
    "by store and product family."
    )
    forecast_mode = st.radio(
    "Forecast Mode",
    ["Validation", "Final Forecast"],
    horizontal=True,
    key="forecast_mode"
    )
    
    if forecast_mode == "Validation":
        active_data = validation
    else:
        active_data = forecast

    col1, col2 = st.columns([1, 2])

    with col1:
        selected_store = st.selectbox(
            "Select Store",
            sorted(active_data["store_nbr"].unique()),
            key="forecast_store"
        )

    with col2:
        selected_family = st.selectbox(
            "Select Product Family",
            sorted(
                active_data[
                    active_data["store_nbr"] == selected_store
                ]["family"].unique()
            ),
            key="forecast_family"
        )

    selected_forecast = active_data[
        (active_data["store_nbr"] == selected_store) &
        (active_data["family"] == selected_family)
    ].copy()

    selected_replenishment = replenishment[
        (replenishment["store_nbr"] == selected_store) &
        (replenishment["family"] == selected_family)
    ].copy()

    if forecast_mode == "Validation":
        import numpy as np

        actual = selected_forecast["sales"]
        pred = selected_forecast["deepar_pred"]

        rmsle = np.sqrt(
            np.mean(
                (np.log1p(pred.clip(lower=0)) -
                 np.log1p(actual.clip(lower=0))) ** 2
            )
        )

        mae = np.mean(np.abs(actual - pred))
        rmse = np.sqrt(np.mean((actual - pred) ** 2))

        wmape = (
            np.sum(np.abs(actual - pred)) / actual.sum() * 100
            if actual.sum() != 0 else 0
        )

        pattern = selected_forecast["pattern"].iloc[0]

        m1, m2, m3, m4, m5 = st.columns(5)

        with m1:
            st.metric("Demand Pattern", pattern)

        with m2:
            st.metric("RMSLE", f"{rmsle:.4f}")

        with m3:
            st.metric("MAE", f"{mae:.2f}")

        with m4:
            st.metric("RMSE", f"{rmse:.2f}")

        with m5:
            st.metric("WMAPE", f"{wmape:.2f}%")

    else:
        if not selected_replenishment.empty:
            row = selected_replenishment.iloc[0]

            m1, m2, m3 = st.columns(3)

            with m1:
                st.metric(
                    "15-Day Demand",
                    f"{row['forecast_demand']:,.0f}"
                )

            with m2:
                st.metric(
                    "Average Daily Demand",
                    f"{row['average_daily_demand']:,.1f}"
                )

            with m3:
                st.metric(
                    "Maximum Daily Demand",
                    f"{row['max_daily_demand']:,.1f}"
                )

    fig = go.Figure()

    if forecast_mode == "Validation":
        fig.add_trace(
            go.Scatter(
                x=selected_forecast["date"],
                y=selected_forecast["sales"],
                mode="lines+markers",
                name="Actual Sales"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=selected_forecast["date"],
                y=selected_forecast["deepar_pred"],
                mode="lines+markers",
                name="DeepAR Prediction"
            )
        )

    else:
        fig.add_trace(
            go.Scatter(
                x=selected_forecast["date"],
                y=selected_forecast["deepar_pred"],
                mode="lines+markers",
                line=dict(color="#69b9ee", width=3),
                marker=dict(size=8, color="#69b9ee"),
                fill="tozeroy",
                fillcolor="rgba(105,185,238,0.10)",
                name="DeepAR Forecast"
            )
        )
    
    fig.update_layout(
        height=450,
        margin=dict(l=20, r=20, t=25, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#aeb8c8"),
        showlegend=False,
        hovermode="x unified",
        xaxis=dict(title="Date", showgrid=False),
        yaxis=dict(title="Forecast Demand", gridcolor="#263041")
    )
    st.plotly_chart(fig, use_container_width=True)

    forecast_table = selected_forecast.copy()
    forecast_table["date"] = forecast_table["date"].dt.strftime("%d %b %Y")

    if forecast_mode == "Validation":
        forecast_table["deepar_pred"] = forecast_table["deepar_pred"].round(2)
        forecast_table["sales"] = forecast_table["sales"].round(2)
        forecast_table["prediction_error"] = forecast_table["prediction_error"].round(2)

        forecast_table = forecast_table[
            [
                "date",
                "store_nbr",
                "family",
                "sales",
                "deepar_pred",
                "prediction_error",
                "pattern"
            ]
        ].rename(
            columns={
                "date": "Date",
                "store_nbr": "Store",
                "family": "Product Family",
                "sales": "Actual Sales",
                "deepar_pred": "DeepAR Prediction",
                "prediction_error": "Prediction Error",
                "pattern": "Demand Pattern"
            }
        )

    else:
        forecast_table["deepar_pred"] = forecast_table["deepar_pred"].round(2)

        forecast_table = forecast_table[
            ["date", "store_nbr", "family", "deepar_pred"]
        ].rename(
            columns={
                "date": "Date",
                "store_nbr": "Store",
                "family": "Product Family",
                "deepar_pred": "Forecast Demand"
            }
        )

    if forecast_mode == "Validation":
        st.subheader("Validation Results · Actual vs Predicted")
    else:
        st.subheader("15-Day Forecast Results")
        
    st.dataframe(
        forecast_table,
        use_container_width=True,
        hide_index=True
    )

    csv = forecast_table.to_csv(index=False).encode("utf-8")
    safe_family = (
        str(selected_family)
        .replace("/", "_")
        .replace(" ", "_")
    )

    st.download_button(
        "Download Forecast CSV",
        data=csv,
        file_name=f"forecast_store_{selected_store}_{safe_family}.csv",
        mime="text/csv"
    )


# ============================================================
# INVENTORY PLANNER
# ============================================================
elif page == "Inventory Planner":

    st.caption("INVENTORY PLANNING")
    st.title("Replenishment Planner")
    st.write(
        "Translate forecast demand into actionable inventory recommendations."
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        selected_store = st.selectbox(
            "Select Store",
            sorted(replenishment["store_nbr"].unique()),
            key="inventory_store"
        )

    with col2:
        selected_family = st.selectbox(
            "Select Product Family",
            sorted(
                replenishment[
                    replenishment["store_nbr"] == selected_store
                ]["family"].unique()
            ),
            key="inventory_family"
        )

    selection = replenishment[
        (replenishment["store_nbr"] == selected_store) &
        (replenishment["family"] == selected_family)
    ]

    if not selection.empty:
        row = selection.iloc[0]
        gross_requirement = float(row["recommended_order_qty"])

        current_stock = st.number_input(
            "Current Stock",
            min_value=0.0,
            value=0.0,
            step=1.0,
            key="current_stock"
        )

        net_order_qty = max(gross_requirement - current_stock, 0)    
        st.caption(
            f"Gross Replenishment Requirement: {gross_requirement:,.0f} units  •  "
            f"Current Stock: {current_stock:,.0f} units  •  "
            f"Net Order Quantity: {net_order_qty:,.0f} units"
        )   
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Forecast Demand",
                f"{row['forecast_demand']:,.0f}"
            )
        with c2:
            st.metric(
                "Lead-Time Demand",
                f"{row['lead_time_demand']:,.0f}"
            )
        with c3:
            st.metric(
                "Safety Stock",
                f"{row['safety_stock']:,.0f}"
            )
        with c4:
            st.metric(
                "Net Order Quantity",
                f"{net_order_qty:,.0f}"
        )

    st.info(
        "Gross replenishment uses a 3-day lead time and 20% safety stock. "
        "Current stock is entered manually and deducted to calculate the Net Order Quantity."
    )

    st.subheader("Top Replenishment Priorities")

    top_orders = replenishment.sort_values(
        "recommended_order_qty",
        ascending=False
    ).head(10).copy()

    top_orders = top_orders.rename(
        columns={
            "store_nbr": "Store",
            "family": "Product Family",
            "forecast_demand": "Forecast Demand",
            "average_daily_demand": "Average Daily Demand",
            "max_daily_demand": "Maximum Daily Demand",
            "lead_time_demand": "Lead-Time Demand",
            "safety_stock": "Safety Stock",
            "recommended_order_qty": "Recommended Order"
        }
    )

    st.dataframe(
        top_orders,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# MODEL LAB
# ============================================================
elif page == "Model Lab":

    st.caption("MODEL PERFORMANCE")
    st.title("Model Lab")
    st.write(
        "Compare forecasting performance overall and across demand patterns."
    )

    model_display = model_comparison.copy()
    model_display["RMSLE"] = model_display["RMSLE"].round(3)
    model_display["MAE"] = model_display["MAE"].round(2)
    model_display["RMSE"] = model_display["RMSE"].round(2)
    model_display["WMAPE"] = model_display["WMAPE"].round(2)

    chart_col, table_col = st.columns([1.15, 1])

    with chart_col:
        st.subheader("Overall Model Comparison")

        sorted_models = model_comparison.sort_values(
            "RMSLE", ascending=False
        )
        colors = [
            "#69b9ee" if model == "DeepAR" else "#344154"
            for model in sorted_models["Model"]
        ]

        fig_models = go.Figure()
        fig_models.add_trace(
            go.Bar(
                x=sorted_models["RMSLE"],
                y=sorted_models["Model"],
                orientation="h",
                marker_color=colors,
                text=sorted_models["RMSLE"].round(3),
                textposition="outside"
            )
        )
        fig_models.update_layout(
            height=390,
            margin=dict(l=10, r=50, t=20, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#aeb8c8"),
            showlegend=False,
            xaxis=dict(
                title="RMSLE · Lower is Better",
                gridcolor="#263041"
            ),
            yaxis=dict(title="", showgrid=False)
        )
        st.plotly_chart(fig_models, use_container_width=True)

    with table_col:
        st.subheader("Validation Metrics")
        st.dataframe(
            model_display,
            use_container_width=True,
            hide_index=True,
            height=340
        )

    st.subheader("Performance by Demand Pattern")
    st.caption(
        "RMSLE across Regular, Intermittent and Irregular demand."
    )

    pattern_colors = {
        "DeepAR": "#69b9ee",
        "XGBoost Tuned": "#76dda7",
        "LightGBM Tuned": "#8d83f4",
        "LightGBM": "#465267",
        "XGBoost": "#56657b",
        "Seasonal Naive": "#303b4d"
    }

    fig_patterns = go.Figure()

    for model in pattern_metrics["Model"].unique():
        model_data = pattern_metrics[
            pattern_metrics["Model"] == model
        ]
        fig_patterns.add_trace(
            go.Bar(
                x=model_data["Pattern"],
                y=model_data["RMSLE"],
                name=model,
                marker_color=pattern_colors.get(model, "#465267")
            )
        )

    fig_patterns.update_layout(
        height=450,
        barmode="group",
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#aeb8c8"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        ),
        xaxis=dict(title="Demand Pattern", showgrid=False),
        yaxis=dict(title="RMSLE", gridcolor="#263041")
    )

    st.plotly_chart(fig_patterns, use_container_width=True)

    st.info(
        "DeepAR achieved the lowest RMSLE for Regular and Intermittent "
        "demand, while XGBoost Tuned achieved the lowest RMSLE for "
        "Irregular demand."
    )


# ============================================================
# PROJECT STORY
# ============================================================
elif page == "Project Story":

    st.caption("PROJECT OVERVIEW")
    st.title("Morrow")
    st.write(
        "Retail demand forecasting across different demand patterns "
        "using classical, machine learning, and deep learning models."
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Supported Series", "1,728")
    with c2:
        st.metric("Final Forecast Rows", "25,920")
    with c3:
        st.metric("Forecast Horizon", "15 Days")

    st.markdown("<br>", unsafe_allow_html=True)

    s1, s2 = st.columns(2)

    with s1:
        st.markdown("""
        <div class="df-story">
            <h4>Business Goal</h4>
            <p>
                Forecast retail demand across store and product-family
                combinations and support smarter inventory replenishment
                decisions.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with s2:
        st.markdown("""
        <div class="df-story">
            <h4>Final Forecast</h4>
            <p>
                DeepAR is the final forecasting model. The final forecast
                covers 16–30 August 2017 across 1,728 supported series.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    s3, s4 = st.columns(2)

    with s3:
        st.markdown("""
        <div class="df-story">
            <h4>Model Evaluation</h4>
            <p>
                RMSLE is the primary evaluation metric, supported by
                MAE, RMSE and WMAPE. Performance is also evaluated
                across Regular, Intermittent and Irregular demand.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with s4:
        st.markdown("""
        <div class="df-story">
            <h4>Replenishment Logic</h4>
            <p>
                Recommendations use a 3-day lead time and 20% safety
                stock based on expected lead-time demand. Current stock
                can be entered manually in the Inventory Planner and is
                deducted to calculate the Net Order Quantity.
            </p>
        </div>
        """, unsafe_allow_html=True)


# -----------------------------
# Footer
# -----------------------------
st.markdown("""
<div class="df-footer">
    Morrow · Retail Demand Forecasting · DeepAR Final Model ·
    15-Day Forecast Horizon
</div>
""", unsafe_allow_html=True)
