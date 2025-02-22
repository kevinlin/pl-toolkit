import pandas as pd
import streamlit as st

from timesheet_review import extract_user_row_mappings, extract_date_col_mappings, read_timesheet_entries_by_users

st.title("Vertec Timesheet Analyzer")

uploaded_file = st.file_uploader("Upload Vertec Timesheet")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, sheet_name="Sheet2", skiprows=0)

    user_row_mappings, category_row_indices = extract_user_row_mappings(df)
    date_col_mappings = extract_date_col_mappings(df)
    timesheet_entries = read_timesheet_entries_by_users(df, user_row_mappings, date_col_mappings)

    # Define color conditions
    def color_negative_red_positive_yellow(val):
        if val > 0:
            return 'background-color: pink'
        elif val < 0:
            return 'background-color: yellow'
        return ''

    # Apply styling to the DataFrame
    styled_timesheet = timesheet_entries.style.map(color_negative_red_positive_yellow)

    # Display the styled DataFrame
    st.dataframe(styled_timesheet)
