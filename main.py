import pandas as pd
import plotly.express as px
import streamlit as st

# -------------------------- Config & Style --------------------------
st.set_page_config(page_title="World Explorer by JP Kasia", layout="wide")

hide_style = """
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0e1117; color: white;}
</style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

st.title("🌍 World Population & Happiness Explorer")
st.markdown("**Built by JP Kasia – Data Engineer** • Pure Python • Zero servers • Lightning fast")

# -------------------------- Load Data (100% working URLs) --------------------------
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data():
    # Gapminder data (official, stable)
    url1 = "https://storage.googleapis.com/public-data-uploads/gapminder.csv"
    df = pd.read_csv(url1)
    
    # World Happiness Report 2024 (direct, stable)
    url2 = "https://raw.githubusercontent.com/ajaytcdav/world-happiness-report/main/world-happiness-report-2024.csv"
    happy = pd.read_csv(url2)
    happy = happy[["Country name", "year", "Ladder score"]].rename(columns={
        "Country name": "country",
        "Ladder score": "happiness_score"
    })
    
    # Merge
    df = df.merge(happy, on=["country", "year"], how="left")
    return df

df = load_data()

# -------------------------- Filters --------------------------
st.sidebar.header("Filters")
year_range = st.sidebar.slider("Year", 1800, 2023, (1950, 2023))
continent = st.sidebar.multiselect("Continent", sorted(df.continent.unique()))
min_pop = st.sidebar.slider("Min Population", 0, 200_000_000, 500_000, step=500_000)

filtered = df[(df.year >= year_range[0]) & (df.year <= year_range[1]) & (df.population >= min_pop)]
if continent:
    filtered = filtered[filtered.continent.isin(continent)]

# -------------------------- Animated Bubble Chart --------------------------
fig = px.scatter(
    filtered,
    x="gdp_per_capita_ppp",
    y="happiness_score",
    size="population",
    color="continent",
    hover_name="country",
    animation_frame="year",
    size_max=80,
    log_x=True,
    range_x=[300, 150000],
    range_y=[2, 10],
    labels={"gdp_per_capita_ppp": "GDP per capita ($)", "happiness_score": "Happiness Score"},
    title="Watch countries get richer & happier → Click Play!"
)

fig.update_layout(
    height=700,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    legend_title_text=""
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------- World Map Bonus --------------------------
latest = filtered[filtered.year == filtered.year.max()]
map_fig = px.choropleth(
    latest,
    locations="iso_alpha",
    color="happiness_score",
    hover_name="country",
    color_continuous_scale="Viridis",
    title=f"World Happiness in {latest.year.iloc[0]}"
)
map_fig.update_layout(height=500, paper_bgcolor="rgba(0,0,0,0)", font_color="white")
st.plotly_chart(map_fig, use_container_width=True)

st.markdown("---")
st.markdown("Built with ❤️ using Streamlit • Source code on GitHub")
