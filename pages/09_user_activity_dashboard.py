import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(page_title="User Activity Dashboard", layout="wide")

# =============================================================================
# STYLING CONSTANTS
# =============================================================================
# Color palettes for consistent styling
COLOR_PRIMARY = '#1f77b4'      # Blue
COLOR_SECONDARY = '#ff7f0e'    # Orange
COLOR_SUCCESS = '#2ca02c'      # Green
COLOR_DANGER = '#d62728'       # Red
COLOR_INFO = '#9467bd'         # Purple
COLOR_BACKGROUND = '#f8f9fa'   # Light gray for chart backgrounds

# Chart color schemes
COLORS_QUALITATIVE = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                      '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
COLORS_SEQUENTIAL_BLUE = plt.cm.Blues
COLORS_SEQUENTIAL_ORANGE = plt.cm.Oranges
COLORS_DIVERGING = plt.cm.RdYlGn

# =============================================================================
# HEADER
# =============================================================================
st.title("User Activity Dashboard")
st.markdown("### Weekly User Activity Analysis")

# =============================================================================
# FILE UPLOAD SECTION
# =============================================================================
st.markdown("---")
st.header("📁 Data Upload")
uploaded_file = st.file_uploader(
    "Choose a CSV file", 
    type="csv",
    help="Upload a CSV file with weekly user activity data"
)

