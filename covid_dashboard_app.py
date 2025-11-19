"""
COVID-19 Comprehensive Dashboard
Combines data from multiple COVID-19 research repositories
"""

import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "COVID-19 Comprehensive Dashboard"

# ============================================================================
# DATA LOADING
# ============================================================================

print("Loading data...")

# Load Economist Excess Deaths Data
try:
    economist_data = pd.read_csv('economist-excess-deaths/output-data/export_country.csv')
    economist_data['date'] = pd.to_datetime(economist_data['date'])
    print(f"✓ Loaded Economist data: {len(economist_data)} rows")
except Exception as e:
    print(f"✗ Error loading Economist data: {e}")
    economist_data = pd.DataFrame()

# Load Economist World Bank Income Groups Data
try:
    wb_income_data = pd.read_csv('economist-excess-deaths/output-data/wb_income_groups.csv')
    wb_income_data['date'] = pd.to_datetime(wb_income_data['date'])
    print(f"✓ Loaded World Bank income data: {len(wb_income_data)} rows")
except Exception as e:
    print(f"✗ Error loading World Bank income data: {e}")
    wb_income_data = pd.DataFrame()

# Load Sermo Barometer Data (all waves)
sermo_data_all = []
for wave in range(1, 8):
    try:
        df = pd.read_csv(f'sermo-barometer/sermo-covid-19-real-time-barometer-wave-{wave}.csv')
        df['wave'] = wave
        sermo_data_all.append(df)
        print(f"✓ Loaded Sermo wave {wave}: {len(df)} rows")
    except Exception as e:
        print(f"✗ Error loading Sermo wave {wave}: {e}")

sermo_data = pd.concat(sermo_data_all, ignore_index=True) if sermo_data_all else pd.DataFrame()

# Load Peru Ivermectin Distribution Data
try:
    peru_ivm_data = pd.read_csv('peru-ivermectin-study/Data/IVM Distribution.csv', encoding='latin-1')
    peru_ivm_data['FECHA'] = pd.to_datetime(peru_ivm_data['FECHA'], format='%d/%m/%Y', errors='coerce')
    print(f"✓ Loaded Peru IVM data: {len(peru_ivm_data)} rows")
except Exception as e:
    print(f"✗ Error loading Peru IVM data: {e}")
    peru_ivm_data = pd.DataFrame()

# Load US States Data
try:
    us_states = pd.read_csv('us_states.csv')
    print(f"✓ Loaded US states: {len(us_states)} rows")
except Exception as e:
    print(f"✗ Error loading US states: {e}")
    us_states = pd.DataFrame()

print("Data loading complete!\n")

# ============================================================================
# LAYOUT
# ============================================================================

app.layout = html.Div([
    html.Div([
        html.H1("COVID-19 Comprehensive Research Dashboard",
                style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '10px'}),
        html.P("Unified visualization of multiple COVID-19 research datasets",
               style={'textAlign': 'center', 'color': '#7f8c8d', 'marginBottom': '30px'}),
    ]),

    # Navigation tabs
    dcc.Tabs(id='tabs', value='overview', children=[
        dcc.Tab(label='📊 Overview', value='overview'),
        dcc.Tab(label='🌍 Global Excess Deaths', value='excess-deaths'),
        dcc.Tab(label='💊 Peru Ivermectin Study', value='peru-ivm'),
        dcc.Tab(label='🏥 Sermo Medical Survey', value='sermo'),
        dcc.Tab(label='🇺🇸 US States', value='us-states'),
    ], style={'marginBottom': '20px'}),

    # Content area
    html.Div(id='tab-content', style={'padding': '20px'})
])

# ============================================================================
# CALLBACKS
# ============================================================================

@app.callback(
    Output('tab-content', 'children'),
    Input('tabs', 'value')
)
def render_content(tab):
    if tab == 'overview':
        return render_overview()
    elif tab == 'excess-deaths':
        return render_excess_deaths()
    elif tab == 'peru-ivm':
        return render_peru_ivm()
    elif tab == 'sermo':
        return render_sermo()
    elif tab == 'us-states':
        return render_us_states()

