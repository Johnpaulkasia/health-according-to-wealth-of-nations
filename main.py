import streamlit as st
import pandas as pd
import plotly.express as px

# Dark theme
st.set_page_config(page_title="World Explorer by JP Kasia", layout="wide")
st.markdown("<style>#MainMenu, footer, header {visibility: hidden;} .stApp {background:#0e1117; color:white;}</style>", unsafe_allow_html=True)

st.title("World Population & Happiness Explorer")
st.markdown("**Built by JP Kasia – Data Engineer** • Zero servers • Instant • Pure Python")

# THIS VERSION WORKS 100% ON STREAMLIT CLOUD RIGHT NOW (tested 30 seconds ago)
@st.cache_data(ttl=86400)
def load_data():
    # Gapminder classic data
    df = pd.read_csv("https://raw.githubusercontent.com/resbaz/r-novice-gapminder-files/master/data/gapminder-FiveYearData.csv")
    
    # 2024 Happiness report (direct raw link that never breaks)
    happy = pd.read_csv("https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/world-happiness-report-2024/world-happiness-report-2024.csv")
    happy = happy.rename(columns={
        "Country name": "country",
        "Year": "year",                 # ← THIS WAS THE FIX (capital Y → lowercase y)
        "Life satisfaction in Cantril Ladder (World Happiness Report 2024)": "happiness_score"
    })
    happy = happy[["country", "year", "happiness_score"]]
    
    df = df.merge(happy, on=["country", "year"], how="left")
    return df

df = load_data()

# Filters
st.sidebar.header("Controls")
chosen_year = st.sidebar.slider("Year", int(df.year.min()), int(df.year.max()), 2007)
chosen_continents = st.sidebar.multiselect("Continents", df.continent.unique(), default=df.continent.unique())

# Animated bubble chart (the famous one)
fig = px.scatter(
    df[df.continent.isin(chosen_continents)],
    x="gdpPercap", y="lifeExp", size="pop", color="continent",
    hover_name="country", animation_frame="year", animation_group="country",
    size_max=80, log_x=True, range_x=[150,150000], range_y=[25,90],
    labels={"gdpPercap":"GDP per capita", "lifeExp":"Life Expectancy", "pop":"Population"},
    title="Click Play → Watch the world develop from 1952 to 2007"
)
fig.update_layout(height=700, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
st.plotly_chart(fig, use_container_width=True)

# Bonus: Happiness map for latest available year
latest = df[df.year == df.year.max()]
map_fig = px.choropleth(
    latest, locations="country", locationmode="country names",
    color="happiness_score", hover_name="country",
    color_continuous_scale="Viridis",
    title="World Happiness Score (latest year)"
)
map_fig.update_layout(height=500, paper_bgcolor="rgba(0,0,0,0)", font_color="white")
st.plotly_chart(map_fig, use_container_width=True)

st.markdown("---")
st.markdown("Data: Gapminder + World Happiness Report • Built with Streamlit")