# =============================================================================
# MAIN DASHBOARD (Only if file is uploaded)
# =============================================================================
if uploaded_file is not None:
    try:
        # ---------------------------------------------------------------------
        # Data Loading and Validation
        # ---------------------------------------------------------------------
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
        
        # ---------------------------------------------------------------------
        # Data Preview
        # ---------------------------------------------------------------------
        st.markdown("---")
        st.header("📋 Data Preview")
        st.write(f"Loaded {len(df)} weekly records")
        preview_cols = ['fullName', 'country', 'division', 'week_period', 'logins']
        if 'salesRepEmail' in df.columns:
            preview_cols.insert(-1, 'salesRepEmail')
        st.dataframe(df[preview_cols].head(10), use_container_width=True)
        
        # ---------------------------------------------------------------------
        # Data Aggregation
        # ---------------------------------------------------------------------
        # Aggregate user data across all weeks
        agg_dict = {
            'logins': 'sum',
            'week_period': 'count'
        }
        
        # Add createEvents if it exists in the dataframe
        if 'createEvents' in df.columns:
            agg_dict['createEvents'] = 'sum'
        
        user_totals = df.groupby(['fullName', 'country', 'division']).agg(agg_dict).reset_index()
        
        # Rename columns based on what's available
        new_columns = ['fullName', 'country', 'division', 'total_logins', 'weeks_active']
        if 'createEvents' in df.columns:
            new_columns.append('total_createEvents')
        user_totals.columns = new_columns
        
        # Filter out users with zero logins
        active_users = user_totals[user_totals['total_logins'] > 0].copy()
        active_users = active_users.sort_values(['country', 'total_logins'], ascending=[True, False])

        # Filter users with createEvents if column exists
        if 'createEvents' in df.columns:
            active_users_events = user_totals[user_totals['total_createEvents'] > 0].copy()
            active_users_events = active_users_events.sort_values(['country', 'total_createEvents'], ascending=[True, False])

        # =============================================================================
        # OVERVIEW SECTION
        # =============================================================================
        st.markdown("---")
        st.header("📊 Overview")

        date_range = f"{df['fromDate'].min().strftime('%Y-%m-%d')} to {df['toDate'].max().strftime('%Y-%m-%d')}"
        st.metric("Date Range", date_range)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Users", len(user_totals))
        with col2:
            st.metric("Active Users", len(active_users))
        with col3:
            st.metric("Countries", df['country'].nunique())

        st.subheader("📈 Weekly Activity Trends")
        weekly_agg_dict = {
            'logins': 'sum',
            'fullName': 'nunique'
        }
        if 'createEvents' in df.columns:
            weekly_agg_dict['createEvents'] = 'sum'
        
        weekly_summary = df.groupby(['fromDate', 'week_period']).agg(weekly_agg_dict).reset_index()
        
        # Rename columns based on what's available
        weekly_columns = ['fromDate', 'week_period', 'total_logins', 'active_users']
        if 'createEvents' in df.columns:
            weekly_columns.append('total_createEvents')
        weekly_summary.columns = weekly_columns
        
        # Create weekly trend chart with consistent styling
        fig_weekly, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Total logins per week
        ax1.plot(weekly_summary['fromDate'], weekly_summary['total_logins'], 
                marker='o', linewidth=2.5, markersize=6, color=COLOR_PRIMARY)
        ax1.set_title('Total Logins per Week', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Total Logins', fontsize=10)
        ax1.grid(True, alpha=0.3, linestyle='--')
        ax1.tick_params(axis='x', rotation=45)
        ax1.set_facecolor(COLOR_BACKGROUND)
        
        # Active users per week
        ax2.plot(weekly_summary['fromDate'], weekly_summary['active_users'], 
                marker='s', linewidth=2.5, markersize=6, color=COLOR_SUCCESS)
        ax2.set_title('Active Users per Week', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Number of Active Users', fontsize=10)
        ax2.set_xlabel('Week', fontsize=10)
        ax2.grid(True, alpha=0.3, linestyle='--')
        ax2.tick_params(axis='x', rotation=45)
        ax2.set_facecolor(COLOR_BACKGROUND)
        
        plt.tight_layout()
        st.pyplot(fig_weekly)

        # Weekly summary table
        st.subheader("📅 Weekly Summary")
        display_columns = ['week_period', 'total_logins', 'active_users']
        if 'total_createEvents' in weekly_summary.columns:
            display_columns.append('total_createEvents')
        
        weekly_display = weekly_summary[display_columns].copy()
        # Rename columns for better display
        column_rename = {
            'week_period': 'Week Period',
            'total_logins': 'Total Logins',
            'active_users': 'Active Users'
        }
        if 'total_createEvents' in weekly_summary.columns:
            column_rename['total_createEvents'] = 'Total Events Created'
        
        weekly_display.columns = [column_rename.get(col, col) for col in weekly_display.columns]
        st.dataframe(weekly_display, use_container_width=True, hide_index=True)

        # Monthly Active Users section
        st.subheader("📊 Monthly Active Users")
        
        # Total user counts per country (hardcoded as specified)
        total_users_by_country = {
            'Singapore': 32,
            'Malaysia': 35,
            'Vietnam': 27
        }
        
        # Calculate MAU (users with total_logins > 0) per country
        mau_by_country = active_users['country'].value_counts().to_dict()
        
        # Create pie charts for each country
        countries_in_data = [country for country in total_users_by_country.keys() if country in mau_by_country]
        
        if countries_in_data:
            # Create a single figure with subplots for consistent sizing
            fig_mau, axes = plt.subplots(1, len(countries_in_data), figsize=(15, 5))
            if len(countries_in_data) == 1:
                axes = [axes]  # Make it iterable for single country
            
            for i, country in enumerate(countries_in_data):
                total_users = total_users_by_country[country]
                active_users_count = mau_by_country.get(country, 0)
                inactive_users_count = total_users - active_users_count
                
                # Create pie chart data with consistent colors
                sizes = [active_users_count, inactive_users_count]
                labels = ['Active Users', 'Inactive Users']
                colors = [COLOR_SUCCESS, COLOR_DANGER]  # Green for active, red for inactive
                
                # Create pie chart
                wedges, texts, autotexts = axes[i].pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', 
                                                     startangle=90, textprops={'fontsize': 10})
                axes[i].set_title(f'{country}\nMAU: {active_users_count}/{total_users}', fontsize=12, fontweight='bold')
                axes[i].axis('equal')  # Ensure circular pie chart
                
                # Make percentage text bold
                for autotext in autotexts:
                    autotext.set_fontweight('bold')
                    autotext.set_color('white')
            
            plt.tight_layout()
            st.pyplot(fig_mau)
            
            # Display MAU rate metrics below the charts
            cols = st.columns(len(countries_in_data))
            for i, country in enumerate(countries_in_data):
                total_users = total_users_by_country[country]
                active_users_count = mau_by_country.get(country, 0)
                with cols[i]:
                    st.metric(f"{country} MAU Rate", f"{(active_users_count/total_users*100):.1f}%")
        else:
            st.info("No data available for the specified countries (Singapore, Malaysia, Vietnam)")

        # Summary table by country
        st.subheader("📋 Summary by Country")
        
        # Build aggregation dictionary
        country_agg_dict = {
            'total_logins': ['count', 'sum', 'mean', 'max'],
            'weeks_active': 'mean'
        }
        
        # Add createEvents metrics if available
        if 'total_createEvents' in user_totals.columns:
            country_agg_dict['total_createEvents'] = ['sum', 'mean', 'max']
        
        country_summary = user_totals.groupby('country').agg(country_agg_dict).round(2)
        
        # Build column names
        column_names = ['Total Number of Users', 'Total Logins', 'Avg Logins per User', 'Max Weekly Logins', 'Avg Weekly Active']
        if 'total_createEvents' in user_totals.columns:
            column_names.extend(['Total Events Created', 'Avg Events per User', 'Max Weekly Events'])
        
        country_summary.columns = column_names
        st.dataframe(country_summary, use_container_width=True)

        # =============================================================================
        # LOGIN ANALYSIS SECTION
        # =============================================================================
        st.markdown("---")
        st.header("🔑 Login Analysis")

        # User input for top N users per country
        st.subheader("🎯 Filter Options")
        top_n = st.slider("Select top N users per country", min_value=3, max_value=10, value=5)

        # Get top N users per country (by total logins)
        top_users_by_country = active_users.groupby('country').head(top_n).reset_index(drop=True)

        # Display country-wise breakdown
        st.subheader("🌍 Country Breakdown - Top Users")
        for country in df['country'].unique():
            country_data = active_users[active_users['country'] == country].head(top_n)
            if not country_data.empty:
                st.write(f"**{country}** - Top {min(top_n, len(country_data))} Users:")
                display_df = country_data[['fullName', 'division', 'total_logins', 'weeks_active']].copy()
                display_df.columns = ['Full Name', 'Division', 'Total Logins', 'Weeks Active']
                st.dataframe(display_df, use_container_width=True, hide_index=True)

        # Matplotlib bar chart for top users by logins
        st.subheader("📊 Top Users by Logins")
        fig_top_users, ax = plt.subplots(figsize=(12, 6))

        top_users_overall = active_users.sort_values('total_logins', ascending=False).head(top_n * 3)
        user_labels = [f"{name}\n({country})" for name, country in 
                       zip(top_users_overall['fullName'], top_users_overall['country'])]

        # Use consistent color scheme
        bars2 = ax.bar(range(len(top_users_overall)), top_users_overall['total_logins'], 
                        color=COLORS_SEQUENTIAL_BLUE(np.linspace(0.4, 0.9, len(top_users_overall))),
                        edgecolor='white', linewidth=0.5)
        ax.set_xlabel('Users', fontsize=10)
        ax.set_ylabel('Total Login Count', fontsize=10)
        ax.set_title(f'Top {len(top_users_overall)} Users Overall', fontsize=12, fontweight='bold')
        ax.set_xticks(range(len(top_users_overall)))
        ax.set_xticklabels(user_labels, rotation=45, ha='right', fontsize=8)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_facecolor(COLOR_BACKGROUND)

        # Add value labels on bars
        for i, value in enumerate(top_users_overall['total_logins']):
            ax.text(i, value + 0.1, str(value), ha='center', va='bottom', fontweight='bold')

        plt.tight_layout()
        st.pyplot(fig_top_users)

        # Create matplotlib bar chart for top countries by logins
        st.subheader("🌍 Top Countries by Total Logins")
        fig_top_countries, ax = plt.subplots(figsize=(15, 6))

        country_totals = active_users.groupby('country')['total_logins'].sum().sort_values(ascending=True)
        colors = [COLORS_QUALITATIVE[i % len(COLORS_QUALITATIVE)] for i in range(len(country_totals))]

        bars1 = ax.barh(country_totals.index, country_totals.values, color=colors, 
                       edgecolor='white', linewidth=1)
        ax.set_xlabel('Total Login Count (All Weeks)', fontsize=10)
        ax.set_title('Total Logins by Country', fontsize=12, fontweight='bold')
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        ax.set_facecolor(COLOR_BACKGROUND)

        # Add value labels on bars
        for i, (country, value) in enumerate(country_totals.items()):
            ax.text(value + 0.5, i, str(value), va='center', fontweight='bold')

        plt.tight_layout()
        st.pyplot(fig_top_countries)

        # Key insights - login
        st.subheader("💡 Key Insights")
        most_active_country = active_users.groupby('country')['total_logins'].sum().idxmax()
        most_active_user = active_users.loc[active_users['total_logins'].idxmax()]
        most_active_week = weekly_summary.loc[weekly_summary['total_logins'].idxmax()]

        st.write(f"• **Average Logins per Active User**: {active_users['total_logins'].mean():.1f}")
        st.write(f"• **Most Active User**: {most_active_user['fullName']} from {most_active_user['country']} with {most_active_user['total_logins']} total logins across {most_active_user['weeks_active']} weeks")
        st.write(f"• **Average Weeks Active per User**: {user_totals['weeks_active'].mean():.1f}")
        st.write(f"• **Most Active Week**: {most_active_week['week_period']} with {most_active_week['total_logins']} total logins")
        st.write(f"• **Most Active Country**: {most_active_country} with {active_users[active_users['country'] == most_active_country]['total_logins'].sum()} total logins")

        # =============================================================================
        # CREATE EVENTS ANALYSIS SECTION
        # =============================================================================
        if 'createEvents' in df.columns and 'total_createEvents' in user_totals.columns:
            st.markdown("---")
            st.header("📝 Create Events Analysis")
            
            # Display basic statistics for createEvents
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Events Created", int(df['createEvents'].sum()))
            with col2:
                st.metric("Users with Events", len(active_users_events))
            with col3:
                avg_events = active_users_events['total_createEvents'].mean() if len(active_users_events) > 0 else 0
                st.metric("Avg Events per Active User", f"{avg_events:.1f}")
            
            if len(active_users_events) > 0:
                # Country-wise breakdown for createEvents
                st.subheader("🌍 Country Breakdown - Top Users (Total Create Events)")
                for country in df['country'].unique():
                    country_data = active_users_events[active_users_events['country'] == country].head(top_n)
                    if not country_data.empty:
                        st.write(f"**{country}** - Top {min(top_n, len(country_data))} Users:")
                        display_df = country_data[['fullName', 'division', 'total_createEvents', 'weeks_active']].copy()
                        display_df.columns = ['Full Name', 'Division', 'Total Create Events', 'Weeks Active']
                        st.dataframe(display_df, use_container_width=True, hide_index=True)
                
                # Matplotlib bar chart for top users by createEvents
                st.subheader("📊 Top Users by Create Events")
                fig_top_users_events, ax = plt.subplots(figsize=(12, 6))
                
                top_users_events_overall = active_users_events.sort_values('total_createEvents', ascending=False).head(top_n * 3)
                user_labels_events = [f"{name}\n({country})" for name, country in 
                                      zip(top_users_events_overall['fullName'], top_users_events_overall['country'])]
                
                # Use consistent color scheme (orange for events)
                bars_events = ax.bar(range(len(top_users_events_overall)), top_users_events_overall['total_createEvents'], 
                                     color=COLORS_SEQUENTIAL_ORANGE(np.linspace(0.4, 0.9, len(top_users_events_overall))),
                                     edgecolor='white', linewidth=0.5)
                ax.set_xlabel('Users', fontsize=10)
                ax.set_ylabel('Total Create Events Count', fontsize=10)
                ax.set_title(f'Top {len(top_users_events_overall)} Users Overall by Create Events', fontsize=12, fontweight='bold')
                ax.set_xticks(range(len(top_users_events_overall)))
                ax.set_xticklabels(user_labels_events, rotation=45, ha='right', fontsize=8)
                ax.grid(axis='y', alpha=0.3, linestyle='--')
                ax.set_facecolor(COLOR_BACKGROUND)
                
                # Add value labels on bars
                for i, value in enumerate(top_users_events_overall['total_createEvents']):
                    ax.text(i, value + 0.1, str(int(value)), ha='center', va='bottom', fontweight='bold')
                
                plt.tight_layout()
                st.pyplot(fig_top_users_events)
                
                # Create matplotlib bar chart for top countries by createEvents
                st.subheader("🌍 Top Countries by Total Create Events")
                fig_top_countries_events, ax = plt.subplots(figsize=(15, 6))
                
                country_totals_events = active_users_events.groupby('country')['total_createEvents'].sum().sort_values(ascending=True)
                colors_events = [COLORS_QUALITATIVE[i % len(COLORS_QUALITATIVE)] for i in range(len(country_totals_events))]
                
                bars_events_country = ax.barh(country_totals_events.index, country_totals_events.values, 
                                             color=colors_events, edgecolor='white', linewidth=1)
                ax.set_xlabel('Total Create Events Count (All Weeks)', fontsize=10)
                ax.set_title('Total Create Events by Country', fontsize=12, fontweight='bold')
                ax.grid(axis='x', alpha=0.3, linestyle='--')
                ax.set_facecolor(COLOR_BACKGROUND)
                
                # Add value labels on bars
                for i, (country, value) in enumerate(country_totals_events.items()):
                    ax.text(value + 0.5, i, str(int(value)), va='center', fontweight='bold')
                
                plt.tight_layout()
                st.pyplot(fig_top_countries_events)
                
                # Weekly createEvents trends
                st.subheader("📈 Weekly Create Events Trends")
                weekly_events_summary = df.groupby(['fromDate', 'week_period']).agg({
                    'createEvents': 'sum',
                    'fullName': 'nunique'
                }).reset_index()
                weekly_events_summary.columns = ['fromDate', 'week_period', 'total_createEvents', 'active_users']
                
                # Filter weeks with at least some events
                weekly_events_summary = weekly_events_summary[weekly_events_summary['total_createEvents'] > 0]
                
                if len(weekly_events_summary) > 0:
                    fig_weekly_events, ax = plt.subplots(figsize=(12, 5))
                    
                    # Total createEvents per week with consistent styling
                    ax.plot(weekly_events_summary['fromDate'], weekly_events_summary['total_createEvents'], 
                            marker='o', linewidth=2.5, markersize=6, color=COLOR_SECONDARY)
                    ax.set_title('Total Create Events per Week', fontsize=12, fontweight='bold')
                    ax.set_ylabel('Total Create Events', fontsize=10)
                    ax.set_xlabel('Week', fontsize=10)
                    ax.grid(True, alpha=0.3, linestyle='--')
                    ax.tick_params(axis='x', rotation=45)
                    ax.set_facecolor(COLOR_BACKGROUND)
                    
                    plt.tight_layout()
                    st.pyplot(fig_weekly_events)
                
                # Add key insights for createEvents
                st.subheader("💡 Key Insights")
                most_active_country_events = active_users_events.groupby('country')['total_createEvents'].sum().idxmax()
                most_active_user_events = active_users_events.loc[active_users_events['total_createEvents'].idxmax()]
                
                st.write(f"• **Users Creating Events**: {len(active_users_events)} out of {len(user_totals)} users ({len(active_users_events)/len(user_totals)*100:.1f}%)")
                st.write(f"• **Average Events per Active User**: {active_users_events['total_createEvents'].mean():.1f}")
                st.write(f"• **Most Active User**: {most_active_user_events['fullName']} from {most_active_user_events['country']} with {int(most_active_user_events['total_createEvents'])} total events")
                st.write(f"• **Most Active Country**: {most_active_country_events} with {int(active_users_events[active_users_events['country'] == most_active_country_events]['total_createEvents'].sum())} total events created")
            else:
                st.info("No users have created events in this period.")

        # =============================================================================
        # ACTIVITY BREAKDOWN SECTION
        # =============================================================================
        st.markdown("---")
        st.header("🔍 Activity Breakdown Analysis")
        
        # Calculate total activity across all view types
        view_columns = [col for col in df.columns if 'view' in col.lower() or 'create' in col.lower()]
        activity_totals = {}
        for col in view_columns:
            if df[col].dtype in ['int64', 'float64']:
                total = df[col].sum()
                if total > 0:
                    activity_totals[col.replace('Counts', '').replace('view', '').replace('create', '')] = total
        
        if activity_totals:
            # Sort activities by total count in descending order
            sorted_activities = sorted(activity_totals.items(), key=lambda x: x[1], reverse=True)
            
            # Create activity breakdown chart with consistent styling
            st.subheader("📊 Overall Activity Distribution")
            fig_activity, ax = plt.subplots(figsize=(12, 6))
            activities = [item[0] for item in sorted_activities]
            values = [item[1] for item in sorted_activities]
            
            # Use consistent color palette
            colors = [COLORS_QUALITATIVE[i % len(COLORS_QUALITATIVE)] for i in range(len(activities))]
            bars = ax.bar(activities, values, color=colors, edgecolor='white', linewidth=0.5)
            ax.set_title('Total Activity Breakdown (All Weeks)', fontsize=12, fontweight='bold')
            ax.set_ylabel('Total Count', fontsize=10)
            ax.set_xlabel('Activity Type', fontsize=10)
            plt.xticks(rotation=45, ha='right')
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            ax.set_facecolor(COLOR_BACKGROUND)
            
            # Add value labels
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                        f'{int(value)}', ha='center', va='bottom')
            
            plt.tight_layout()
            st.pyplot(fig_activity)

            # Create stacked bar chart by country for top activities
            st.subheader("📊 Activity Breakdown by Country (Stacked)")
            
            # Get top N activities (e.g., top 10 to avoid overcrowding)
            top_n_activities = min(10, len(sorted_activities))
            top_activities = [item[0] for item in sorted_activities[:top_n_activities]]
            
            # Map clean names back to original column names
            original_col_mapping = {}
            for col in view_columns:
                clean_name = col.replace('Counts', '').replace('view', '').replace('create', '')
                if clean_name in top_activities:
                    original_col_mapping[clean_name] = col
            
            # Aggregate by country for each activity
            country_activity_data = {}
            countries = df['country'].unique()
            
            for activity in top_activities:
                if activity in original_col_mapping:
                    col_name = original_col_mapping[activity]
                    country_totals = df.groupby('country')[col_name].sum()
                    country_activity_data[activity] = country_totals
            
            # Create DataFrame for plotting
            activity_by_country_df = pd.DataFrame(country_activity_data)
            
            # Create stacked horizontal bar chart with consistent styling
            fig_country_activity, ax = plt.subplots(figsize=(14, max(8, len(countries) * 0.5)))
            
            # Plot stacked bars
            activity_by_country_df.plot(
                kind='barh',
                stacked=True,
                ax=ax,
                colormap='tab20',
                width=0.7,
                edgecolor='white',
                linewidth=0.5
            )
            
            ax.set_xlabel('Total Activity Count', fontsize=10)
            ax.set_ylabel('Country', fontsize=10)
            ax.set_title(f'Top {top_n_activities} Activities by Country (Stacked)', fontsize=12, fontweight='bold')
            ax.legend(title='Activity Type', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
            ax.grid(axis='x', alpha=0.3, linestyle='--')
            ax.set_facecolor(COLOR_BACKGROUND)
            
            plt.tight_layout()
            st.pyplot(fig_country_activity)
            
            # Also create a grouped bar chart for comparison
            st.subheader("📊 Activity Comparison by Country (Grouped)")
            
            # Select top 5 activities for better readability in grouped chart
            top_5_activities = [item[0] for item in sorted_activities[:5]]
            top_5_data = {}
            
            for activity in top_5_activities:
                if activity in original_col_mapping:
                    col_name = original_col_mapping[activity]
                    country_totals = df.groupby('country')[col_name].sum()
                    top_5_data[activity] = country_totals
            
            top_5_df = pd.DataFrame(top_5_data)
            
            # Create grouped bar chart with consistent styling
            fig_grouped, ax = plt.subplots(figsize=(14, max(6, len(countries) * 0.4)))
            
            top_5_df.plot(
                kind='barh',
                ax=ax,
                color=[COLORS_QUALITATIVE[i % len(COLORS_QUALITATIVE)] for i in range(len(top_5_activities))],
                width=0.7,
                edgecolor='white',
                linewidth=0.5
            )
            
            ax.set_xlabel('Total Activity Count', fontsize=10)
            ax.set_ylabel('Country', fontsize=10)
            ax.set_title('Top 5 Activities by Country (Grouped Comparison)', fontsize=12, fontweight='bold')
            ax.legend(title='Activity Type', bbox_to_anchor=(1.05, 1), loc='upper left')
            ax.grid(axis='x', alpha=0.3, linestyle='--')
            ax.set_facecolor(COLOR_BACKGROUND)
            
            plt.tight_layout()
            st.pyplot(fig_grouped)
            
            # Create a summary table
            st.subheader("📋 Activity Summary by Country")
            
            # Calculate total activities per country across all activity types
            summary_data = []
            for country in countries:
                country_df = df[df['country'] == country]
                country_row = {'Country': country}
                
                for activity in top_activities:
                    if activity in original_col_mapping:
                        col_name = original_col_mapping[activity]
                        country_row[activity] = int(country_df[col_name].sum())
                
                country_row['Total Activities'] = sum([v for k, v in country_row.items() if k != 'Country'])
                summary_data.append(country_row)
            
            summary_df = pd.DataFrame(summary_data)
            summary_df = summary_df.sort_values('Total Activities', ascending=False)
            
            st.dataframe(summary_df, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Error reading the CSV file: {str(e)}")
        st.info("Please make sure your CSV file is properly formatted and contains the required columns.")

# =============================================================================
# NO FILE UPLOADED - SHOW INSTRUCTIONS
# =============================================================================
else:
    st.info("👆 Please upload a CSV file to get started!")
    
    st.markdown("---")
    st.header("📝 File Format Requirements")
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