# ============================================================================
# TAB RENDERERS
# ============================================================================

def render_overview():
    """Overview dashboard with key statistics"""

    # Calculate key metrics
    total_countries = economist_data['iso3c'].nunique() if not economist_data.empty else 0
    total_survey_responses = len(sermo_data) if not sermo_data.empty else 0
    peru_states = peru_ivm_data['State'].nunique() if not peru_ivm_data.empty else 0

    return html.Div([
        html.H2("📊 Dashboard Overview", style={'color': '#2c3e50'}),

        # Key Statistics Cards
        html.Div([
            html.Div([
                html.Div([
                    html.H3(total_countries, style={'color': '#3498db', 'fontSize': '48px', 'margin': '10px'}),
                    html.P("Countries in Excess Deaths Study", style={'color': '#7f8c8d'})
                ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#ecf0f1',
                         'borderRadius': '10px', 'margin': '10px'}),
            ], style={'flex': '1'}),

            html.Div([
                html.Div([
                    html.H3(total_survey_responses, style={'color': '#e74c3c', 'fontSize': '48px', 'margin': '10px'}),
                    html.P("Medical Professional Responses", style={'color': '#7f8c8d'})
                ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#ecf0f1',
                         'borderRadius': '10px', 'margin': '10px'}),
            ], style={'flex': '1'}),

            html.Div([
                html.Div([
                    html.H3(peru_states, style={'color': '#2ecc71', 'fontSize': '48px', 'margin': '10px'}),
                    html.P("Peru States in IVM Study", style={'color': '#7f8c8d'})
                ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#ecf0f1',
                         'borderRadius': '10px', 'margin': '10px'}),
            ], style={'flex': '1'}),
        ], style={'display': 'flex', 'marginBottom': '30px'}),

        # Dataset descriptions
        html.Div([
            html.H3("📚 Available Datasets", style={'color': '#2c3e50', 'marginTop': '30px'}),

            html.Div([
                html.H4("🌍 The Economist Global Excess Deaths Model"),
                html.P("Comprehensive analysis of excess mortality across countries during the COVID-19 pandemic. "
                       "Includes daily estimates with confidence intervals and comparisons by income groups."),
            ], style={'padding': '15px', 'backgroundColor': '#f8f9fa', 'borderLeft': '4px solid #3498db', 'marginBottom': '15px'}),

            html.Div([
                html.H4("💊 Peru Real-World Evidence: COVID-19 and Ivermectin"),
                html.P("Distribution data and analysis of Ivermectin usage across Peru during the COVID-19 pandemic. "
                       "Includes state-level distribution tracking and temporal analysis."),
            ], style={'padding': '15px', 'backgroundColor': '#f8f9fa', 'borderLeft': '4px solid #2ecc71', 'marginBottom': '15px'}),

            html.Div([
                html.H4("🏥 Sermo COVID-19 Real-Time Barometer"),
                html.P("Survey data from medical professionals worldwide across 7 waves. Captures physician opinions, "
                       "treatment approaches, concerns, and observations throughout the pandemic."),
            ], style={'padding': '15px', 'backgroundColor': '#f8f9fa', 'borderLeft': '4px solid #e74c3c', 'marginBottom': '15px'}),

            html.Div([
                html.H4("🇺🇸 US States and Counties Data"),
                html.P("Population and geographic data for US states and counties, useful for contextualizing "
                       "COVID-19 impact across different regions."),
            ], style={'padding': '15px', 'backgroundColor': '#f8f9fa', 'borderLeft': '4px solid #9b59b6', 'marginBottom': '15px'}),
        ]),

        html.Div([
            html.P("Use the tabs above to explore each dataset in detail with interactive visualizations.",
                   style={'textAlign': 'center', 'color': '#95a5a6', 'marginTop': '40px', 'fontStyle': 'italic'})
        ])
    ])

