"""
Wildlife Health Watch Dashboard
Smithsonian Global Health Program - Kenya Syndromic Surveillance

A streamlit dashboard for visualizing wildlife health surveillance data.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Wildlife Health Watch",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1B4332;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1rem;
        color: #52796F;
        margin-top: 0;
    }
    .metric-card {
        background-color: #F8F9FA;
        border-radius: 10px;
        padding: 20px;
        border-left: 4px solid #2D6A4F;
    }
    .stMetric {
        background-color: #F8F9FA;
        padding: 15px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load and preprocess surveillance data."""
    # Generate synthetic data inline for demo
    np.random.seed(42)

    regions = {
        "Maasai Mara": (-1.4833, 35.1333),
        "Amboseli": (-2.6527, 37.2606),
        "Tsavo East": (-2.6857, 38.7578),
        "Tsavo West": (-3.0167, 38.0667),
        "Samburu": (0.5833, 37.5333),
        "Lake Nakuru": (-0.3667, 36.0833),
        "Nairobi NP": (-1.3733, 36.8581),
        "Meru": (0.0500, 38.1833),
    }

    species_list = [
        "African Elephant", "Lion", "Zebra", "Giraffe", "Buffalo",
        "Wildebeest", "Hippopotamus", "Rhino", "Cheetah", "Hyena"
    ]

    syndromes = [
        "Respiratory", "Gastrointestinal", "Neurological", "Dermatological",
        "Musculoskeletal", "Sudden Death", "Reproductive", "Ocular"
    ]

    severity_levels = ["Low", "Moderate", "High", "Critical"]
    status_options = ["Active", "Resolved", "Under Investigation"]

    n_records = 500
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    data = []
    for i in range(n_records):
        region = np.random.choice(list(regions.keys()))
        lat, lon = regions[region]
        lat += np.random.normal(0, 0.1)
        lon += np.random.normal(0, 0.1)

        days_offset = np.random.randint(0, 365)
        report_date = start_date + timedelta(days=days_offset)

        species = np.random.choice(species_list, p=[0.15, 0.08, 0.20, 0.12, 0.18, 0.12, 0.05, 0.02, 0.03, 0.05])
        syndrome = np.random.choice(syndromes)
        severity = np.random.choice(severity_levels, p=[0.40, 0.35, 0.20, 0.05])

        days_ago = (end_date - report_date).days
        if days_ago < 14:
            status = np.random.choice(status_options, p=[0.60, 0.20, 0.20])
        elif days_ago < 60:
            status = np.random.choice(status_options, p=[0.30, 0.50, 0.20])
        else:
            status = np.random.choice(status_options, p=[0.10, 0.80, 0.10])

        n_affected = np.random.randint(1, 10)

        data.append({
            "case_id": f"WHW-2024-{i+1:04d}",
            "report_date": report_date,
            "region": region,
            "latitude": round(lat, 4),
            "longitude": round(lon, 4),
            "species": species,
            "syndrome": syndrome,
            "severity": severity,
            "status": status,
            "animals_affected": n_affected,
        })

    df = pd.DataFrame(data)
    df = df.sort_values("report_date").reset_index(drop=True)
    return df


def create_map(df):
    """Create an interactive map of surveillance events."""
    color_map = {
        "Low": "#95D5B2",
        "Moderate": "#74C69D",
        "High": "#F4A261",
        "Critical": "#E63946"
    }

    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        color="severity",
        size="animals_affected",
        hover_name="case_id",
        hover_data=["species", "syndrome", "region", "report_date"],
        color_discrete_map=color_map,
        zoom=5.5,
        center={"lat": -1.0, "lon": 37.5},
        mapbox_style="carto-positron",
        title=""
    )

    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=450,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig


def create_timeline(df):
    """Create a timeline of cases."""
    daily = df.groupby(df["report_date"].dt.to_period("W")).agg({
        "case_id": "count",
        "animals_affected": "sum"
    }).reset_index()
    daily["report_date"] = daily["report_date"].astype(str)
    daily.columns = ["Week", "Cases", "Animals Affected"]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=daily["Week"],
        y=daily["Cases"],
        name="Cases",
        marker_color="#2D6A4F"
    ))

    fig.update_layout(
        title=dict(text="Weekly Case Reports", y=0.95),
        xaxis_title="Week",
        yaxis_title="Number of Cases",
        height=350,
        margin=dict(l=40, r=40, t=60, b=40),
        showlegend=False
    )

    return fig


def create_species_chart(df):
    """Create species distribution chart."""
    species_counts = df["species"].value_counts().reset_index()
    species_counts.columns = ["Species", "Count"]

    fig = px.bar(
        species_counts,
        x="Count",
        y="Species",
        orientation="h",
        color="Count",
        color_continuous_scale=["#95D5B2", "#2D6A4F"]
    )

    fig.update_layout(
        title="Cases by Species",
        height=350,
        margin=dict(l=40, r=40, t=40, b=40),
        showlegend=False,
        coloraxis_showscale=False
    )

    return fig


