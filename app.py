import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from nasa_api import fetch_exoplanets
from ai_summary import get_ai_summary

st.set_page_config(
    page_title="🪐 Exoplanet Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# Custom CSS
# -------------------------------------------------

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0a0a1a 0%, #0d1b2a 100%); }
    h1, h2, h3 { color: #e0e0ff; }
    .stMetric { background: rgba(255,255,255,0.03); border-radius: 10px; padding: 0.5rem; }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Header
# -------------------------------------------------

st.title("🪐 Exoplanet Explorer Dashboard")
st.caption("Real NASA exoplanet data • AI-powered summaries • Interactive visualizations")
st.markdown("---")

# -------------------------------------------------
# Load Data
# -------------------------------------------------

@st.cache_data(ttl=3600)
def load_data():
    return fetch_exoplanets()

with st.spinner("🔭 Fetching exoplanet data from NASA..."):
    df = load_data()

if df is None or df.empty:
    st.error("Failed to load exoplanet data. Please check your connection.")
    st.stop()

# -------------------------------------------------
# Sidebar Filters
# -------------------------------------------------

st.sidebar.title("🔧 Filters")

methods = ["All"] + sorted(df["discoverymethod"].dropna().unique().tolist())
selected_method = st.sidebar.selectbox("Discovery Method", methods)

min_year = int(df["disc_year"].min())
max_year = int(df["disc_year"].max())
year_range = st.sidebar.slider("Discovery Year", min_year, max_year, (2000, max_year))

habitable_only = st.sidebar.checkbox("🌱 Habitable Zone Only", value=False)

max_radius = float(df["pl_rade"].dropna().max())
radius_range = st.sidebar.slider(
    "Planet Radius (Earth radii)",
    0.0, min(max_radius, 30.0), (0.0, 10.0)
)

st.sidebar.markdown("---")
st.sidebar.caption("Data source: NASA Exoplanet Archive")

# -------------------------------------------------
# Apply Filters
# -------------------------------------------------

filtered = df.copy()

if selected_method != "All":
    filtered = filtered[filtered["discoverymethod"] == selected_method]

filtered = filtered[
    (filtered["disc_year"] >= year_range[0]) &
    (filtered["disc_year"] <= year_range[1])
]

filtered = filtered[
    (filtered["pl_rade"] >= radius_range[0]) &
    (filtered["pl_rade"] <= radius_range[1])
]

if habitable_only:
    filtered = filtered[
        (filtered["pl_orbsmax"] >= 0.5) &
        (filtered["pl_orbsmax"] <= 2.0) &
        (filtered["st_teff"] >= 3700) &
        (filtered["st_teff"] <= 7200)
    ]

# -------------------------------------------------
# KPI Metrics
# -------------------------------------------------

col1, col2, col3, col4 = st.columns(4)
col1.metric("🪐 Total Exoplanets", f"{len(filtered):,}")
col2.metric("🔭 Discovery Methods", filtered["discoverymethod"].nunique())
col3.metric("⭐ Host Stars", filtered["hostname"].nunique())
col4.metric("📅 Year Range", f"{year_range[0]}–{year_range[1]}")

st.markdown("---")

# -------------------------------------------------
# Chart 1: Timeline of Discoveries
# -------------------------------------------------

st.subheader("📅 Timeline of Exoplanet Discoveries")

timeline = (
    filtered.groupby(["disc_year", "discoverymethod"])
    .size()
    .reset_index(name="count")
)

fig_timeline = px.bar(
    timeline,
    x="disc_year",
    y="count",
    color="discoverymethod",
    labels={"disc_year": "Year", "count": "Planets Discovered", "discoverymethod": "Method"},
    color_discrete_sequence=px.colors.qualitative.Vivid,
    template="plotly_dark"
)
fig_timeline.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    legend_title="Discovery Method",
    bargap=0.1
)
st.plotly_chart(fig_timeline, use_container_width=True)

st.markdown("---")

# -------------------------------------------------
# Chart 2: Planet Size vs Distance
# -------------------------------------------------

st.subheader("🔵 Planet Size vs. Distance from Star")

scatter_df = filtered.dropna(subset=["pl_orbsmax", "pl_rade"])
scatter_df = scatter_df[scatter_df["pl_orbsmax"] < 10]
scatter_df = scatter_df[scatter_df["pl_rade"] < 25]
scatter_df = scatter_df.copy()
if "pl_masse" in scatter_df.columns:
    scatter_df["pl_masse"] = scatter_df["pl_masse"].fillna(scatter_df["pl_masse"].median())
    use_size = "pl_masse"
else:
    use_size = None

fig_scatter = px.scatter(
    scatter_df,
    x="pl_orbsmax",
    y="pl_rade",
    size=use_size,
    color="discoverymethod",
    hover_name="pl_name",
    hover_data={"pl_orbsmax": ":.2f", "pl_rade": ":.2f"},
    labels={
        "pl_orbsmax": "Orbital Distance (AU)",
        "pl_rade": "Planet Radius (Earth radii)",
        "discoverymethod": "Method"
    },
    size_max=25,
    template="plotly_dark",
    color_discrete_sequence=px.colors.qualitative.Vivid
)

fig_scatter.add_vrect(
    x0=0.95, x1=1.37,
    fillcolor="green", opacity=0.08,
    line_width=1, line_color="green",
    annotation_text="🌱 Habitable Zone",
    annotation_position="top left",
    annotation_font_color="lightgreen"
)

fig_scatter.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
)
st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

