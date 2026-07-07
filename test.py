import streamlit as st
import pandas as pd
import plotly.express as px
import os



# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Climate Risk & Weather Trend Analytics Platform",
    page_icon="🌍",
    layout="wide"
)


# --------------------------------------------------
# Load Dataset
# --------------------------------------------------
@st.cache_data
def load_data():
    file_path = "data/processed/climate_weather_processed.csv"

    if not os.path.exists(file_path):
        st.error("Processed dataset not found. Please check the file path.")
        st.stop()

    df = pd.read_csv(file_path)
    df["date"] = pd.to_datetime(df["date"])

    return df


df = load_data()


# --------------------------------------------------
# Dashboard Title
# --------------------------------------------------
st.title("🌍 Climate Risk & Weather Trend Analytics Platform")
st.markdown(
    """
    **Myanmar & Singapore Climate Intelligence Dashboard**  
    Analyze temperature trends, rainfall patterns, seasonal behavior, and climate risk indicators.
    """
)


# --------------------------------------------------
# Quick Dataset Preview
# --------------------------------------------------
st.subheader("Dataset Preview")

st.write("Dataset shape:", df.shape)
st.dataframe(df.head())

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------
st.sidebar.header("🔎 Dashboard Filters")

city_options = sorted(df["city"].unique())
selected_city = st.sidebar.selectbox(
    "Select City",
    city_options
)

city_df = df[df["city"] == selected_city].copy()

min_date = city_df["date"].min()
max_date = city_df["date"].max()

selected_date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(selected_date_range) == 2:
    start_date, end_date = selected_date_range

    city_df = city_df[
        (city_df["date"] >= pd.to_datetime(start_date)) &
        (city_df["date"] <= pd.to_datetime(end_date))
    ]


# --------------------------------------------------
# KPI Cards
# --------------------------------------------------
st.subheader(f"📌 Climate Overview: {selected_city}")

avg_temp = city_df["temperature_avg"].mean()
total_rainfall = city_df["rainfall"].sum()
heat_risk_days = city_df["heat_risk_day"].sum()
avg_risk_score = city_df["daily_climate_risk_score"].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Average Temperature",
        value=f"{avg_temp:.1f} °C"
    )

with col2:
    st.metric(
        label="Total Rainfall",
        value=f"{total_rainfall:,.0f} mm"
    )

with col3:
    st.metric(
        label="Heat-Risk Days",
        value=f"{heat_risk_days:,.0f} days"
    )

with col4:
    st.metric(
        label="Average Risk Score",
        value=f"{avg_risk_score:.1f}/100"
    )
# --------------------------------------------------
# Temperature and Rainfall Trend Charts
# --------------------------------------------------
st.subheader("📈 Temperature & Rainfall Trends")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    temp_fig = px.line(
        city_df,
        x="date",
        y="temperature_avg",
        title=f"Average Temperature Trend - {selected_city}",
        labels={
            "date": "Date",
            "temperature_avg": "Average Temperature (°C)"
        }
    )

    temp_fig.update_layout(
        height=400,
        title_x=0.02
    )

    st.plotly_chart(temp_fig, use_container_width=True)


with chart_col2:
    rain_fig = px.line(
        city_df,
        x="date",
        y="rainfall",
        title=f"Daily Rainfall Trend - {selected_city}",
        labels={
            "date": "Date",
            "rainfall": "Rainfall (mm)"
        }
    )

    rain_fig.update_layout(
        height=400,
        title_x=0.02
    )

    st.plotly_chart(rain_fig, use_container_width=True)
# --------------------------------------------------
# Monthly Seasonal Patterns
# --------------------------------------------------
st.subheader("🌦️ Monthly Seasonal Patterns")

monthly_summary = (
    city_df.groupby(["month", "month_name"], as_index=False)
    .agg(
        avg_temperature=("temperature_avg", "mean"),
        avg_rainfall=("rainfall", "mean"),
        total_rainfall=("rainfall", "sum"),
        heat_risk_days=("heat_risk_day", "sum"),
        heavy_rain_days=("heavy_rain_day", "sum")
    )
    .sort_values("month")
)

season_col1, season_col2 = st.columns(2)

