import pandas as pd
import plotly.express as px
import streamlit as st

# -------------------------- Page Config & Dark Mode --------------------------
st.set_page_config(page_title="World Explorer by JP Kasia", layout="wide")

hide_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {background-color: #0e1117;}
</style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# -------------------------- Title --------------------------
st.title("🌍 World Population & Happiness Explorer")
st.markdown("**Built by JP Kasia – Data Engineer** | Zero servers | Sub-second queries | Pure Python magic")

# -------------------------- Load Data (one-liner now) --------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/gapminder-%28owid%29/gapminder-%28owid%29.csv"
    df = pd.read_csv(url)
    # Add World Happiness Score (2024 latest)
    happiness_url = "https://raw.githubusercontent.com/ajaytcdav/world-happiness-report/main/world-happiness-report-2024.csv"
    happy = pd.read_csv(happiness_url)[["Country name", "year", "Ladder score"]]
    happy.rename(columns={"Country name": "country", "Ladder score": "happiness_score"}, inplace=True)
    df = df.merge(happy, on=["country", "year"], how="left")
    return df

df = load_data()

# -------------------------- Filters (sidebar for clean look) --------------------------
st.sidebar.header("🎛 Filters")
continents = st.sidebar.multiselect("Continent", options=sorted(df.continent.unique()), default=[])
countries = st.sidebar.multiselect("Country", options=sorted(df.country.unique()))
year_range = st.sidebar.slider("Year Range", 1800, 2023, (1950, 2023), step=5)
min_pop = st.sidebar.slider("Min Population", 0, 200_000_000, 1_000_000)

# Apply filters
filtered = df.copy()
filtered = filtered[(filtered.year >= year_range[0]) & (filtered.year <= year_range[1])]
filtered = filtered[filtered.population >= min_pop]
if continents:
    filtered = filtered[filtered.continent.isin(continents)]
if countries:
    filtered = filtered[filtered.country.isin(countries)]

# -------------------------- Main Chart (Happiness + Life Expectancy) --------------------------
fig = px.scatter(
    filtered,
    x="gdpPercap",
    y="happiness_score",           # ← Now using happiness score!
    size="population",
    color="continent",
    hover_name="country",
    animation_frame="year",
    animation_group="country",
    size_max=100,
    log_x=True,
    range_x=[200, 150000],
    range_y=[3, 10.5],
    labels={
        "gdpPercap": "GDP per capita (PPP $)",
        "happiness_score": "Happiness Score (0-10)",
        "population": "Population",
        "continent": "Continent"
    },
    title="Watch the world get richer & happier over 200+ years → Click Play!"
)

fig.update_layout(
    height=700,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#ffffff",
    title_font_size=24,
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#444")
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------- Bonus: Static Map (extra wow) --------------------------
st.markdown("### 🗺 Static World Map View (Latest Year)")
latest = filtered[filtered.year == filtered.year.max()]
map_fig = px.choropleth(
    latest,
    locations="iso_alpha",
    color="happiness_score",
    hover_name="country",
    color_continuous_scale="Viridis",
    title=f"Happiness Around the World in {latest.year.iloc[0]}"
)
map_fig.update_layout(height=500, paper_bgcolor="rgba(0,0,0,0)", font_color="#ffffff")
st.plotly_chart(map_fig, use_container_width=True)

# -------------------------- Footer --------------------------
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit + Plotly + public OWID data")
