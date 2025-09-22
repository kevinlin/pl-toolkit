# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the PL Toolkit - a comprehensive Streamlit web application and Python toolkit for People Leads to perform their duties efficiently. The main components are:

- **Streamlit Web Application**: Interactive dashboards for timesheet analysis and visualization
- **Command Line Tools**: Python scripts for processing timesheets, PDFs, and CSV conversion
- **Core Modules**: `timesheet_review.py` handles Vertec timesheet parsing and analysis

## Common Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e .[dev]
```

### Running the Application
```bash
# Start the Streamlit web application
streamlit run homepage.py

# Command line tools (after installation)
timesheet-review input/filename.xlsx
pdf-parser
csv-converter
```

### Code Quality and Testing
```bash
# Code formatting
black .

# Import sorting
isort .

# Type checking
mypy .

# Linting
flake8 .

# Testing with coverage
pytest

# Run all pre-commit checks
pre-commit run --all-files
```

## Architecture

### Streamlit Application Structure
- **`homepage.py`**: Main entry point for the Streamlit app, handles file uploads and displays timesheet analysis with color-coded styling
- **`pages/01_time_distribution.py`**: Time distribution visualizations with pie charts
- **`pages/09_user_activity_dashboard.py`**: User activity analysis and dashboard

### Core Processing Logic
- **`timesheet_review.py`**: Contains the core timesheet processing functions:
  - `extract_user_row_mappings()`: Extracts team members and row indices from Excel sheets
  - `extract_date_col_mappings()`: Maps date columns in the timesheet
  - `read_timesheet_entries_by_users()`: Processes timesheet data by user
- **`pdf_parser.py`**: PDF document text extraction utilities
- **`csv_converter.py`**: CSV data conversion and processing tools

### Data Flow
1. Excel files (`.xlsx`) are uploaded via Streamlit or processed via CLI
2. Data is parsed from "Sheet2" of the Excel file using pandas and openpyxl
3. User mappings and date columns are extracted from the timesheet structure
4. Data is processed and can be exported to CSV files in the `output/` directory
5. Results are visualized in the Streamlit dashboard with color-coded styling

### Directory Structure
- `input/`: Excel timesheet files and other input data
- `output/`: Generated CSV files and analysis results
- `pages/`: Streamlit page components
- `tests/`: Test files using pytest
- `.streamlit/`: Streamlit configuration with auto-reload enabled

## Key Dependencies
- **streamlit**: Web application framework
- **pandas**: Data processing and analysis
- **openpyxl**: Excel file reading/writing
- **matplotlib**: Data visualization
- **PyPDF2**: PDF processing

## Code Style
- Uses Black formatting with 88-character line length
- Type hints are configured via mypy with strict settings
- Import sorting handled by isort with Black profile
- All configurations centralized in `pyproject.toml`

## Testing
- Tests located in `tests/` directory
- Uses pytest with coverage reporting
- Run individual tests: `pytest tests/test_specific_file.py`
- Coverage reports generated in HTML, XML, and terminal formats