def render_excess_deaths():
    """Excess deaths visualization tab"""

    if economist_data.empty:
        return html.Div([
            html.H3("No data available", style={'color': '#e74c3c'})
        ])

    # Get list of countries for dropdown
    countries = sorted(economist_data['iso3c'].unique())

    return html.Div([
        html.H2("🌍 Global Excess Deaths Analysis", style={'color': '#2c3e50'}),
        html.P("Data from The Economist's global excess deaths model", style={'color': '#7f8c8d', 'marginBottom': '30px'}),

        # Country selector
        html.Div([
            html.Label("Select Countries (up to 5):", style={'fontWeight': 'bold', 'marginBottom': '10px'}),
            dcc.Dropdown(
                id='country-selector',
                options=[{'label': c, 'value': c} for c in countries],
                value=countries[:3] if len(countries) >= 3 else countries,
                multi=True,
                placeholder="Select countries..."
            ),
        ], style={'marginBottom': '30px'}),

        # Graphs
        dcc.Graph(id='excess-deaths-time-series'),

        html.Div([
            dcc.Graph(id='excess-deaths-by-income', style={'width': '50%', 'display': 'inline-block'}),
            dcc.Graph(id='top-countries-total', style={'width': '50%', 'display': 'inline-block'}),
        ]),
    ])

@app.callback(
    [Output('excess-deaths-time-series', 'figure'),
     Output('top-countries-total', 'figure')],
    Input('country-selector', 'value')
)
def update_excess_deaths(selected_countries):
    """Update excess deaths visualizations"""

    if not selected_countries:
        selected_countries = economist_data['iso3c'].unique()[:3]

    # Limit to 5 countries
    selected_countries = selected_countries[:5] if isinstance(selected_countries, list) else [selected_countries]

    # Time series plot
    df_filtered = economist_data[economist_data['iso3c'].isin(selected_countries)]

    fig1 = go.Figure()

    for country in selected_countries:
        df_country = df_filtered[df_filtered['iso3c'] == country]

        # Add confidence interval
        fig1.add_trace(go.Scatter(
            x=df_country['date'],
            y=df_country['estimated_daily_excess_deaths_ci_95_top'],
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))

        fig1.add_trace(go.Scatter(
            x=df_country['date'],
            y=df_country['estimated_daily_excess_deaths_ci_95_bot'],
            mode='lines',
            line=dict(width=0),
            fillcolor='rgba(0,100,200,0.2)',
            fill='tonexty',
            showlegend=False,
            hoverinfo='skip'
        ))

        # Add main line
        fig1.add_trace(go.Scatter(
            x=df_country['date'],
            y=df_country['estimated_daily_excess_deaths'],
            mode='lines',
            name=country,
            line=dict(width=2),
        ))

    fig1.update_layout(
        title="Daily Excess Deaths Over Time (with 95% confidence intervals)",
        xaxis_title="Date",
        yaxis_title="Estimated Daily Excess Deaths",
        hovermode='x unified',
        height=500,
        template='plotly_white'
    )

    # Top countries by total excess deaths
    total_by_country = economist_data.groupby('iso3c')['estimated_daily_excess_deaths'].sum().reset_index()
    total_by_country = total_by_country.sort_values('estimated_daily_excess_deaths', ascending=False).head(20)

    fig2 = px.bar(
        total_by_country,
        x='iso3c',
        y='estimated_daily_excess_deaths',
        title="Top 20 Countries by Total Excess Deaths",
        labels={'iso3c': 'Country', 'estimated_daily_excess_deaths': 'Total Excess Deaths'},
        color='estimated_daily_excess_deaths',
        color_continuous_scale='Reds'
    )

    fig2.update_layout(
        height=500,
        template='plotly_white',
        showlegend=False
    )

    return fig1, fig2

