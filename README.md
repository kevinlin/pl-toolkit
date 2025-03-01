# Tools for People Leads

## Purpose
A collection of tools for People Leads to perform their duties. This includes a Streamlit application for interactive dashboards and a Python script for generating processed timesheet data.

---

## Streamlit App

To start the app:
```bash
streamlit run `homepage.py`
```

### Structure
- **`homepage.py`**: Main entry point for the Streamlit interface. Displays a styled table of differences between target and actual timesheet hours.
- **`pages/01_time_distribution.py`**: Generates pie charts to visualize user-specific time distribution by categories.  

---

## Execute the Python Script Locally

Use:
```bash
python `timesheet_review.py` `input/202502_ZE\ TimeSheet_OpHours.xlsx`
```

### Input/Output Folders
- **Input folder**: Stores raw Excel files (e.g., `202502_ZE\ TimeSheet_OpHours.xlsx`) before processing.
- **Output folder**: After running the script, CSV files (`timesheet_entries.csv`, `time_distribution.csv`) are generated here for further analysis or uploading into the Streamlit application.

---
```