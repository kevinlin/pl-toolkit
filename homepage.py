import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from timesheet_review import (
    extract_date_col_mappings,
    extract_user_row_mappings,
    extract_weekend_col_mappings,
    read_timesheet_entries_by_users,
    read_weekend_timesheet_entries,
)


# Define color conditions
def color_negative_red_positive_yellow(val):
    if val > 0:
        return 'background-color: pink'
    elif val < 0:
        return 'background-color: yellow'
    return ''


# Streamlit Code
st.set_page_config(page_title="PL Toolkit", layout="wide", initial_sidebar_state="collapsed")

st.title("Vertec Timesheet Analyzer")

uploaded_file = st.file_uploader("Upload Vertec Timesheet")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, sheet_name="Sheet2", skiprows=0)

    user_row_mappings, category_row_indices = extract_user_row_mappings(df)
    date_col_mappings = extract_date_col_mappings(df)
    df_timesheet = read_timesheet_entries_by_users(df, user_row_mappings, date_col_mappings)

    weekend_col_mappings = extract_weekend_col_mappings(df)
    df_weekend = read_weekend_timesheet_entries(df, user_row_mappings, weekend_col_mappings)

    if not df_weekend.empty:
        submitted = df_timesheet["Submitted?"]
        date_only = df_timesheet.drop(columns=["Submitted?"])
        merged = pd.concat([date_only, df_weekend], axis=1)

        all_col_mappings = {**date_col_mappings, **weekend_col_mappings}
        ordered_cols = sorted(
            [c for c in merged.columns if c in all_col_mappings],
            key=lambda c: all_col_mappings[c],
        )
        df_timesheet = merged[ordered_cols]
        df_timesheet["Submitted?"] = submitted

    # Apply styling to the DataFrame
    styled_timesheet = df_timesheet.style.map(color_negative_red_positive_yellow)

    # Display the styled DataFrame
    st.dataframe(styled_timesheet)