# -------------------------------------------------
# Chart 3: Habitable Zone Map
# -------------------------------------------------

st.subheader("🌱 Habitable Zone Analysis")

hab_df = filtered.dropna(subset=["pl_orbsmax", "st_teff", "pl_rade"])
hab_df = hab_df[hab_df["st_teff"].between(2000, 12000)]
hab_df = hab_df[hab_df["pl_orbsmax"] < 10]

in_hz = hab_df[
    (hab_df["pl_orbsmax"] >= 0.5) &
    (hab_df["pl_orbsmax"] <= 2.0) &
    (hab_df["st_teff"] >= 3700) &
    (hab_df["st_teff"] <= 7200)
]
out_hz = hab_df[~hab_df.index.isin(in_hz.index)]

col_hz1, col_hz2 = st.columns([2, 1])

with col_hz1:
    fig_hz = go.Figure()

    fig_hz.add_trace(go.Scatter(
        x=out_hz["pl_orbsmax"],
        y=out_hz["st_teff"],
        mode="markers",
        marker=dict(color="steelblue", size=4, opacity=0.4),
        name="Outside HZ",
        hovertext=out_hz["pl_name"]
    ))

    fig_hz.add_trace(go.Scatter(
        x=in_hz["pl_orbsmax"],
        y=in_hz["st_teff"],
        mode="markers",
        marker=dict(color="limegreen", size=8, opacity=0.9, symbol="star"),
        name="🌱 In Habitable Zone",
        hovertext=in_hz["pl_name"]
    ))

    fig_hz.add_vrect(x0=0.5, x1=2.0, fillcolor="green", opacity=0.06, line_width=0)
    fig_hz.add_hrect(y0=3700, y1=7200, fillcolor="yellow", opacity=0.04, line_width=0)

    fig_hz.update_layout(
        xaxis_title="Orbital Distance (AU)",
        yaxis_title="Star Temperature (K)",
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(bgcolor="rgba(0,0,0,0)")
    )
    st.plotly_chart(fig_hz, use_container_width=True)

with col_hz2:
    st.markdown("### 🌍 Habitable Zone Stats")
    total = len(hab_df)
    hz_count = len(in_hz)
    pct = (hz_count / total * 100) if total > 0 else 0

    st.metric("Planets in HZ", hz_count)
    st.metric("Total Analyzed", total)
    st.metric("HZ Percentage", f"{pct:.1f}%")

    st.markdown("---")
    st.markdown("**Habitable Zone Criteria:**")
    st.markdown("- Orbital distance: 0.5–2.0 AU")
    st.markdown("- Star temperature: 3,700–7,200 K")

    if not in_hz.empty:
        st.markdown("---")
        st.markdown("**🌟 Top HZ Candidates:**")
        top = in_hz.nsmallest(5, "pl_rade")[["pl_name", "pl_rade", "pl_orbsmax"]]
        top.columns = ["Planet", "Radius (R⊕)", "Distance (AU)"]
        st.dataframe(top, hide_index=True, use_container_width=True)

st.markdown("---")

# -------------------------------------------------
# AI Summary Section
# -------------------------------------------------

st.subheader("🤖 AI Summary")

summary_target = st.selectbox(
    "Summarize which view?",
    ["All filtered results", "Habitable zone candidates only"]
)

if st.button("✨ Generate AI Summary", type="primary"):
    target_df = in_hz if summary_target == "Habitable zone candidates only" else filtered

    stats = {
        "total_planets": len(target_df),
        "year_range": f"{year_range[0]}–{year_range[1]}",
        "top_methods": target_df["discoverymethod"].value_counts().head(3).to_dict(),
        "avg_radius": round(target_df["pl_rade"].mean(), 2) if not target_df["pl_rade"].isna().all() else "N/A",
        "avg_distance": round(target_df["pl_orbsmax"].mean(), 2) if not target_df["pl_orbsmax"].isna().all() else "N/A",
        "habitable_zone_count": len(in_hz),
        "filter_method": selected_method,
        "habitable_only": habitable_only
    }

    with st.spinner("🤖 Generating AI summary with Gemini..."):
        summary = get_ai_summary(stats)

    st.markdown(
        f"""
        <div style="background: rgba(100,100,255,0.08); border: 1px solid rgba(100,100,255,0.3);
        border-radius: 12px; padding: 1.5rem; color: #e0e0ff; line-height: 1.7;">
        {summary}
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# -------------------------------------------------
# Raw Data Table
# -------------------------------------------------

with st.expander("📋 View Raw Data"):
    display_cols = ["pl_name", "hostname", "discoverymethod", "disc_year", "pl_rade", "pl_masse", "pl_orbsmax", "st_teff"]
    available_cols = [c for c in display_cols if c in filtered.columns]
    rename_map = {
        "pl_name": "Planet", "hostname": "Host Star", "discoverymethod": "Method",
        "disc_year": "Year", "pl_rade": "Radius (R⊕)", "pl_masse": "Mass (M⊕)",
        "pl_orbsmax": "Distance (AU)", "st_teff": "Star Temp (K)"
    }
    st.dataframe(
        filtered[available_cols].rename(columns=rename_map),
        use_container_width=True,
        hide_index=True
    )
    st.caption(f"Showing {len(filtered):,} planets")