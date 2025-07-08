import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(page_title="User Activity Dashboard", layout="wide")

st.title("User Activity Dashboard")
st.header("Weekly User Activity Analysis")

# File upload section
st.subheader("📁 Upload Your Data")
uploaded_file = st.file_uploader(
    "Choose a CSV file", 
    type="csv",
    help="Upload a CSV file with weekly user activity data"
)

# Only proceed if a file is uploaded
if uploaded_file is not None:
    try:
        # Load data from uploaded file
        df = pd.read_csv(uploaded_file)
        
        # Validate required columns
        required_columns = ['country', 'division', 'fullName', 'fromDate', 'toDate', 'logins']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"Missing required columns: {', '.join(missing_columns)}")
            st.info("Required columns: country, division, fullName, fromDate, toDate, logins")
            st.stop()
        
        # Data preprocessing
        df['fromDate'] = pd.to_datetime(df['fromDate'], format='%Y%m%d')
        df['toDate'] = pd.to_datetime(df['toDate'], format='%Y%m%d')
        df['week_period'] = df['fromDate'].dt.strftime('%Y-%m-%d') + ' to ' + df['toDate'].dt.strftime('%Y-%m-%d')
        
        # Display data preview
        st.subheader("📋 Data Preview")
        st.write(f"Loaded {len(df)} weekly records")
        preview_cols = ['fullName', 'country', 'division', 'week_period', 'logins']
        if 'salesRepEmail' in df.columns:
            preview_cols.insert(-1, 'salesRepEmail')
        st.dataframe(df[preview_cols].head(10), use_container_width=True)
        
        # Aggregate user data across all weeks
        user_totals = df.groupby(['fullName', 'country', 'division']).agg({
            'logins': 'sum',
            'week_period': 'count'
        }).reset_index()
        user_totals.columns = ['fullName', 'country', 'division', 'total_logins', 'weeks_active']
        
        # Filter out users with zero logins
        active_users = user_totals[user_totals['total_logins'] > 0].copy()
        active_users = active_users.sort_values(['country', 'total_logins'], ascending=[True, False])

        # Display basic statistics
        st.subheader("📊 Overview")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Users", len(user_totals))
        with col2:
            st.metric("Active Users", len(active_users))
        with col3:
            st.metric("Countries", df['country'].nunique())

        date_range = f"{df['fromDate'].min().strftime('%Y-%m-%d')} to {df['toDate'].max().strftime('%Y-%m-%d')}"
        st.metric("Date Range", date_range)

        # Weekly Activity Trends
        st.subheader("📈 Weekly Activity Trends")
        weekly_summary = df.groupby(['fromDate', 'week_period']).agg({
            'logins': 'sum',
            'fullName': 'nunique'
        }).reset_index()
        weekly_summary.columns = ['fromDate', 'week_period', 'total_logins', 'active_users']
        
        # Create weekly trend chart
        fig_weekly, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Total logins per week
        ax1.plot(weekly_summary['fromDate'], weekly_summary['total_logins'], 
                marker='o', linewidth=2, color='steelblue')
        ax1.set_title('Total Logins per Week')
        ax1.set_ylabel('Total Logins')
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)
        
        # Active users per week
        ax2.plot(weekly_summary['fromDate'], weekly_summary['active_users'], 
                marker='s', linewidth=2, color='darkgreen')
        ax2.set_title('Active Users per Week')
        ax2.set_ylabel('Number of Active Users')
        ax2.set_xlabel('Week')
        ax2.grid(True, alpha=0.3)
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        st.pyplot(fig_weekly)

        # User input for top N users per country
        st.subheader("🎯 Filter Options")
        top_n = st.slider("Select top N users per country", min_value=3, max_value=10, value=5)

        # Get top N users per country (by total logins)
        top_users_by_country = active_users.groupby('country').head(top_n).reset_index(drop=True)

        # Display country-wise breakdown
        st.subheader("🌍 Country Breakdown - Top Users (Total Logins)")
        for country in df['country'].unique():
            country_data = active_users[active_users['country'] == country].head(top_n)
            if not country_data.empty:
                st.write(f"**{country}** - Top {min(top_n, len(country_data))} Users:")
                display_df = country_data[['fullName', 'division', 'total_logins', 'weeks_active']].copy()
                display_df.columns = ['Full Name', 'Division', 'Total Logins', 'Weeks Active']
                st.dataframe(display_df, use_container_width=True, hide_index=True)

        # Streamlit bar chart for top users
        st.subheader("📊 Top Users by Total Login Count")
        chart_data = top_users_by_country.set_index('fullName')['total_logins']
        st.bar_chart(chart_data)

        # Detailed visualization
        st.subheader("📊 Detailed Analysis")

        # Create matplotlib figure for country and user analysis
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        # Chart 1: Total logins by country
        country_totals = active_users.groupby('country')['total_logins'].sum().sort_values(ascending=True)
        colors = plt.cm.Set3(np.linspace(0, 1, len(country_totals)))

        bars1 = ax1.barh(country_totals.index, country_totals.values, color=colors)
        ax1.set_xlabel('Total Login Count (All Weeks)')
        ax1.set_title('Total Logins by Country')
        ax1.grid(axis='x', alpha=0.3)

        # Add value labels on bars
        for i, (country, value) in enumerate(country_totals.items()):
            ax1.text(value + 0.5, i, str(value), va='center', fontweight='bold')

        # Chart 2: Top users overall
        top_users_overall = active_users.head(top_n * 2)
        user_labels = [f"{name}\n({country})" for name, country in 
                       zip(top_users_overall['fullName'], top_users_overall['country'])]

        bars2 = ax2.bar(range(len(top_users_overall)), top_users_overall['total_logins'], 
                        color=plt.cm.viridis(np.linspace(0, 1, len(top_users_overall))))
        ax2.set_xlabel('Users')
        ax2.set_ylabel('Total Login Count')
        ax2.set_title(f'Top {len(top_users_overall)} Users Overall')
        ax2.set_xticks(range(len(top_users_overall)))
        ax2.set_xticklabels(user_labels, rotation=45, ha='right', fontsize=8)
        ax2.grid(axis='y', alpha=0.3)

        # Add value labels on bars
        for i, value in enumerate(top_users_overall['total_logins']):
            ax2.text(i, value + 0.1, str(value), ha='center', va='bottom', fontweight='bold')

        plt.tight_layout()
        st.pyplot(fig)

        # Activity breakdown analysis (if additional columns are available)
        view_columns = [col for col in df.columns if 'view' in col.lower() or 'create' in col.lower()]
        if view_columns:
            st.subheader("🔍 Activity Breakdown Analysis")
            
            # Calculate total activity across all view types
            activity_totals = {}
            for col in view_columns:
                if df[col].dtype in ['int64', 'float64']:
                    total = df[col].sum()
                    if total > 0:
                        activity_totals[col.replace('Counts', '').replace('view', '').replace('create', '')] = total
            
            if activity_totals:
                # Create activity breakdown chart
                fig_activity, ax = plt.subplots(figsize=(12, 6))
                activities = list(activity_totals.keys())
                values = list(activity_totals.values())
                
                bars = ax.bar(activities, values, color=plt.cm.tab20(np.linspace(0, 1, len(activities))))
                ax.set_title('Total Activity Breakdown (All Weeks)')
                ax.set_ylabel('Total Count')
                ax.set_xlabel('Activity Type')
                plt.xticks(rotation=45, ha='right')
                ax.grid(axis='y', alpha=0.3)
                
                # Add value labels
                for bar, value in zip(bars, values):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                           f'{int(value)}', ha='center', va='bottom')
                
                plt.tight_layout()
                st.pyplot(fig_activity)

        # Summary table by country
        st.subheader("📋 Summary by Country")
        country_summary = user_totals.groupby('country').agg({
            'total_logins': ['count', 'sum', 'mean', 'max'],
            'weeks_active': 'mean'
        }).round(2)

        country_summary.columns = ['Total Users', 'Total Logins', 'Avg Logins per User', 'Max User Logins', 'Avg Weeks Active']
        st.dataframe(country_summary, use_container_width=True)

        # Weekly summary table
        st.subheader("📅 Weekly Summary")
        st.dataframe(weekly_summary[['week_period', 'total_logins', 'active_users']], use_container_width=True, hide_index=True)

        # Additional insights
        st.subheader("💡 Key Insights")
        most_active_country = active_users.groupby('country')['total_logins'].sum().idxmax()
        most_active_user = active_users.loc[active_users['total_logins'].idxmax()]
        most_active_week = weekly_summary.loc[weekly_summary['total_logins'].idxmax()]

        st.write(f"• **Most Active Country**: {most_active_country} with {active_users[active_users['country'] == most_active_country]['total_logins'].sum()} total logins")
        st.write(f"• **Most Active User**: {most_active_user['fullName']} from {most_active_user['country']} with {most_active_user['total_logins']} total logins across {most_active_user['weeks_active']} weeks")
        st.write(f"• **Most Active Week**: {most_active_week['week_period']} with {most_active_week['total_logins']} total logins")
        st.write(f"• **Average Logins per Active User**: {active_users['total_logins'].mean():.1f}")
        st.write(f"• **Total Active Users**: {len(active_users)} out of {len(user_totals)} users ({len(active_users)/len(user_totals)*100:.1f}%)")
        st.write(f"• **Average Weeks Active per User**: {user_totals['weeks_active'].mean():.1f}")

    except Exception as e:
        st.error(f"Error reading the CSV file: {str(e)}")
        st.info("Please make sure your CSV file is properly formatted and contains the required columns.")

