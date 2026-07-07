import os
import pandas as pd
import streamlit as st
import plotly.express as px


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Climate Risk & Weather Trend Analytics Platform",
    page_icon="🌍",
    layout="wide"
)


# --------------------------------------------------
# Custom CSS
# --------------------------------------------------
def load_custom_css():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #f4fbf8 0%, #eef7ff 45%, #ffffff 100%);
            color: #1f2937;
        }

        .block-container {
            padding-top: 0.7rem;
            padding-bottom: 0.6rem;
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: 1450px;
        }

        h1 {
            color: #0f766e;
            font-weight: 850;
            letter-spacing: -0.6px;
            margin-bottom: 0.1rem;
            font-size: 2.5rem !important;

        }

        h2, h3 {
            color: #134e4a;
            font-weight: 750;
        }

        div[data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.95);
            border: 1px solid rgba(15, 118, 110, 0.15);
            padding: 0.55rem 0.8rem;
            border-radius: 14px;
            box-shadow: 0 5px 14px rgba(15, 118, 110, 0.07);
        }

        div[data-testid="stMetricLabel"] {
            font-size: 0.9rem;
            color: #475569;
            font-weight: 650;
        }

        div[data-testid="stMetricValue"] {
            font-size: 1.5rem;
            color: #0f766e;
            font-weight: 850;
        }

        div[data-testid="stPlotlyChart"] {
            background: rgba(255, 255, 255, 0.96);
            border-radius: 16px;
            padding: 0.5rem;
            border: 1px solid rgba(15, 118, 110, 0.12);
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
        }
           
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f766e 0%, #115e59 100%);
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] span {
            color: #ffffff !important;
        }

        /* Selectbox main box */
        section[data-testid="stSidebar"] div[data-baseweb="select"] {
            background-color: #ffffff !important;
            border-radius: 10px !important;
        }

        section[data-testid="stSidebar"] div[data-baseweb="select"] * {
            color: #111827 !important;
        }

        /* Date input box */
        section[data-testid="stSidebar"] input {
            background-color: #ffffff !important;
            color: #111827 !important;
            border-radius: 8px !important;
        }

        /* Dropdown menu options */
        div[data-baseweb="popover"] {
            background-color: #ffffff !important;
        }

        div[data-baseweb="popover"] * {
            color: #111827 !important;
        }

        /* Selectbox arrow/icon */
        section[data-testid="stSidebar"] svg {
            fill: #111827 !important;
            color: #111827 !important;
        }
        .section-banner {
            background: linear-gradient(90deg, #ccfbf1 0%, #e0f2fe 100%);
            border-left: 5px solid #0f766e;
            padding: 0.55rem 0.85rem;
            border-radius: 12px;
            margin: 0.75rem 0 0.55rem 0;
            font-weight: 800;
            color: #134e4a;
            box-shadow: 0 3px 10px rgba(15, 118, 110, 0.07);
            font-size: 1.2rem;
        }

        .forecast-banner {
            background: linear-gradient(90deg, #fef3c7 0%, #fffbeb 100%);
            border-left: 5px solid #f59e0b;
            padding: 0.55rem 0.85rem;
            border-radius: 12px;
            margin: 0.75rem 0 0.55rem 0;
            font-weight: 800;
            color: #92400e;
            box-shadow: 0 3px 10px rgba(245, 158, 11, 0.08);
            font-size: 1.2rem;
        }
        


        .insight-card {
            background: rgba(255, 255, 255, 0.96);
            border: 1px solid rgba(15, 118, 110, 0.14);
            border-radius: 16px;
            padding: 1rem 1.2rem;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
            font-size: 1.3rem;
            line-height: 1.55;
        }

        .small-caption {
            color: #64748b;
            font-size: 0.9rem;
            margin-top: -0.4rem;
            margin-bottom: 0.8rem;
        }

        hr {
            margin: 0.7rem 0 1rem 0;
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, #99f6e4, transparent);
        }

        #MainMenu, footer, header {
            visibility: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


load_custom_css()


# --------------------------------------------------
# Load Dataset
# --------------------------------------------------
@st.cache_data
def load_data():
    file_path = "data/processed/climate_weather_processed.csv"

    if not os.path.exists(file_path):
        st.error("Processed dataset not found. Please check the file path.")
        st.stop()

    data = pd.read_csv(file_path)
    data["date"] = pd.to_datetime(data["date"])

    return data


df = load_data()


# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------
st.sidebar.header("🔎 Filters")

city_options = sorted(df["city"].unique())
selected_city = st.sidebar.selectbox("Select City", city_options)

city_full_df = df[df["city"] == selected_city].copy()

min_date = city_full_df["date"].min()
max_date = city_full_df["date"].max()



forecast_days = st.sidebar.selectbox(
    "Forecast Period",
    options=[30, 90, 180, 365],
    index=2
)

city_df = city_full_df.copy()


# --------------------------------------------------
# Header
# --------------------------------------------------
st.title("🌍 Climate Risk & Weather Trend Analytics Platform")
st.markdown(
    "<p class='small-caption'>Executive dashboard for temperature trends, rainfall behavior, climate-risk detection, city comparison, and seasonal forecasting.</p>",
    unsafe_allow_html=True
)

st.markdown("---")


# --------------------------------------------------
# KPI Cards
# --------------------------------------------------
avg_temp = city_df["temperature_avg"].mean()
total_rainfall = city_df["rainfall"].sum()
heat_risk_days = int(city_df["heat_risk_day"].sum())
avg_risk_score = city_df["daily_climate_risk_score"].mean()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric("Average Temperature", f"{avg_temp:.1f} °C")

with kpi2:
    st.metric("Total Rainfall", f"{total_rainfall:,.0f} mm")

with kpi3:
    st.metric("Heat-Risk Days", f"{heat_risk_days:,} days")

with kpi4:
    st.metric("Climate Risk Score", f"{avg_risk_score:.1f}/100")


# --------------------------------------------------
# Seasonal Forecasting Section
# --------------------------------------------------
st.markdown(
    "<div class='forecast-banner'>🔮 Seasonal Forecasting — Future Climate Pattern Estimate</div>",
    unsafe_allow_html=True
)
forecast_start_date = city_full_df["date"].max() + pd.Timedelta(days=1)

future_dates = pd.date_range(
    start=forecast_start_date,
    periods=forecast_days
)
future_df = pd.DataFrame({"date": future_dates})
future_df["month"] = future_df["date"].dt.month
future_df["day"] = future_df["date"].dt.day

historical_pattern = city_full_df.copy()
historical_pattern["month"] = historical_pattern["date"].dt.month
historical_pattern["day"] = historical_pattern["date"].dt.day

recent_history = city_full_df[
    city_full_df["date"] >= city_full_df["date"].max() - pd.Timedelta(days=180)
]

# --------------------------------------------------
# Temperature Forecast Data
# --------------------------------------------------
temperature_lookup = (
    historical_pattern
    .groupby(["month", "day"])["temperature_avg"]
    .mean()
    .reset_index()
)
future_temp_df = future_df.merge(
    temperature_lookup,
    on=["month", "day"],
    how="left"
)

future_temp_df = future_temp_df.rename(
    columns={"temperature_avg": "forecast_temperature"}
)
historical_temp = recent_history[["date", "temperature_avg"]].rename(
    columns={"temperature_avg": "temperature"}
)
historical_temp["type"] = "Historical"

forecast_temp = future_temp_df[["date", "forecast_temperature"]].rename(
    columns={"forecast_temperature": "temperature"}
)
forecast_temp["type"] = "Forecast"

temp_forecast_plot = pd.concat(
    [historical_temp, forecast_temp],
    ignore_index=True
)

# ----------------------------------
# Rainfall Forecast Data
#----------------------------------
rainfall_lookup = (
    historical_pattern
    .groupby(["month", "day"])["rainfall"]
    .mean()
    .reset_index()
)

future_rain_df = future_df.merge(
    rainfall_lookup,
    on=["month", "day"],
    how="left"
)
future_rain_df = future_rain_df.rename(
    columns={"rainfall": "forecast_rainfall"}
)

future_rain_df["forecast_rainfall"] = future_rain_df["forecast_rainfall"].clip(lower=0)

historical_rain = recent_history[["date", "rainfall"]].rename(
    columns={"rainfall": "rainfall_value"}
)
historical_rain["type"] = "Historical"

forecast_rain = future_rain_df[["date", "forecast_rainfall"]].rename(
    columns={"forecast_rainfall": "rainfall_value"}
)
forecast_rain["type"] = "Forecast"

rain_forecast_plot = pd.concat(
    [historical_rain, forecast_rain],
    ignore_index=True
)

#---------------------------------------------------
# Forecast Charts
#--------------------------------------------------
forecast_col1, forecast_col2 = st.columns(2)

with forecast_col1:
    forecast_temp_fig = px.line(
        temp_forecast_plot,
        x="date",
        y="temperature",
        color="type",
        line_dash="type",
        title=f"Next {forecast_days} Days Temperature Forecast - {selected_city}",
        labels={
            "date": "Date",
            "temperature": "Avg Temperature (°C)",
            "type": "Data Type"
        }
    )

    forecast_temp_fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=25),
        title_x=0.02,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    st.plotly_chart(
        forecast_temp_fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )
with forecast_col2:
    forecast_rain_fig = px.line(
        rain_forecast_plot,
        x="date",
        y="rainfall_value",
        color="type",
        line_dash="type",
        title=f"Next {forecast_days} Days Rainfall Forecast - {selected_city}",
        labels={
            "date": "Date",
            "rainfall_value": "Rainfall (mm)",
            "type": "Data Type"
        }
    )
    forecast_rain_fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=25),
        title_x=0.02,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    st.plotly_chart(
        forecast_rain_fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# ----------------------------------------------------
# Key Insights Summary
# -----------------------------------------------------

st.markdown(
    "<div class='section-banner'>🧠 Key Insights Summary</div>",
    unsafe_allow_html=True
)
hottest_month = (
        city_df.groupby(["month", "month_name"], as_index=False)
        .agg(avg_temperature=("temperature_avg", "mean"))
        .sort_values("avg_temperature", ascending=False)
        .iloc[0]["month_name"]
    )

wettest_month = (
        city_df.groupby(["month", "month_name"], as_index=False)
        .agg(total_rainfall=("rainfall", "sum"))
        .sort_values("total_rainfall", ascending=False)
        .iloc[0]["month_name"]
    )

heavy_rain_days = int(city_df["heavy_rain_day"].sum())
very_hot_days = int(city_df["very_hot_day"].sum())
dry_days = int(city_df["dry_day"].sum())
common_risk_level = city_df["risk_level"].mode()[0]

insight_col1, insight_col2, insight_col3 = st.columns(3)

with insight_col1:
    st.markdown(
        f"""
        <div class="insight-card">
            <h3>🌡️ Temperature Insight</h3>
            <p>
                <b>{selected_city}</b> recorded an average temperature of 
                <b>{avg_temp:.1f}°C</b>.
            </p>
            <p>
                The hottest monthly pattern appears around <b>{hottest_month}</b>.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
with insight_col2:
    st.markdown(
        f"""
        <div class="insight-card">
            <h3>🌧️ Rainfall Insight</h3>
            <p>
                Total rainfall during the selected period reached 
                <b>{total_rainfall:,.0f} mm</b>.
            </p>
            <p>
                The wettest monthly pattern appears around <b>{wettest_month}</b>.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
with insight_col3:
    st.markdown(
        f"""
        <div class="insight-card">
            <h3>🚨 Risk Insight</h3>
            <p>
                The city recorded <b>{heat_risk_days}</b> heat-risk days, 
                <b>{very_hot_days}</b> very-hot days, and 
                <b>{heavy_rain_days}</b> heavy-rain days.
            </p>
            <p>
                The most common daily risk level is <b>{common_risk_level}</b>.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
# --------------------------------------------------
# Main Trend Charts
# --------------------------------------------------
st.markdown(
    "<div class='section-banner'>📊 Historical Climate Trend Analysis</div>",
    unsafe_allow_html=True
)
trend_col1, trend_col2 = st.columns(2)

with trend_col1:
    temp_fig = px.line(
        city_df,
        x="date",
        y="temperature_avg",
        title=f"Temperature Trend - {selected_city}",
        labels={
            "date": "Date",
            "temperature_avg": "Avg Temperature (°C)"
        }
    )

    temp_fig.update_layout(
        height=300,
        margin=dict(l=15, r=15, t=40, b=15),
        title_x=0.02
    )

    st.plotly_chart(
    temp_fig,
    use_container_width=True,
    config={"displayModeBar": False}
)


with trend_col2:
    monthly_rainfall = (
        city_df.groupby(["month", "month_name"], as_index=False)
        .agg(total_rainfall=("rainfall", "sum"))
        .sort_values("month")
    )

    rainfall_fig = px.bar(
        monthly_rainfall,
        x="month_name",
        y="total_rainfall",
        title=f"Monthly Rainfall Pattern - {selected_city}",
        labels={
            "month_name": "Month",
            "total_rainfall": "Rainfall (mm)"
        }
    )

    rainfall_fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=45, b=20),
        title_x=0.02
    )
    st.plotly_chart(
    rainfall_fig,
    use_container_width=True,
    config={"displayModeBar": False}
)
    


# --------------------------------------------------
# Risk + Forecast Section
# --------------------------------------------------
st.markdown(
    "<div class='section-banner'>🚨 Climate Risk Detection & City Comparison</div>",
    unsafe_allow_html=True
)
risk_col, comparison_col  = st.columns(2)

with risk_col:
    risk_level_summary = (
        city_df["risk_level"]
        .value_counts()
        .reset_index()
    )
    risk_level_summary.columns = ["risk_level", "number_of_days"]

    risk_order = ["Low", "Moderate", "High"]
    risk_level_summary["risk_level"] = pd.Categorical(
        risk_level_summary["risk_level"],
        categories=risk_order,
        ordered=True
    )
    risk_level_summary = risk_level_summary.sort_values("risk_level")

    risk_fig = px.bar(
        risk_level_summary,
        x="risk_level",
        y="number_of_days",
        title=f"Risk Level Distribution - {selected_city}",
        labels={
            "risk_level": "Risk Level",
            "number_of_days": "Days"
        }
    )

    risk_fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=45, b=20),
        title_x=0.02
    )

    st.plotly_chart(
    risk_fig,
    use_container_width=True,
    config={"displayModeBar": False}
)

with comparison_col:
    city_comparison = (
        df.groupby("city", as_index=False)
        .agg(
            avg_risk_score=("daily_climate_risk_score", "mean"),
            heat_risk_days=("heat_risk_day", "sum"),
            total_rainfall=("rainfall", "sum")
        )
    )

    city_comparison["avg_risk_score"] = city_comparison["avg_risk_score"].round(2)

    city_risk_fig = px.bar(
        city_comparison.sort_values("avg_risk_score", ascending=False),
        x="city",
        y="avg_risk_score",
        title="City Climate Risk Ranking",
        labels={
            "city": "City",
            "avg_risk_score": "Avg Risk Score"
        }
    )

    city_risk_fig.update_layout(
        height=300,
        margin=dict(l=15, r=15, t=40, b=15),
        title_x=0.02
    )

    st.plotly_chart(
    city_risk_fig,
    use_container_width=True,
    config={"displayModeBar": False}
)


# --------------------------------------------------
# Detailed Analysis Expander
# --------------------------------------------------
with st.expander("View Detailed Data & Extra Analysis"):
    st.subheader("Filtered Dataset")
    st.dataframe(city_df.head(100), use_container_width=True)

    st.subheader("City Comparison Table")
    st.dataframe(city_comparison, use_container_width=True)

    rainfall_lookup = (
        historical_pattern
        .groupby(["month", "day"])["rainfall"]
        .mean()
        .reset_index()
    )

    future_rain_df = future_df.merge(
        rainfall_lookup,
        on=["month", "day"],
        how="left"
    )

    future_rain_df = future_rain_df.rename(
        columns={"rainfall": "forecast_rainfall"}
    )
    future_rain_df["forecast_rainfall"] = future_rain_df["forecast_rainfall"].clip(lower=0)

    historical_rain = recent_history[["date", "rainfall"]].rename(
        columns={"rainfall": "rainfall_value"}
    )
    historical_rain["type"] = "Historical"

    forecast_rain = future_rain_df[["date", "forecast_rainfall"]].rename(
        columns={"forecast_rainfall": "rainfall_value"}
    )
    forecast_rain["type"] = "Forecast"

    rainfall_forecast_plot = pd.concat(
        [historical_rain, forecast_rain],
        ignore_index=True
    )

    rainfall_forecast_fig = px.line(
        rainfall_forecast_plot,
        x="date",
        y="rainfall_value",
        color="type",
        title=f"Seasonal Rainfall Forecast - {selected_city}",
        labels={
            "date": "Date",
            "rainfall_value": "Rainfall (mm)",
            "type": "Data"
        }
    )

    rainfall_forecast_fig.update_layout(
        height=250,
        title_x=0.02
    )

    st.plotly_chart(rainfall_forecast_fig, use_container_width=True)


# --------------------------------------------------
# Footer Note
# --------------------------------------------------
st.caption(
    "Forecasting method: Seasonal baseline forecasting. Future values are estimated using historical averages for the same month and day. Results should be interpreted as climate-pattern estimates, not exact daily weather predictions."
)