@app.callback(
    Output('excess-deaths-by-income', 'figure'),
    Input('tabs', 'value')
)
def update_income_groups(tab):
    """Update income group visualization"""

    if wb_income_data.empty:
        return go.Figure()

    # Aggregate by income group and date
    income_summary = wb_income_data.groupby(['date', 'income_group'])['estimated_daily_excess_deaths'].sum().reset_index()

    fig = px.line(
        income_summary,
        x='date',
        y='estimated_daily_excess_deaths',
        color='income_group',
        title="Excess Deaths by World Bank Income Groups",
        labels={'date': 'Date', 'estimated_daily_excess_deaths': 'Daily Excess Deaths', 'income_group': 'Income Group'},
    )

    fig.update_layout(
        height=500,
        template='plotly_white',
        hovermode='x unified'
    )

    return fig

def render_peru_ivm():
    """Peru Ivermectin study visualization"""

    if peru_ivm_data.empty:
        return html.Div([
            html.H3("No data available", style={'color': '#e74c3c'})
        ])

    # Calculate distribution by state
    dist_by_state = peru_ivm_data.groupby('State')['Doses'].sum().reset_index()
    dist_by_state = dist_by_state.sort_values('Doses', ascending=False)

    # Time series of distribution
    dist_by_date = peru_ivm_data.groupby('FECHA')['Doses'].sum().reset_index()
    dist_by_date = dist_by_date.sort_values('FECHA')

    # Bar chart by state
    fig1 = px.bar(
        dist_by_state,
        x='State',
        y='Doses',
        title="Ivermectin Distribution by Peru State (Total Doses)",
        labels={'State': 'State', 'Doses': 'Total Doses Distributed'},
        color='Doses',
        color_continuous_scale='Greens'
    )

    fig1.update_layout(
        height=500,
        template='plotly_white',
        xaxis_tickangle=-45
    )

    # Time series
    fig2 = px.line(
        dist_by_date,
        x='FECHA',
        y='Doses',
        title="Ivermectin Distribution Over Time",
        labels={'FECHA': 'Date', 'Doses': 'Daily Doses Distributed'},
        markers=True
    )

    fig2.update_layout(
        height=400,
        template='plotly_white'
    )

    # Product breakdown
    dist_by_product = peru_ivm_data.groupby('PRODUCTO')['Doses'].sum().reset_index()

    fig3 = px.pie(
        dist_by_product,
        values='Doses',
        names='PRODUCTO',
        title="Distribution by Product Type"
    )

    fig3.update_layout(height=400)

    return html.Div([
        html.H2("💊 Peru COVID-19 Ivermectin Study", style={'color': '#2c3e50'}),
        html.P("Real-world evidence of Ivermectin distribution across Peru",
               style={'color': '#7f8c8d', 'marginBottom': '30px'}),

        dcc.Graph(figure=fig1),

        html.Div([
            dcc.Graph(figure=fig2, style={'width': '60%', 'display': 'inline-block'}),
            dcc.Graph(figure=fig3, style={'width': '40%', 'display': 'inline-block'}),
        ]),

        html.Div([
            html.H4("📊 Summary Statistics", style={'marginTop': '30px'}),
            html.P(f"Total Doses Distributed: {peru_ivm_data['Doses'].sum():,.0f}"),
            html.P(f"States Covered: {peru_ivm_data['State'].nunique()}"),
            html.P(f"Distribution Period: {peru_ivm_data['FECHA'].min().strftime('%Y-%m-%d')} to {peru_ivm_data['FECHA'].max().strftime('%Y-%m-%d')}"),
        ], style={'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px'})
    ])

