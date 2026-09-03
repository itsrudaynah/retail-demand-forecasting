
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

st.set_page_config(
    page_title="Retail Demand Forecasting",
    layout="wide"
)

# Load data
historical = pd.read_csv("clean_sample.csv", parse_dates=["date"])
validation = pd.read_csv("validation_results.csv", parse_dates=["date"])
forecast = pd.read_csv("forward_forecast_15d.csv", parse_dates=["date"])

# Header
st.title("Retail Demand Forecasting")
st.subheader("15-Day Forecasting Prototype")

st.write("Store 1 × BEVERAGES")
st.write(
    "This prototype demonstrates demand forecasting using "
    "Seasonal Naive and XGBoost."
)

st.divider()

# Prototype information
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Store", "1")

with col2:
    st.metric("Product Family", "BEVERAGES")

with col3:
    st.metric("Forecast Horizon", "15 Days")

# Model performance
st.subheader("Model Performance")

def calculate_metrics(actual, predicted):
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    wmape = (
        np.sum(np.abs(actual - predicted))
        / np.sum(np.abs(actual))
        * 100
    )
    return mae, rmse, wmape

baseline_mae, baseline_rmse, baseline_wmape = calculate_metrics(
    validation["sales"],
    validation["baseline_pred"]
)

xgb_mae, xgb_rmse, xgb_wmape = calculate_metrics(
    validation["sales"],
    validation["xgb_pred"]
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Seasonal Naive")
    st.metric("MAE", f"{baseline_mae:.2f}")
    st.metric("RMSE", f"{baseline_rmse:.2f}")
    st.metric("WMAPE", f"{baseline_wmape:.2f}%")

with col2:
    st.markdown("#### XGBoost")
    st.metric("MAE", f"{xgb_mae:.2f}")
    st.metric("RMSE", f"{xgb_rmse:.2f}")
    st.metric("WMAPE", f"{xgb_wmape:.2f}%")

st.success(
    "XGBoost reduced WMAPE from "
    f"{baseline_wmape:.2f}% to {xgb_wmape:.2f}%."
)
# Forecast visualization
st.divider()
st.subheader("Forecast Visualization")

historical_plot = historical[
    historical["date"] >= validation["date"].min() - pd.Timedelta(days=90)
]

fig = go.Figure()

# Historical sales before validation
historical_before_validation = historical_plot[
    historical_plot["date"] < validation["date"].min()
]

fig.add_trace(
    go.Scatter(
        x=historical_before_validation["date"],
        y=historical_before_validation["sales"],
        mode="lines",
        name="Historical Sales"
    )
)

# Actual sales during validation
fig.add_trace(
    go.Scatter(
        x=validation["date"],
        y=validation["sales"],
        mode="lines",
        name="Actual Sales (Validation)",
        line=dict(width=3)
    )
)

# Seasonal Naive validation
fig.add_trace(
    go.Scatter(
        x=validation["date"],
        y=validation["baseline_pred"],
        mode="lines",
        name="Seasonal Naive (Validation)",
        line=dict(dash="dash")
    )
)

# XGBoost validation
fig.add_trace(
    go.Scatter(
        x=validation["date"],
        y=validation["xgb_pred"],
        mode="lines",
        name="XGBoost (Validation)",
        line=dict(dash="dash")
    )
)

# XGBoost future forecast
fig.add_trace(
    go.Scatter(
        x=forecast["date"],
        y=forecast["xgb_pred"],
        mode="lines",
        name="XGBoost Forecast (Next 15 Days)",
        line=dict(dash="dash")
    )
)

# Validation period
fig.add_vrect(
    x0=validation["date"].min(),
    x1=validation["date"].max(),
    opacity=0.10,
    layer="below",
    line_width=0,
    annotation_text="Validation"
)

# Forecast period
fig.add_vrect(
    x0=forecast["date"].min(),
    x1=forecast["date"].max(),
    opacity=0.08,
    layer="below",
    line_width=0,
    annotation_text="Forecast"
)

fig.update_layout(
    title="Store 1 — BEVERAGES: Validation and 15-Day Forecast",
    xaxis_title="Date",
    yaxis_title="Sales",
    hovermode="x unified",
    height=550,
    legend_title="Series"
)

st.plotly_chart(fig, use_container_width=True)
st.divider()
st.subheader("15-Day Forecast Results")

forecast_table = forecast[["date", "xgb_pred"]].copy()
forecast_table.columns = ["Date", "Forecasted Sales"]

forecast_table["Date"] = forecast_table["Date"].dt.strftime("%Y-%m-%d")
forecast_table["Forecasted Sales"] = forecast_table["Forecasted Sales"].round(0).astype(int)

st.dataframe(
    forecast_table,
    use_container_width=True,
    hide_index=True
)

st.download_button(
    label="Download Forecast CSV",
    data=forecast_table.to_csv(index=False),
    file_name="15_day_demand_forecast.csv",
    mime="text/csv"
)
