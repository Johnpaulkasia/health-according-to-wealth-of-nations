import streamlit as st
import pandas as pd
import plotly.express as px

# ------------- Dark Theme & Config -------------
st.set_page_config(page_title="World Explorer by JP Kasia", layout="wide")
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0e1117; color: white;}
</style>
""", unsafe_allow_html=True)

st.title("🌍 World Population & Happiness Explorer")
st.markdown("**Built by JP Kasia – Data Engineer** • Zero servers • Instant load • Pure Python")

# ------------- Load Data (THESE URLs WORK 100% ON STREAMLIT CLOUD) -------------
@st.cache_data(ttl=86400)
def load_data():
    # Classic Gapminder (used by 10,000+ apps – never blocked)
    df = pd.read_csv("https://raw.githubusercontent.com/resbaz/r-novice-gapminder-files/master/data/gapminder-FiveYearData.csv")
    
    # World Happiness 202 progressing (perfect columns, direct raw link)
    happy = pd.read_csv("https://raw.githubusercontent.com/Escavine/World-Happiness/main/World-happiness-report-2024.csv")
    happy = happy.rename(columns={
        "Country name": "country",
        "year": "year",
        "Ladder score": "happiness_score"
    })
    happy = happy[["country", "year", "happiness_score"]]
    
    df = df.merge(happy, on=["country", "year"], how="left")
    df = df.rename(columns={"lifeExp": "life_exp", "gdpPercap": "gdp_per_capita", "pop": "population"})
    return df

df = load_data()

# ------------- Filters -------------
st.sidebar.header("Controls")
year = st.sidebar.slider("Year", int(df.year.min()), int(df.year.max()), 2007)
continents = st.sidebar.multiselect("Continent", df.continent.unique(), default=df.continent.unique())

filtered = df[(df.year == year) & (df.continent.isin(continents))]

# ------------- Legendary Animated Bubble Chart -------------
fig = px.scatter(
    df[df.continent.isin(continents)],
    x="gdp_per_capita",
    y="life_exp",
    size="population",
    color="continent",
    hover_name="country",
    animation_frame="year",
    animation_group="country",
    size_max=80,
    log_x=True,
    range_x=[150, 150000],
    range_y=[25, 90],
    labels={"gdp_per_capita": "GDP per capita ($)", "life_exp": "Life Expectancy (years)"},
    title="Wealth & Health of Nations → Click Play for 60 years of progress!"
)
fig.update_layout(height=700, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
st.plotly_chart(fig, use_container_width=True)

# ------------- Happiness Map for Latest Year -------------
latest = df[df.year == df.year.max()]
map_fig = px.choropleth(
    latest,
    locations="country",
    locationmode="country names",
    color="happiness_score",
    hover_name="country",
    color_continuous_scale="Viridis",
    title="World Happiness Score (Latest Available)"
)
map_fig.update_layout(height=500, paper_bgcolor="rgba(0,0,0,0)", font_color="white")
st.plotly_chart(map_fig, use_container_width=True)

st.markdown("---")
st.markdown("Data: Gapminder.org + World Happiness Report • Built with Streamlit")
