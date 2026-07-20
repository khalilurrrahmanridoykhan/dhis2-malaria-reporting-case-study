"""Interactive dashboard for the synthetic DHIS2 malaria case study."""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "synthetic_malaria_monthly.csv"

st.set_page_config(
    page_title="Malaria Programme Overview — DEMO",
    page_icon="📊",
    layout="wide",
)


@st.cache_data
def load_data() -> pd.DataFrame:
    frame = pd.read_csv(DATA_FILE, dtype={"period": str})
    frame["month"] = pd.to_datetime(frame["period"], format="%Y%m")
    frame["total_tests"] = frame["tests_rdt"] + frame["tests_microscopy"]
    return frame


def safe_ratio(numerator: float, denominator: float, factor: float = 100) -> float | None:
    return numerator / denominator * factor if denominator else None


data = load_data()

st.title("Malaria Programme Overview — DEMO")
st.caption("Independent portfolio demonstration using entirely synthetic aggregate data")
st.warning(
    "Educational case study only. This dashboard is not an official surveillance, "
    "diagnostic, clinical, or outbreak-warning system."
)

with st.sidebar:
    st.header("Filters")
    upazilas = st.multiselect("Upazila", sorted(data["upazila"].unique()))
    facilities = st.multiselect("Facility", sorted(data["facility"].unique()))
    min_month, max_month = data["month"].min().date(), data["month"].max().date()
    start_month, end_month = st.date_input(
        "Reporting period",
        value=(min_month, max_month),
        min_value=min_month,
        max_value=max_month,
    )

filtered = data.copy()
if upazilas:
    filtered = filtered[filtered["upazila"].isin(upazilas)]
if facilities:
    filtered = filtered[filtered["facility"].isin(facilities)]
filtered = filtered[
    (filtered["month"].dt.date >= start_month)
    & (filtered["month"].dt.date <= end_month)
]

confirmed = int(filtered["confirmed_cases"].sum())
tests = int(filtered["total_tests"].sum())
deaths = int(filtered["malaria_deaths"].sum())
reports_expected = int(filtered["reports_expected"].sum())
reports_received = int(filtered["reports_received"].sum())

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Confirmed cases", f"{confirmed:,}")
kpi2.metric("Test positivity", f"{safe_ratio(confirmed, tests) or 0:.1f}%")
kpi3.metric("Malaria deaths", f"{deaths:,}")
kpi4.metric("Reporting completeness", f"{safe_ratio(reports_received, reports_expected) or 0:.1f}%")

monthly = (
    filtered.groupby("month", as_index=False)
    .agg(confirmed_cases=("confirmed_cases", "sum"), total_tests=("total_tests", "sum"))
)
monthly["test_positivity_pct"] = monthly["confirmed_cases"].div(monthly["total_tests"]).mul(100)

left, right = st.columns(2)
with left:
    st.subheader("Confirmed cases by month")
    st.plotly_chart(
        px.line(monthly, x="month", y="confirmed_cases", markers=True, labels={"confirmed_cases": "Cases"}),
        use_container_width=True,
    )
with right:
    st.subheader("Test positivity by month")
    st.plotly_chart(
        px.line(
            monthly,
            x="month",
            y="test_positivity_pct",
            markers=True,
            labels={"test_positivity_pct": "Positivity (%)"},
        ),
        use_container_width=True,
    )

facility_summary = (
    filtered.groupby(["upazila", "facility"], as_index=False)
    .agg(
        confirmed_cases=("confirmed_cases", "sum"),
        total_tests=("total_tests", "sum"),
        reports_expected=("reports_expected", "sum"),
        reports_received=("reports_received", "sum"),
        stockout_days=("stockout_days", "sum"),
    )
)
facility_summary["test_positivity_pct"] = (
    facility_summary["confirmed_cases"].div(facility_summary["total_tests"]).mul(100)
)
facility_summary["reporting_completeness_pct"] = (
    facility_summary["reports_received"].div(facility_summary["reports_expected"]).mul(100)
)

left, right = st.columns(2)
with left:
    st.subheader("Confirmed cases by facility")
    st.plotly_chart(
        px.bar(
            facility_summary.sort_values("confirmed_cases"),
            x="confirmed_cases",
            y="facility",
            color="upazila",
            orientation="h",
            labels={"confirmed_cases": "Cases", "facility": "Facility"},
        ),
        use_container_width=True,
    )
with right:
    st.subheader("Case-origin distribution")
    origin = pd.DataFrame(
        {
            "Origin": ["Indigenous", "Imported"],
            "Cases": [filtered["indigenous_cases"].sum(), filtered["imported_cases"].sum()],
        }
    )
    st.plotly_chart(px.pie(origin, names="Origin", values="Cases", hole=0.55), use_container_width=True)

st.subheader("Reporting and commodity review")
reporting_table = facility_summary[
    [
        "upazila",
        "facility",
        "confirmed_cases",
        "test_positivity_pct",
        "reporting_completeness_pct",
        "stockout_days",
    ]
].copy()
reporting_table["test_positivity_pct"] = reporting_table["test_positivity_pct"].map(
    lambda value: f"{value:.1f}%"
)
reporting_table["reporting_completeness_pct"] = reporting_table[
    "reporting_completeness_pct"
].map(lambda value: f"{value:.1f}%")
st.dataframe(
    reporting_table,
    use_container_width=True,
    hide_index=True,
)

st.download_button(
    "Download filtered synthetic data",
    filtered.drop(columns=["month", "total_tests"]).to_csv(index=False).encode("utf-8"),
    file_name="filtered_synthetic_malaria_data.csv",
    mime="text/csv",
)
