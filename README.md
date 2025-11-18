# COVID-19 Data Analysis Repository

This repository combines multiple COVID-19 related projects and datasets into a single unified repository.

## Repository Structure

### Root Directory - Country-Specific Analysis Scripts
The root directory contains Python scripts for analyzing COVID-19 data from various countries:

- `mainPeru.py` - Peru COVID-19 data analysis
- `mainArgent.py` - Argentina COVID-19 data analysis
- `mainEcuador.py` - Ecuador COVID-19 data analysis
- `mainIndia.py` - India COVID-19 data analysis
- `mainJapan.py` - Japan COVID-19 data analysis
- `mainMexico.py` - Mexico COVID-19 data analysis
- `mainSlovakia.py` - Slovakia COVID-19 data analysis
- `mainSouthAfrica.py` / `mainSouthAfrica2.py` - South Africa COVID-19 data analysis
- `mainUSA.py` - USA COVID-19 data analysis
- `main Chilepy.py` - Chile COVID-19 data analysis
- `COVID_COLOMBIA.py` - Colombia COVID-19 data analysis
- `BoletinINS.py` - Instituto Nacional de Salud (INS) bulletin analysis
- `JhonHopkins.py` - Johns Hopkins University COVID-19 data
- `PerBraMex.py` - Peru, Brazil, Mexico comparative analysis
- `Peru2.py` - Additional Peru analysis
- `peruFullPython.py` - Comprehensive Peru COVID-19 analysis
- `fluBrazil.py` - Brazil flu data analysis
- `C19_WM_World_daily.py` - World daily COVID-19 data
- `us_counties.csv` / `us_states.csv` - US geographical data

### Subdirectories

#### `economist-excess-deaths/`
**Source:** [covid-19-the-economist-global-excess-deaths-model](https://github.com/JQ-dev/covid-19-the-economist-global-excess-deaths-model)

The Economist's global excess deaths model for COVID-19 analysis.

- `scripts/` - Analysis scripts
- `source-data/` - Raw data sources
- `output-data/` - Generated analysis outputs
- `global_mortality.png` - Global mortality visualization
- `README.md` - Project documentation
- `LICENCE` - License information

#### `sermo-barometer/`
**Source:** [sermo-covid](https://github.com/JQ-dev/sermo-covid)

Sermo COVID-19 Real-Time Barometer survey data from medical professionals.

- `sermo-covid-19-real-time-barometer-wave-1.csv` to `wave-7.csv` - Survey data across 7 waves
- `sermo_covid.py` - Analysis script for Sermo data
- `README.md` - Project documentation

#### `peru-ivermectin-study/`
**Source:** [Real-World-Evidence.-Peru-COVID-19-and-Ivermectin](https://github.com/JQ-dev/Real-World-Evidence.-Peru-COVID-19-and-Ivermectin)

Real-world evidence study on COVID-19 and Ivermectin usage in Peru.

- `Data/` - Study datasets
- `Figures and tables/` - Generated visualizations and tables
- `Sources/` - Source references and documentation
- `mainPeru.py` - Main analysis script
- `PeruTest&Hosptalizations.py` - Testing and hospitalization analysis
- `README.md` - Study documentation

## Merged Repositories

This repository consolidates the following GitHub repositories:

1. **COVID19** (main repository) - Multi-country COVID-19 analysis scripts
2. **covid-19-the-economist-global-excess-deaths-model** - Global excess deaths modeling
3. **sermo-covid** - Medical professional survey data
4. **Real-World-Evidence.-Peru-COVID-19-and-Ivermectin** - Peru Ivermectin study
5. **COVID_in_Africa** (empty repository)
6. **covid19-data** (empty repository)

## Usage

Each subdirectory contains its own README with specific usage instructions. Root-level scripts can be run independently for country-specific analyses.

## Data Sources

- Johns Hopkins University CSSE COVID-19 Data
- The Economist excess deaths model
- Sermo COVID-19 Real-Time Barometer
- Various national health ministries and institutions
- Peru Ministry of Health (MINSA)

## License

Please refer to individual subdirectories for specific licensing information.

## Last Updated

Repository merged and consolidated: November 18, 2025
