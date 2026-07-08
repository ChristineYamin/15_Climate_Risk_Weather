# Project 15 - Climate Risk and Weather Trend Analytics Platform
An interactive climate analytics dashboard that analyzes historical weather trends, detects climate-risk indicators, compares city-level climate risk, and estimates future seasonal temperature and rainfall patterns.

This project uses historical daily climate data to help users understand temperature behavior, rainfall patterns, heat-risk days, heavy-rain events, and future seasonal climate trends through a clean Streamlit dashboard.

## Project Overview
Climate change and extreme weather events are becoming increasingly important for cities, communities, and decision-makers. Understanding long-term weather patterns can help identify risk signals such as extreme heat, heavy rainfall, dry days, and seasonal climate changes.

This project was built as a data science analytics platform to answer questions such as:

- How does temperature change over time across different cities?
- Which months receive the highest rainfall?
- Which cities show higher climate-risk patterns?
- How many heat-risk or heavy-rain days occur in each city?
- What could future seasonal temperature and rainfall patterns look like?

## Objectives
- Collect data from Nasa power
- Clean the data, preprocess , feature engineering and get the cleaned csv for the further steps
- Analyze temperature, rainfall, climate risk patterns
- Compare climate risk across cities
- Build a seasonal Baseline forecasting system
- Deploy an interactive dashboard using Streamlit

## Key Features
### Historical Climate Trend Analysis
- Daily average temperature trend
- Monthly rainfall pattern
- Seasonal weather behavior
- City-level climate comparison

### 🚨 Climate Risk Detection

The dashboard identifies important climate-risk indicators, including:

- Heat-risk days
- Very hot days
- Heavy-rain days
- Dry days
- Daily climate risk score
- Risk level classification: Low, Moderate, High

### 🔮 Seasonal Forecasting

The project includes a seasonal baseline forecasting method for:

- Future temperature patterns
- Future rainfall patterns

The forecasting method estimates future values using historical averages for the same month and day from previous years. This helps capture natural seasonal climate behavior.

### 🌍 City Comparison

The dashboard compares selected cities based on:

- Average climate risk score
- Heat-risk days
- Rainfall behavior
- Overall climate-risk ranking

## 🏙️ Cities Included

The analysis currently includes:

- Yangon
- Mandalay
- Naypyidaw
- Singapore

## Dataset
The project uses historical daily weather and climate data collected from the NASA POWER API.
Main weather variables include: Average temperature, Maximum temperature, Minimum temperature, Rainfall, Humidity, Wind speed
, City, Country, Latitude, Longitude, Date

## Data Preprocessing
The raw climate data was cleaned and transformed before analysis.

Main preprocessing steps:

Converted date column into datetime format
Sorted records by city and date
Extracted year, month, month name, day, and day of year
Created seasonal categories
Created climate-risk indicator columns
Created rainfall and temperature categories
Built a daily climate risk score
Classified each day into Low, Moderate, or High risk level

## Feature Engineering
- Heat risk day [temperature_max >= 35°C]
- Very Hot day [temperature_max >= 38°C]
- Heavy rain day [rainfall >= 50 mm]
- Dry day [rainfall < 1 mm]
- Daily Climate Risk Score 
- Risk Level

## Forecasting Method
This project uses a seasonal baseline forecasting approach.

For each future date, the model looks at historical records from the same month and day, then calculates the average value.
This method was selected because climate data often follows seasonal patterns. It creates a more natural climate-pattern forecast compared with a simple straight-line forecast.
Forecasted variables : Average temperature, Rainfall

## Dashboard Sections
The Streamlit dashboard includes:

KPI summary cards
Seasonal temperature and rainfall forecasting
Key insights summary
Historical temperature trend analysis
Monthly rainfall pattern
Climate risk level distribution
City climate risk ranking
Detailed data and extra analysis section

## Technologies Used
- Python
- Pandas
- Plotly
- Streamlit
- NASA PoWER API
- Jupyter Notebook

## Key Insights

Some of the insights generated from this project include:

Cities show different temperature and rainfall patterns across seasons.
Rainfall is highly seasonal, with clear wet and dry periods.
Heat-risk days are useful indicators for identifying climate stress.
City-level comparison helps reveal which locations show higher average climate risk.
Seasonal baseline forecasting provides an interpretable way to estimate future climate patterns.

## Project Outcome
This project demonstrates a complete data science workflow:

Data collection
Data cleaning
Feature engineering
Exploratory data analysis
Climate-risk scoring
Seasonal forecasting
Dashboard development
Streamlit deployment

The final dashboard helps transform raw climate data into clear, interactive, and decision-friendly insights.

## Future Improvements
Possible future improvements include:

- Add more cities and countries
- Add map-based climate visualization
- Add anomaly detection for extreme weather events
- Add machine learning forecasting models
- Add downloadable forecast reports
- Add comparison between historical and future climate-risk levels
- Add user-selected forecast variables

## Live Demo
https://15-climate-risk-weather-trends.streamlit.app/


## Author
Shwe Yamin