else:
    # Show instructions when no file is uploaded
    st.info("👆 Please upload a CSV file to get started!")
    
    st.subheader("📝 File Format Requirements")
    st.write("Your CSV file should contain weekly user activity data with the following columns:")
    
    sample_data = {
        'country': ['Malaysia', 'Singapore', 'Malaysia'],
        'division': ['Endo', 'PI', 'IC'],
        'fullName': ['John Doe', 'Jane Smith', 'Bob Johnson'],
        'salesRepEmail': ['john.doe@company.com', 'jane.smith@company.com', 'bob.johnson@company.com'],
        'fromDate': ['20250616', '20250616', '20250623'],
        'toDate': ['20250622', '20250622', '20250629'],
        'logins': [12, 5, 8]
    }
    sample_df = pd.DataFrame(sample_data)
    
    st.dataframe(sample_df, use_container_width=True, hide_index=True)
    
    st.write("**Required Column Descriptions:**")
    st.write("- **country**: Country where the user is located")
    st.write("- **division**: User's department or division") 
    st.write("- **fullName**: User's full name")
    st.write("- **fromDate**: Start date of the week (format: YYYYMMDD)")
    st.write("- **toDate**: End date of the week (format: YYYYMMDD)")
    st.write("- **logins**: Number of login sessions for the user in that week")
    
    st.write("**Optional columns can include:**")
    st.write("- **salesRepEmail**: User's email address")
    st.write("- **dailyPointAwarded_days**: Daily points awarded")
    st.write("- **Various view counts**: Additional activity metrics (viewHomeCounts, createEvents, etc.)")
