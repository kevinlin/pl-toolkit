# PL Toolkit - Tools for People Leads

A comprehensive collection of tools for People Leads to perform their duties efficiently. This toolkit includes a Streamlit web application for interactive dashboards and Python scripts for processing timesheet data, PDF parsing, and CSV conversion.

## 🚀 Quick Start

### Installation

#### Option 1: Development Installation (Recommended)
```bash
# Clone the repository
git clone <repository-url>
cd pl-toolkit

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e .[dev]
```

#### Option 2: Production Installation
```bash
pip install -e .
```



### Running the Streamlit Application

```bash
streamlit run homepage.py
```

Or use the web interface at `http://localhost:8501` after starting.

---

## 📋 Features

### 🌐 Streamlit Web Application
- **Interactive Dashboard**: Upload and analyze timesheet data with visual feedback
- **Time Distribution Visualization**: Generate pie charts showing user-specific time allocation
- **Real-time Processing**: Instant analysis of uploaded Excel files

### 🔧 Command Line Tools

#### Timesheet Processing
```bash
# Using the installed console script
timesheet-review input/202502_ZE\ TimeSheet_OpHours.xlsx

# Or directly with Python
python timesheet_review.py input/202502_ZE\ TimeSheet_OpHours.xlsx
```

#### PDF Document Processing
```bash
# Using the installed console script
pdf-parser

# Or directly with Python
python pdf_parser.py
```

#### CSV Data Conversion
```bash
# Using the installed console script
csv-converter

# Or directly with Python
python csv_converter.py
```

---

## 📁 Project Structure

```
pl-toolkit/
├── homepage.py              # Main Streamlit application entry point
├── timesheet_review.py      # Core timesheet processing logic
├── pdf_parser.py           # PDF document parsing utilities
├── csv_converter.py        # CSV data conversion tools
├── pages/                 # Streamlit pages
│   └── 01_time_distribution.py  # Time distribution visualizations
├── input/                 # Input data directory (Excel files, PDFs)
├── output/               # Generated output files (CSV, reports)
├── pyproject.toml        # Modern Python project configuration
├── requirements.txt      # Legacy dependency list
└── README.md            # This file
```

---

## 🔄 Workflow

### 1. Data Processing Workflow
1. **Upload Excel File**: Place timesheet Excel files in the `input/` directory
2. **Run Processing**: Execute `timesheet-review <filename>` to analyze the data
3. **Review Output**: Check generated CSV files in the `output/` directory
4. **Visualize**: Upload the generated CSVs to the Streamlit app for interactive analysis

### 2. Web Application Workflow
1. **Start Application**: Run `streamlit run homepage.py`
2. **Upload Data**: Use the file uploader to select your timesheet Excel file
3. **View Analysis**: Instantly see styled tables showing hour differences
4. **Navigate Pages**: Use the sidebar to access time distribution visualizations

---

## 📊 Data Formats

### Input Files
- **Timesheet Excel Files**: `.xlsx` files with specific structure (Sheet2)
- **PDF Documents**: Any PDF file for text extraction
- **CSV Files**: Standard comma-separated value files

### Output Files
- `timesheet_entries.csv`: Processed timesheet data with user entries
- `time_distribution.csv`: Summary of time allocation by categories
- Converted text files from PDF processing

---

## 🛠️ Development

### Code Quality Tools
The project includes pre-configured development tools:

```bash
# Code formatting
black .

# Import sorting
isort .

# Type checking
mypy .

# Linting
flake8 .

# Testing
pytest

# Run all checks
pre-commit run --all-files
```

### Development Dependencies
Install development tools with:
```bash
pip install -e .[dev]
```

This includes:
- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **pre-commit**: Git hooks

---

## ⚙️ Configuration

### Streamlit Configuration
The application includes custom Streamlit configuration in `.streamlit/config.toml`:
- Auto-reload on save
- Detailed error reporting
- Usage statistics disabled

### Python Configuration
All tool configurations are centralized in `pyproject.toml`:
- Package metadata and dependencies
- Black, isort, mypy, pytest configurations
- Build system specifications

---

## 📝 Requirements

- **Python**: 3.11 or higher
- **Operating System**: Cross-platform (Windows, macOS, Linux)
- **Memory**: Sufficient for pandas DataFrame operations
- **Storage**: Space for input Excel files and output CSV files

---

## 🤝 Contributing

1. **Setup Development Environment**:
   ```bash
   git clone <repository-url>
   cd pl-toolkit
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .[dev]
   ```

2. **Install Pre-commit Hooks**:
   ```bash
   pre-commit install
   ```

3. **Run Tests**:
   ```bash
   pytest
   ```

4. **Code Style**:
   - Follow PEP 8 conventions
   - Use Black for formatting
   - Add type hints where appropriate
   - Write docstrings for functions

---

## 📄 License

This project is licensed under the MIT License - see the `pyproject.toml` file for details.

---

## 🆘 Support

For issues, questions, or contributions:
1. Check the existing documentation
2. Create an issue in the project repository
3. Review the code for implementation details

---

## 🔄 Version History

- **v0.1.0**: Initial release with Streamlit dashboard and timesheet processing capabilities