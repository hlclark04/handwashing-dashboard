# app.py
# Code assisted by ChatGPT (for assignment requirement)

import streamlit as st
import pandas as pd
import altair as alt

# -----------------------------
# LOAD DATA
# -----------------------------
# Make sure yearly_deaths_by_clinic.csv is in the same folder as this file.
df = pd.read_csv("yearly_deaths_by_clinic.csv")

# Convert year column to an integer year (e.g., 1841, 1842, ...)
df["year"] = pd.to_datetime(df["year"], format="%Y").dt.year

# -----------------------------
# APP TITLE + DESCRIPTION
# -----------------------------
st.title("The Handwashing Discovery: Dr. Ignaz Semmelweis")

st.write(
    """
    In the 1840s, Dr. Ignaz Semmelweis worked at the Vienna General Hospital and
    noticed a shocking pattern: far more mothers were dying from childbed fever in
    one maternity clinic than the other.
    
    By carefully tracking births and deaths over time, he discovered that simple
    handwashing with a chlorinated solution drastically reduced mortality.
    This dashboard recreates his data so we can see how powerful that change was.
    """
)

st.markdown("---")

# -----------------------------
# OPTIONAL FILTERS
# -----------------------------
st.subheader("Filter by Clinic")
clinics = df["clinic"].unique()
selected_clinic = st.selectbox("Choose a clinic:", clinics)

df_filtered = df[df["clinic"] == selected_clinic].copy()

# -----------------------------
# CALCULATE MORTALITY RATE
# -----------------------------
df_filtered["mortality_rate"] = df_filtered["deaths"] / df_filtered["births"]

# -----------------------------
# LINE CHART: MORTALITY RATE
# -----------------------------
st.subheader(f"Mortality Rate Over Time — {selected_clinic}")

line_chart = (
    alt.Chart(df_filtered)
    .mark_line(point=True)
    .encode(
        x=alt.X("year:O", title="Year"),
        y=alt.Y(
            "mortality_rate:Q",
            title="Mortality Rate",
            axis=alt.Axis(format=".0%")
        ),
        tooltip=[
            "year",
            "births",
            "deaths",
            alt.Tooltip("mortality_rate", format=".2%")
        ],
    )
    .properties(height=350)
    .interactive()
)

st.altair_chart(line_chart, use_container_width=True)

# -----------------------------
# BAR CHART: BIRTHS VS. DEATHS
# -----------------------------
st.subheader("Births vs. Deaths by Year")

bar_chart = (
    alt.Chart(df_filtered)
    .transform_fold(["births", "deaths"], as_=["Metric", "Count"])
    .mark_bar()
    .encode(
        x=alt.X("year:O", title="Year"),
        y=alt.Y("Count:Q", title="Number of Cases"),
        color="Metric:N",
        tooltip=["year", "Metric", "Count"],
    )
    .properties(height=350)
    .interactive()
)

st.altair_chart(bar_chart, use_container_width=True)

# -----------------------------
# FINDINGS TEXT
# -----------------------------
st.subheader("Key Takeaways")
st.write(
    """
    - Before handwashing was introduced, mortality rates in **Clinic 1** were
      consistently higher than in Clinic 2.
    - After Semmelweis required handwashing with a chlorinated solution around 1847,
      mortality rates dropped sharply, especially in Clinic 1.
    - The pattern in this data strongly supports Semmelweis’s claim that **hand hygiene
      was the critical factor** in preventing childbed fever.
    
    In short, these numbers show that a simple change in behavior — washing hands —
    saved many lives.
    """
)

st.caption("Data source: Reconstructed Semmelweis clinic records (Datacamp / course materials).")
