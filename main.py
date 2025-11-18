import streamlit as st
import plotly.express as px

# ------------- Dark Theme & Beautiful Style -------------
st.set_page_config(page_title="World Explorer by JP Kasia", layout="wide")
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0e1117; color: white;}
</style>
""", unsafe_allow_html=True)

st.title("🌍 World Population & Happiness Explorer")
st.markdown("**Built by JP Kasia – Data Engineer** • Zero servers • Built-in data • Lightning fast • Pure Python")

# ------------- Load the legendary Gapminder data (no internet needed!) -------------
df = px.data.gapminder()

# ------------- Sidebar Controls -------------
st.sidebar.header("🎮 Controls")
continents = st.sidebar.multiselect("Continents", df.continent.unique(), default=df.continent.unique())
years = st.sidebar.slider("Year Range", int(df.year.min()), int(df.year.max()), (1952, 2007))

filtered_df = df[df.continent.isin(continents)]
filtered_df = filtered_df[(filtered_df.year >= years[0]) & (filtered_df.year <= years[1])]

# ------------- The Famous Animated Bubble Chart -------------
fig = px.scatter(
    filtered_df,
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
    range_y=[25, 90],
    labels={"gdpPercap": "GDP per capita ($)", "lifeExp": "Life Expectancy", "pop": "Population"},
    title="Click Play → Watch 50+ years of human progress!"
)

fig.update_layout(
    height=700,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    title_font_size=24
)

st.plotly_chart(fig, use_container_width=True)

# ------------- Bonus Choropleth Map for Latest Year -------------
latest_year = filtered_df.year.max()
latest = filtered_df[filtered_df.year == latest_year]

map_fig = px.choropleth(
    latest,
    locations="iso_alpha",
    color="lifeExp",
    hover_name="country",
    color_continuous_scale="Viridis",
    title=f"Life Expectancy Around the World in {latest_year}"
)
map_fig.update_layout(height=500, paper_bgcolor="rgba(0,0,0,0)", font_color="white")
st.plotly_chart(map_fig, use_container_width=True)

st.markdown("---")
st.markdown("Data built into Plotly (Gapminder.org) • Zero external dependencies • Deployed in seconds")
