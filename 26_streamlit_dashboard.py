
from pathlib import Path
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Nassau Candy | Factory Optimization",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 Nassau Candy Distributor")
st.subheader("Factory Reallocation & Shipping Optimization Recommendation System")

st.markdown("""
An interactive decision-support dashboard for factory candidate
comparison, scenario analysis, business impact and recommendations.
""")

# =====================================================
# PROJECT FOLDER
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

# Search main folder and all subfolders
def find_csv(filename):

    matches = list(BASE_DIR.rglob(filename))

    if matches:
        return matches[0]

    return None


def load_csv(filename):

    file_path = find_csv(filename)

    if file_path is None:
        return None

    try:
        return pd.read_csv(file_path)
    except Exception as error:
        st.warning(f"Could not read {filename}: {error}")
        return None


# =====================================================
# LOAD PROJECT OUTPUT FILES
# =====================================================

files = {
    "impact": "nassau_cost_savings_impact_analysis.csv",
    "business": "nassau_business_impact_summary.csv",
    "factory": "nassau_factory_business_impact_summary.csv",
    "recommendations": "nassau_factory_recommendation_system.csv",
    "scenarios": "nassau_factory_scenario_simulation.csv",
    "insights": "nassau_final_business_insights.csv"
}

data = {}

for key, filename in files.items():
    data[key] = load_csv(filename)

available = {
    key: value for key, value in data.items()
    if value is not None
}

if not available:
    st.error("No project CSV files found.")
    st.write("Dashboard folder:", str(BASE_DIR))
    st.write("CSV files detected:")

    for path in BASE_DIR.rglob("*.csv"):
        st.write(str(path.relative_to(BASE_DIR)))

    st.stop()

st.success(
    f"{len(available)} out of {len(files)} project output files loaded successfully."
)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Dashboard Section",
    [
        "Overview",
        "Factory Recommendations",
        "Business Impact",
        "Scenario Analysis",
        "Data Explorer",
        "Project Information"
    ]
)

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def show_dataframe(df):

    if df is not None and not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No data available for this section.")


def show_download(df, filename):

    if df is not None and not df.empty:
        st.download_button(
            label=f"Download {filename}",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name=filename,
            mime="text/csv"
        )


def find_column(df, possible_names):

    if df is None:
        return None

    for name in possible_names:
        if name in df.columns:
            return name

    return None


def show_numeric_summary(df):

    if df is None or df.empty:
        return

    numeric = df.select_dtypes(include="number")

    if not numeric.empty:
        st.write("Numerical Summary")
        st.dataframe(
            numeric.describe().round(2),
            use_container_width=True
        )


# =====================================================
# 1. OVERVIEW
# =====================================================

if page == "Overview":

    st.header("Project Overview")

    c1, c2, c3 = st.columns(3)

    rec = data["recommendations"]
    scenarios = data["scenarios"]
    impact = data["impact"]

    with c1:
        st.metric(
            "Recommendation Records",
            len(rec) if rec is not None else 0
        )

    with c2:
        st.metric(
            "Scenario Records",
            len(scenarios) if scenarios is not None else 0
        )

    with c3:
        st.metric(
            "Impact Analysis Records",
            len(impact) if impact is not None else 0
        )

    st.divider()

    st.subheader("Project Objectives")

    st.markdown("""
    - Compare current and alternative factory assignments.
    - Evaluate factory candidates using available business indicators.
    - Analyze product and destination-region scenarios.
    - Generate factory reallocation recommendations.
    - Present business insights through interactive visualizations.
    """)

    st.subheader("Available Project Files")

    for key, filename in files.items():

        if data[key] is not None:
            st.write("✅", filename)
        else:
            st.write("⚠️", filename, "- Not found")


# =====================================================
# 2. FACTORY RECOMMENDATIONS
# =====================================================

elif page == "Factory Recommendations":

    st.header("Factory Recommendation System")

    df = data["recommendations"]

    show_dataframe(df)

    if df is not None and not df.empty:

        st.subheader("Recommended Factory Analysis")

        factory_col = find_column(
            df,
            ["Recommended_Factory", "Recommended Factory",
             "Candidate Factory", "Factory"]
        )

        if factory_col:

            counts = df[factory_col].value_counts()

            st.bar_chart(counts)

            st.write("Factory Recommendation Counts")
            st.dataframe(counts.rename("Recommendations"))

        show_download(
            df,
            "nassau_factory_recommendations.csv"
        )


# =====================================================
# 3. BUSINESS IMPACT
# =====================================================

elif page == "Business Impact":

    st.header("Business Impact Analysis")

    df = data["impact"]

    if df is None:
        df = data["business"]

    if df is not None:

        show_dataframe(df)

        st.subheader("Available Business Metrics")

        numeric = df.select_dtypes(include="number")

        if not numeric.empty:

            metric = st.selectbox(
                "Select a metric",
                numeric.columns
            )

            st.bar_chart(df[metric].dropna())

        st.info(
            "Factory Relocation Distance KM represents distance "
            "between the current factory and an alternative factory. "
            "It is not a verified customer shipping-distance saving."
        )

        show_download(
            df,
            "nassau_business_impact.csv"
        )

    else:
        st.warning("Business impact output is unavailable.")


# =====================================================
# 4. SCENARIO ANALYSIS
# =====================================================

elif page == "Scenario Analysis":

    st.header("Factory Scenario Analysis")

    df = data["scenarios"]

    show_dataframe(df)

    if df is not None and not df.empty:

        numeric = df.select_dtypes(include="number")

        if not numeric.empty:

            st.subheader("Scenario Metric Visualization")

            metric = st.selectbox(
                "Choose scenario metric",
                numeric.columns,
                key="scenario_metric"
            )

            st.bar_chart(df[metric].dropna())

        show_download(
            df,
            "nassau_factory_scenarios.csv"
        )


# =====================================================
# 5. DATA EXPLORER
# =====================================================

elif page == "Data Explorer":

    st.header("Project Data Explorer")

    available_names = [
        key for key, value in data.items()
        if value is not None
    ]

    selected = st.selectbox(
        "Choose dataset",
        available_names
    )

    df = data[selected]

    st.write("Dataset Shape:", df.shape)

    st.write("Column Names")
    st.write(df.columns.tolist())

    st.subheader("Dataset Preview")

    show_dataframe(df)

    st.subheader("Missing Values")

    missing = df.isnull().sum()

    st.dataframe(
        missing.rename("Missing Values"),
        use_container_width=True
    )

    show_numeric_summary(df)

    show_download(
        df,
        f"{selected}_data.csv"
    )


# =====================================================
# 6. PROJECT INFORMATION
# =====================================================

elif page == "Project Information":

    st.header("About This Project")

    st.markdown("""
    **Project Title:**

    Factory Reallocation & Shipping Optimization
    Recommendation System for Nassau Candy Distributor

    **Project Type:** Supply Chain Data Analytics and Decision Support

    **Tools Used:**
    - Python
    - Pandas
    - NumPy
    - Scikit-learn
    - Matplotlib
    - Streamlit

    **Project Workflow:**
    1. Data preparation
    2. Factory candidate comparison
    3. Reallocation impact assessment
    4. Scenario simulation
    5. Factory recommendation generation
    6. Business impact analysis
    7. Data visualization
    8. Interactive dashboard
    """)

    st.info(
        "Recommendations are analytical suggestions for review. "
        "Actual transportation savings require customer destination "
        "distances, freight rates, factory capacities and operational validation."
    )

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Nassau Candy Distributor | Factory Reallocation Analytics | "
    "Python & Streamlit Project"
)
