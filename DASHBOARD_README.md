# COVID-19 Comprehensive Dashboard

A comprehensive, interactive web dashboard that visualizes data from all merged COVID-19 research repositories.

## Features

### 📊 Overview Tab
- Key statistics across all datasets
- Summary of available data
- Dataset descriptions

### 🌍 Global Excess Deaths Tab
**Data Source:** The Economist's Global Excess Deaths Model

- **Interactive country selector** - Compare up to 5 countries simultaneously
- **Time series visualization** - Daily excess deaths with 95% confidence intervals
- **Income group analysis** - Excess deaths by World Bank income classifications
- **Top countries ranking** - Bar chart of countries most affected

**Key Metrics:**
- 15,120 data points
- 100+ countries covered
- Daily estimates with confidence intervals

### 💊 Peru Ivermectin Study Tab
**Data Source:** Real-World Evidence - Peru COVID-19 and Ivermectin

- **State distribution map** - Total doses distributed by Peru state
- **Time series** - Distribution trends over time
- **Product breakdown** - Pie chart showing different Ivermectin formulations
- **Summary statistics** - Total doses, states covered, date range

**Key Metrics:**
- 807 distribution records
- Multiple Peru states
- Various Ivermectin product types

### 🏥 Sermo Medical Survey Tab
**Data Source:** Sermo COVID-19 Real-Time Barometer (7 Waves)

- **Country distribution** - Top 15 countries by survey responses
- **Wave analysis** - Response counts across all 7 survey waves
- **US state breakdown** - Top 20 US states by physician responses
- **Survey overview** - Total responses and geographic coverage

**Key Metrics:**
- 37,285 total physician responses
- 7 survey waves
- Global coverage across multiple countries

### 🇺🇸 US States Tab
**Data Source:** US Census Data

- **Population ranking** - Top 20 states by population
- **Summary statistics** - Total population, extremes
- **Interactive hover** - State codes and detailed information

## Installation

### Requirements
- Python 3.8+
- pip package manager

### Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the dashboard:**
   ```bash
   python covid_dashboard_app.py
   ```

3. **Open your browser:**
   Navigate to `http://127.0.0.1:8050/`

## File Structure

```
COVID19/
├── covid_dashboard_app.py          # Main dashboard application
├── requirements.txt                # Python dependencies
├── DASHBOARD_README.md            # This file
├── economist-excess-deaths/       # Economist data
│   └── output-data/
│       ├── export_country.csv
│       └── wb_income_groups.csv
├── sermo-barometer/               # Sermo survey data
│   ├── sermo-covid-19-real-time-barometer-wave-1.csv
│   ├── ...
│   └── sermo-covid-19-real-time-barometer-wave-7.csv
├── peru-ivermectin-study/         # Peru IVM study
│   └── Data/
│       └── IVM Distribution.csv
└── us_states.csv                  # US states data
```

## Data Details

### The Economist Excess Deaths
- **Format:** CSV
- **Time Range:** 2020-2021
- **Granularity:** Daily estimates by country
- **Metrics:** Estimated excess deaths with multiple confidence intervals

### Sermo Barometer
- **Format:** CSV (7 files)
- **Survey Waves:** 7 waves conducted during pandemic
- **Respondents:** Medical professionals worldwide
- **Questions:** Treatment approaches, resource availability, concerns

### Peru Ivermectin Distribution
- **Format:** CSV
- **Data Type:** Distribution records by state and date
- **Metrics:** Doses distributed, product types, locations

### US States
- **Format:** CSV
- **Data:** State names, abbreviations, populations

## Technology Stack

- **Dash** - Web application framework
- **Plotly** - Interactive visualizations
- **Pandas** - Data manipulation
- **Python 3** - Core programming language

## Interactive Features

All visualizations support:
- **Hover information** - Detailed data on mouse hover
- **Zoom & Pan** - Interactive chart navigation
- **Export** - Download charts as PNG images
- **Dynamic updates** - Real-time filtering and selection

## Usage Tips

1. **Comparing Countries:** In the Excess Deaths tab, select multiple countries to compare their trajectories

2. **Exploring Trends:** Use the time series charts to identify patterns and peaks

3. **Cross-referencing:** Switch between tabs to correlate different data sources

4. **Exporting Data:** Hover over charts to access the camera icon for downloads

## Troubleshooting

### Port Already in Use
If port 8050 is already in use, modify the port in `covid_dashboard_app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8051)  # Change to 8051 or another port
```

### Missing Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Data Loading Errors
Ensure all data files are in their correct subdirectories relative to the app script.

## Future Enhancements

Potential additions:
- Map visualizations using geographic coordinates
- Statistical analysis tools
- Data export functionality
- More detailed filtering options
- Additional datasets integration

## License

Please refer to individual dataset licenses in their respective subdirectories.

## Contact

For issues or questions about the dashboard, please refer to the main repository README.

---

**Last Updated:** November 2025
**Version:** 1.0.0
