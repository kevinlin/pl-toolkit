import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


def plot_pie_chart_multi_col(summary_df, charts_per_row=3):
    """
    Display each user's time distribution in a multi-column layout.
    Only includes users who have at least one positive value.
    """
    filtered_users = [
        user for user in summary_df.index
        if (summary_df.loc[user] > 0).any()
    ]

    # Now display only the filtered users in multi-column format
    for i in range(0, len(filtered_users), charts_per_row):
        row_users = filtered_users[i: i + charts_per_row]
        cols = st.columns(len(row_users))

        for idx, user in enumerate(row_users):
            with cols[idx]:
                user_data = summary_df.loc[user]
                user_data = user_data[user_data > 0]

                # Create the figure
                fig, ax = plt.subplots(figsize=(4, 4))

                # Draw a pie with no slice labels, only percentages
                wedges, _, autotexts = ax.pie(
                    user_data,
                    labels=None,  # Omit labels on slices
                    autopct="%1.1f%%",  # Show only percentages
                    startangle=90
                )

                # Add a legend on the side for actual slice labels
                ax.legend(
                    wedges,
                    user_data.index,
                    title="Categories",
                    loc="upper center",
                    bbox_to_anchor=(0.5, -0.05),  # Shift legend below the chart
                    ncol=1  # Number of columns for legend items
                )

                # Force aspect ratio to be equal so it's always a circle
                ax.set_aspect("equal")

                ax.set_title(f"{user}'s Time Distribution", pad=20)
                st.pyplot(fig)


# UI Code
st.title("Time Distribution Dashboard")
st.write("Execute the python program below to generate the time distribution CSV file")
st.markdown("""
    ```shell
    python timesheet_review.py ./input/202502_ZE\ TimeSheet_OpHours.xlsx
    ```""")
st.write("Then upload the generated CSV file: `timesheet_entries.csv` below to view the time distribution")

distribution_csv = st.file_uploader("Upload Time Distribution CSV")
if distribution_csv is not None:
    # Summarize the time distribution
    df_summary = pd.read_csv(distribution_csv, index_col=0)
    plot_pie_chart_multi_col(df_summary)