def render_sermo():
    """Sermo medical survey visualization"""

    if sermo_data.empty:
        return html.Div([
            html.H3("No data available", style={'color': '#e74c3c'})
        ])

    # Responses by country
    responses_by_country = sermo_data['country'].value_counts().reset_index()
    responses_by_country.columns = ['country', 'count']
    responses_by_country = responses_by_country.head(15)

    fig1 = px.bar(
        responses_by_country,
        x='country',
        y='count',
        title="Survey Responses by Country (Top 15)",
        labels={'country': 'Country', 'count': 'Number of Responses'},
        color='count',
        color_continuous_scale='Blues'
    )

    fig1.update_layout(
        height=400,
        template='plotly_white'
    )

    # Responses by wave
    responses_by_wave = sermo_data['wave'].value_counts().reset_index()
    responses_by_wave.columns = ['wave', 'count']
    responses_by_wave = responses_by_wave.sort_values('wave')

    fig2 = px.bar(
        responses_by_wave,
        x='wave',
        y='count',
        title="Survey Responses by Wave",
        labels={'wave': 'Wave Number', 'count': 'Number of Responses'},
        color='count',
        color_continuous_scale='Purples'
    )

    fig2.update_layout(
        height=400,
        template='plotly_white'
    )

    # Geographic distribution
    if 'state' in sermo_data.columns:
        us_responses = sermo_data[sermo_data['country'] == 'US']['state'].value_counts().reset_index()
        us_responses.columns = ['state', 'count']
        us_responses = us_responses.head(20)

        fig3 = px.bar(
            us_responses,
            x='state',
            y='count',
            title="US Responses by State (Top 20)",
            labels={'state': 'State', 'count': 'Number of Responses'}
        )

        fig3.update_layout(
            height=400,
            template='plotly_white',
            xaxis_tickangle=-45
        )
    else:
        fig3 = go.Figure()

    return html.Div([
        html.H2("🏥 Sermo COVID-19 Medical Professional Survey", style={'color': '#2c3e50'}),
        html.P("Real-time insights from physicians worldwide across 7 survey waves",
               style={'color': '#7f8c8d', 'marginBottom': '30px'}),

        html.Div([
            dcc.Graph(figure=fig1, style={'width': '50%', 'display': 'inline-block'}),
            dcc.Graph(figure=fig2, style={'width': '50%', 'display': 'inline-block'}),
        ]),

        dcc.Graph(figure=fig3),

        html.Div([
            html.H4("📊 Survey Overview", style={'marginTop': '30px'}),
            html.P(f"Total Responses: {len(sermo_data):,}"),
            html.P(f"Countries Represented: {sermo_data['country'].nunique()}"),
            html.P(f"Survey Waves: 7"),
            html.P("The Sermo COVID-19 Real-Time Barometer captured physician perspectives on "
                   "COVID-19 treatment approaches, concerns, resource availability, and patient care strategies "
                   "throughout the pandemic."),
        ], style={'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px'})
    ])

def render_us_states():
    """US States visualization"""

    if us_states.empty:
        return html.Div([
            html.H3("No data available", style={'color': '#e74c3c'})
        ])

    # Sort by population
    us_states_sorted = us_states.sort_values('Population', ascending=False).head(20)

    fig = px.bar(
        us_states_sorted,
        x='State',
        y='Population',
        title="Top 20 US States by Population",
        labels={'State': 'State', 'Population': 'Population'},
        color='Population',
        color_continuous_scale='Viridis',
        hover_data=['St']
    )

    fig.update_layout(
        height=500,
        template='plotly_white',
        xaxis_tickangle=-45
    )

    return html.Div([
        html.H2("🇺🇸 US States Data", style={'color': '#2c3e50'}),
        html.P("Population distribution across US states and territories",
               style={'color': '#7f8c8d', 'marginBottom': '30px'}),

        dcc.Graph(figure=fig),

        html.Div([
            html.H4("📊 Summary", style={'marginTop': '30px'}),
            html.P(f"Total States/Territories: {len(us_states)}"),
            html.P(f"Total Population: {us_states['Population'].sum():,}"),
            html.P(f"Most Populous: {us_states.loc[us_states['Population'].idxmax(), 'State']} "
                   f"({us_states['Population'].max():,})"),
            html.P(f"Least Populous: {us_states.loc[us_states['Population'].idxmin(), 'State']} "
                   f"({us_states['Population'].min():,})"),
        ], style={'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px'})
    ])

# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("COVID-19 Comprehensive Dashboard")
    print("="*60)
    print("\nStarting server...")
    print("Open your browser and navigate to: http://127.0.0.1:8050/")
    print("\nPress Ctrl+C to stop the server\n")

    app.run(debug=True, host='0.0.0.0', port=8050)