def create_syndrome_chart(df):
    """Create syndrome distribution chart."""
    syndrome_counts = df["syndrome"].value_counts().reset_index()
    syndrome_counts.columns = ["Syndrome", "Count"]

    fig = px.pie(
        syndrome_counts,
        values="Count",
        names="Syndrome",
        color_discrete_sequence=px.colors.sequential.Greens_r,
        hole=0.4
    )

    fig.update_layout(
        title="Syndrome Distribution",
        height=350,
        margin=dict(l=40, r=40, t=40, b=40),
    )

    return fig


def main():
    # Load data
    df = load_data()

    # Header
    st.markdown('<p class="main-header">🦁 Wildlife Health Watch</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Kenya Syndromic Surveillance Dashboard | Smithsonian Global Health Program</p>', unsafe_allow_html=True)
    st.markdown("---")

    # Sidebar filters
    st.sidebar.header("🔍 Filters")

    # Date range filter
    min_date = df["report_date"].min().date()
    max_date = df["report_date"].max().date()

    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # Region filter
    regions = ["All"] + sorted(df["region"].unique().tolist())
    selected_region = st.sidebar.selectbox("Region", regions)

    # Species filter
    species = ["All"] + sorted(df["species"].unique().tolist())
    selected_species = st.sidebar.selectbox("Species", species)

    # Severity filter
    severity_options = ["All"] + ["Critical", "High", "Moderate", "Low"]
    selected_severity = st.sidebar.multiselect(
        "Severity",
        severity_options[1:],
        default=severity_options[1:]
    )

    # Status filter
    status_options = df["status"].unique().tolist()
    selected_status = st.sidebar.multiselect(
        "Status",
        status_options,
        default=status_options
    )

    # Apply filters
    filtered_df = df.copy()

    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df["report_date"].dt.date >= date_range[0]) &
            (filtered_df["report_date"].dt.date <= date_range[1])
        ]

    if selected_region != "All":
        filtered_df = filtered_df[filtered_df["region"] == selected_region]

    if selected_species != "All":
        filtered_df = filtered_df[filtered_df["species"] == selected_species]

    if selected_severity:
        filtered_df = filtered_df[filtered_df["severity"].isin(selected_severity)]

    if selected_status:
        filtered_df = filtered_df[filtered_df["status"].isin(selected_status)]

    # Key metrics
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            label="Total Cases",
            value=len(filtered_df),
            delta=f"{len(filtered_df[filtered_df['report_date'] > datetime.now() - timedelta(days=30)])} this month"
        )

    with col2:
        active_cases = len(filtered_df[filtered_df["status"] == "Active"])
        st.metric(
            label="Active Cases",
            value=active_cases,
            delta=None
        )

    with col3:
        critical_cases = len(filtered_df[filtered_df["severity"] == "Critical"])
        st.metric(
            label="Critical Alerts",
            value=critical_cases,
            delta=None
        )

    with col4:
        total_animals = filtered_df["animals_affected"].sum()
        st.metric(
            label="Animals Affected",
            value=f"{total_animals:,}",
            delta=None
        )

    with col5:
        regions_affected = filtered_df["region"].nunique()
        st.metric(
            label="Regions Monitored",
            value=regions_affected,
            delta=None
        )

    st.markdown("---")

    # Map and timeline
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("📍 Geographic Distribution")
        if len(filtered_df) > 0:
            st.plotly_chart(create_map(filtered_df), use_container_width=True)
        else:
            st.warning("No data available for selected filters.")

    with col_right:
        st.subheader("📈 Case Trends")
        if len(filtered_df) > 0:
            st.plotly_chart(create_timeline(filtered_df), use_container_width=True)
        else:
            st.warning("No data available for selected filters.")

    st.markdown("---")

    # Species and syndrome charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🦒 Species Analysis")
        if len(filtered_df) > 0:
            st.plotly_chart(create_species_chart(filtered_df), use_container_width=True)

    with col2:
        st.subheader("🔬 Syndrome Distribution")
        if len(filtered_df) > 0:
            st.plotly_chart(create_syndrome_chart(filtered_df), use_container_width=True)

    st.markdown("---")

    # Recent cases table
    st.subheader("📋 Recent Cases")

    recent_df = filtered_df.sort_values("report_date", ascending=False).head(10)

    display_df = recent_df[["case_id", "report_date", "region", "species", "syndrome", "severity", "status", "animals_affected"]].copy()
    display_df["report_date"] = display_df["report_date"].dt.strftime("%Y-%m-%d")
    display_df.columns = ["Case ID", "Date", "Region", "Species", "Syndrome", "Severity", "Status", "Animals"]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #6C757D; font-size: 0.8rem;'>
        Wildlife Health Watch | Smithsonian Global Health Program | Kenya Wildlife Service<br>
        Dashboard Demo v1.0 | Data shown is synthetic for demonstration purposes
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
