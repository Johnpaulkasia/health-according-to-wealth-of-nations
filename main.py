import streamlit as st
import pandas as pd
import plotly.express as px

# ------------- Page Config & Dark Theme -------------
st.set_page_config(page_title="World Explorer by JP Kasia", layout="wide")

st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0e1117; color: white;}
</style>
""", unsafe_allow_html=True)

st.title("🌍 World Population & Happiness Explorer")
st.markdown("**Built by JP Kasia – Data Engineer** • Zero servers • Sub-second queries • Pure Python")

# ------------- Load Data (bulletproof links) -------------
@st.cache_data(ttl=86400)  # Cache 24 hours
def load_data():
    # Classic Gapminder data (1952–2007, perfect for animation)
    gap_url = "https://raw.githubusercontent.com/OHI-Science/data-science-training/master/data/gapminder.csv"
    df = pd.read_csv(gap_url)
    
    # Add latest World Happiness 2024 scores
    happy_url = "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/world-happiness-report-2024/world-happiness-report-2024.csv"
    happy = pd.read_csv(happy_url)
    happy = happy.rename(columns={"Country name": "country", "year": "year", "Life satisfaction in Cantril Ladder (World Happiness Report 2024)": "happiness_score"})
    happy = happy[["country", "year", "happiness_score"]]
    
    # Merge (left join so old years keep working)
    df = df.merge(happy, on=["country", "year"], how="left")
    return df

df = load_data()

# ------------- Sidebar Filters -------------
st.sidebar.header("🎮 Controls")
year = st.sidebar.slider("Year", int(df.year.min()), int(df.year.max()), 2007)
continent = st.sidebar.multiselect("Continent", options=sorted(df.continent.unique()), default=df.continent.unique())
min_pop = st.sidebar.slider("Minimum Population", 0, int(df["pop"].max()), 0)

filtered = df[(df.year == year) & (df.continent.isin(continent)) & (df["pop"] >= min_pop)]

# ------------- Animated Bubble Chart (the famous one) -------------
fig = px.scatter(
    df.query("continent in @continent and pop >= @min_pop"),
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="continent",
    hover_name="country",
    animation_frame="year",
    animation_group="country",
    size_max=80,
    log_x=True,
    range_x=[100, 100000],
    range_y=[20, 90],
    labels={"gdpPercap": "GDP per capita ($)", "lifeExp": "Life Expectancy", "pop": "Population"},
    title="Wealth & Health of Nations (1952–2007) → Click Play!"
)

fig.update_layout(height=700, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
st.plotly_chart(fig, use_container_width=True)

# ------------- Latest Year Happiness Map -------------
latest_year = df.year.max()
latest = df[df.year == latest_year]
map_fig = px.choropleth(
    latest,
    locations="iso_alpha",
    color="happiness_score",
    hover_name="country",
    color_continuous_scale="Viridis",
    title=f"World Happiness Score in {latest_year}"
)
map_fig.update_layout(height=500, paper_bgcolor="rgba(0,0,0,0)", font_color="white")
st.plotly_chart(map_fig, use_container_width=True)

st.markdown("---")
st.markdown("Built with ❤️ using Streamlit + Plotly | Source: Gapminder & World Happiness Report")