with season_col1:
    monthly_temp_fig = px.line(
        monthly_summary,
        x="month_name",
        y="avg_temperature",
        markers=True,
        title=f"Monthly Average Temperature - {selected_city}",
        labels={
            "month_name": "Month",
            "avg_temperature": "Average Temperature (°C)"
        }
    )

    monthly_temp_fig.update_layout(
        height=400,
        title_x=0.02
    )

    st.plotly_chart(monthly_temp_fig, use_container_width=True)


with season_col2:
    monthly_rain_fig = px.bar(
        monthly_summary,
        x="month_name",
        y="total_rainfall",
        title=f"Monthly Total Rainfall - {selected_city}",
        labels={
            "month_name": "Month",
            "total_rainfall": "Total Rainfall (mm)"
        }
    )

    monthly_rain_fig.update_layout(
        height=400,
        title_x=0.02
    )

    st.plotly_chart(monthly_rain_fig, use_container_width=True)
# --------------------------------------------------
# Climate Risk Detection
# --------------------------------------------------
st.subheader("🚨 Climate Risk Detection")

heat_risk_days = int(city_df["heat_risk_day"].sum())
very_hot_days = int(city_df["very_hot_day"].sum())
heavy_rain_days = int(city_df["heavy_rain_day"].sum())
dry_days = int(city_df["dry_day"].sum())

risk_col1, risk_col2, risk_col3, risk_col4 = st.columns(4)

with risk_col1:
    st.metric(
        label="🔥 Heat-Risk Days",
        value=f"{heat_risk_days} days"
    )

with risk_col2:
    st.metric(
        label="🌡️ Very Hot Days",
        value=f"{very_hot_days} days"
    )

with risk_col3:
    st.metric(
        label="🌧️ Heavy-Rain Days",
        value=f"{heavy_rain_days} days"
    )

with risk_col4:
    st.metric(
        label="☀️ Dry Days",
        value=f"{dry_days} days"
    )


# --------------------------------------------------
# Risk Level Distribution
# --------------------------------------------------
st.subheader("📊 Risk Level Distribution")

risk_level_summary = (
    city_df["risk_level"]
    .value_counts()
    .reset_index()
)

risk_level_summary.columns = ["risk_level", "number_of_days"]

risk_fig = px.bar(
    risk_level_summary,
    x="risk_level",
    y="number_of_days",
    title=f"Risk Level Distribution - {selected_city}",
    labels={
        "risk_level": "Risk Level",
        "number_of_days": "Number of Days"
    }
)

risk_fig.update_layout(
    height=400,
    title_x=0.02
)

st.plotly_chart(risk_fig, use_container_width=True)

# --------------------------------------------------
# City Comparison
# --------------------------------------------------
st.subheader("🌍 City Comparison")

city_comparison = (
    df.groupby("city", as_index=False)
    .agg(
        avg_temperature=("temperature_avg", "mean"),
        total_rainfall=("rainfall", "sum"),
        heat_risk_days=("heat_risk_day", "sum"),
        heavy_rain_days=("heavy_rain_day", "sum"),
        avg_risk_score=("daily_climate_risk_score", "mean")
    )
)

city_comparison["avg_temperature"] = city_comparison["avg_temperature"].round(2)
city_comparison["total_rainfall"] = city_comparison["total_rainfall"].round(0)
city_comparison["avg_risk_score"] = city_comparison["avg_risk_score"].round(2)

st.dataframe(city_comparison, use_container_width=True)


comparison_col1, comparison_col2 = st.columns(2)

with comparison_col1:
    risk_compare_fig = px.bar(
        city_comparison.sort_values("avg_risk_score", ascending=False),
        x="city",
        y="avg_risk_score",
        title="Average Climate Risk Score by City",
        labels={
            "city": "City",
            "avg_risk_score": "Average Risk Score"
        }
    )

    risk_compare_fig.update_layout(
        height=400,
        title_x=0.02
    )

    st.plotly_chart(risk_compare_fig, use_container_width=True)


with comparison_col2:
    heat_compare_fig = px.bar(
        city_comparison.sort_values("heat_risk_days", ascending=False),
        x="city",
        y="heat_risk_days",
        title="Heat-Risk Days by City",
        labels={
            "city": "City",
            "heat_risk_days": "Heat-Risk Days"
        }
    )

    heat_compare_fig.update_layout(
        height=400,
        title_x=0.02
    )

    st.plotly_chart(heat_compare_fig, use_container_width=True)
# --------------------------------------------------
# Seasonal Forecasting Section
# --------------------------------------------------
st.subheader("🔮 Seasonal Forecasting")

forecast_days = st.selectbox(
    "Select Forecast Period",
    options=[30, 90, 180, 365],
    index=3
)

forecast_start_date = city_df["date"].max() + pd.Timedelta(days=1)

future_dates = pd.date_range(
    start=forecast_start_date,
    periods=forecast_days
)

future_df = pd.DataFrame({
    "date": future_dates
})

future_df["month"] = future_df["date"].dt.month
future_df["day"] = future_df["date"].dt.day

historical_pattern = city_df.copy()
historical_pattern["month"] = historical_pattern["date"].dt.month
historical_pattern["day"] = historical_pattern["date"].dt.day

# --------------------------------------------------
# Temperature Forecast
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
    columns={"temperature_avg": "forecast_temperature_avg"}
)

future_temp_df["city"] = selected_city

# --------------------------------------------------
# Rainfall Forecast
# --------------------------------------------------
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
future_rain_df["city"] = selected_city

# --------------------------------------------------
# Forecast Charts
# --------------------------------------------------
recent_history = city_df[
    city_df["date"] >= city_df["date"].max() - pd.Timedelta(days=180)
]

forecast_col1, forecast_col2 = st.columns(2)

with forecast_col1:
    historical_temp = recent_history[["date", "temperature_avg"]].rename(
        columns={"temperature_avg": "temperature"}
    )
    historical_temp["type"] = "Historical"

    forecast_temp = future_temp_df[["date", "forecast_temperature_avg"]].rename(
        columns={"forecast_temperature_avg": "temperature"}
    )
    forecast_temp["type"] = "Forecast"

    temp_forecast_plot = pd.concat(
        [historical_temp, forecast_temp],
        ignore_index=True
    )

    temp_forecast_fig = px.line(
        temp_forecast_plot,
        x="date",
        y="temperature",
        color="type",
        title=f"Next {forecast_days} Days Seasonal Temperature Forecast - {selected_city}",
        labels={
            "date": "Date",
            "temperature": "Average Temperature (°C)",
            "type": "Data Type"
        }
    )

    temp_forecast_fig.update_layout(
        height=400,
        title_x=0.02
    )

    st.plotly_chart(temp_forecast_fig, use_container_width=True)


with forecast_col2:
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

    rain_forecast_fig = px.line(
        rain_forecast_plot,
        x="date",
        y="rainfall_value",
        color="type",
        title=f"Next {forecast_days} Days Seasonal Rainfall Forecast - {selected_city}",
        labels={
            "date": "Date",
            "rainfall_value": "Rainfall (mm)",
            "type": "Data Type"
        }
    )

    rain_forecast_fig.update_layout(
        height=400,
        title_x=0.02
    )

    st.plotly_chart(rain_forecast_fig, use_container_width=True)

st.info(
    """
    Seasonal baseline forecasting estimates future values using historical averages 
    for the same month and day from previous years. 
    
    This forecast captures seasonal climate patterns, but it should be interpreted 
    as a climate-pattern estimate rather than an exact daily weather prediction.
    """
)
# --------------------------------------------------
# Final Insights Summary
# --------------------------------------------------
st.subheader("🧠 Climate Insights Summary")

hottest_month = (
    monthly_summary
    .sort_values("avg_temperature", ascending=False)
    .iloc[0]["month_name"]
)

wettest_month = (
    monthly_summary
    .sort_values("total_rainfall", ascending=False)
    .iloc[0]["month_name"]
)

risk_level_main = (
    city_df["risk_level"]
    .mode()[0]
)

st.markdown(
    f"""
    ### Key Findings for {selected_city}

    - The average temperature for the selected period is **{avg_temp:.1f}°C**.
    - The total rainfall recorded is **{total_rainfall:,.0f} mm**.
    - The hottest month pattern is observed around **{hottest_month}**.
    - The wettest month pattern is observed around **{wettest_month}**.
    - The city recorded **{heat_risk_days} heat-risk days** and **{heavy_rain_days} heavy-rain days**.
    - The average climate risk score is **{avg_risk_score:.1f}/100**.
    - The most common daily risk level is **{risk_level_main}**.
    """
)

st.success(
    """
    Dashboard completed successfully. This platform helps monitor climate trends, 
    detect weather-related risk indicators, compare cities, and estimate future 
    seasonal climate patterns.
    """
)