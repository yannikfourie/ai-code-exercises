# Documentation Exercise — DataInsight
**Exercise:** AI-Assisted Technical Documentation using Prompts 1, 2, and 3

---

## Table of Contents

1. [Project Information](#1-project-information)
2. [README — Prompt 1](#2-readme--prompt-1)
3. [Step-by-Step Guide — Prompt 2](#3-step-by-step-guide--prompt-2)
4. [FAQ Document — Prompt 3](#4-faq-document--prompt-3)
5. [Reflection](#5-reflection)

---

## 1. Project Information

| Field | Details |
|---|---|
| **Project name** | DataInsight |
| **Description** | A data analysis and visualization framework for scientific data |
| **Technologies** | Python, Pandas, NumPy, Matplotlib, Plotly, Jupyter |
| **Installation** | Python 3.8+, pip |

**Key features:**
- Data import from various sources (CSV, Excel, SQL, APIs)
- Data cleaning and transformation tools
- Statistical analysis functions
- Interactive visualizations
- Report generation
- Export capabilities

**Project structure:**
```
datainsight/
├── datainsight/          # Main package
│   ├── io/               # Data import/export modules
│   ├── transform/        # Data transformation tools
│   ├── analysis/         # Analysis algorithms
│   ├── viz/              # Visualization tools
│   └── report/           # Report generation
├── examples/             # Example notebooks
└── tests/                # Unit tests
```

---

## 2. README — Prompt 1

> **Prompt used:**
> *"Please create a comprehensive README.md file for my project. Project name: DataInsight. Description: A data analysis and visualization framework for scientific data. Key features: [listed above]. Technologies: Python, Pandas, NumPy, Matplotlib, Plotly, Jupyter. Installation requirements: Python 3.8+, pip. The README should include: clear project title and description, installation instructions, basic usage examples, features overview, configuration options, troubleshooting section, contributing guidelines, and license information."*

---

# DataInsight

> A powerful data analysis and visualization framework for scientific data — built for researchers, analysts, and engineers who need to go from raw data to insight fast.

---

### Features

| Feature | Description |
|---|---|
| **Data Import** | Load data from CSV, Excel, SQL databases, and REST APIs in a single line |
| **Data Cleaning** | Handle missing values, outliers, type coercion, and deduplication |
| **Statistical Analysis** | Descriptive stats, hypothesis testing, correlation, and regression |
| **Interactive Visualizations** | Plotly-powered charts with zoom, filter, and hover capabilities |
| **Report Generation** | Auto-generate HTML and PDF reports from your analysis |
| **Export** | Save results to CSV, Excel, JSON, or push directly to a database |

---

### Installation

**Prerequisites:** Python 3.8 or higher, pip

```bash
# Standard install
pip install datainsight

# With Excel support
pip install datainsight[excel]

# With SQL support
pip install datainsight[sql]

# All optional dependencies
pip install datainsight[all]
```

Verify installation:
```bash
python -c "import datainsight; print(datainsight.__version__)"
```

---

### Quick Start

```python
import datainsight as di

# Load data
df = di.load("data/experiment_results.csv")

# Clean it
df = di.clean(df, drop_duplicates=True, fill_missing="mean")

# Analyse it
stats = di.analyse(df, target_column="yield")

# Visualise it
di.plot(df, x="temperature", y="yield", kind="scatter")

# Generate a report
di.report(df, stats, output="report.html")
```

---

### Usage Examples

**Loading from different sources:**
```python
from datainsight.io import load_csv, load_excel, load_sql, load_api

df = load_csv("data/results.csv")
df = load_excel("data/results.xlsx", sheet_name="Sheet1")
df = load_sql(
    query="SELECT * FROM experiments WHERE status = 'complete'",
    connection_string="postgresql://user:pass@localhost/mydb"
)
df = load_api(
    url="https://api.example.com/data",
    headers={"Authorization": "Bearer YOUR_TOKEN"}
)
```

**Cleaning and transforming:**
```python
from datainsight.transform import clean, normalize, encode

df = clean(df, drop_duplicates=True, fill_missing="median")
df["temperature_norm"] = normalize(df["temperature"])
df = encode(df, columns=["category"], method="onehot")
```

**Statistical analysis:**
```python
from datainsight.analysis import describe, correlate, hypothesis_test

summary = describe(df)
corr = correlate(df, method="pearson")
result = hypothesis_test(
    df[df["group"] == "A"]["yield"],
    df[df["group"] == "B"]["yield"],
    test="ttest"
)
print(f"p-value: {result.pvalue:.4f}")
```

**Generating reports:**
```python
from datainsight.report import generate

generate(
    data=df,
    analysis=summary,
    title="Experiment Results Q3 2024",
    output_format="html",
    output_path="reports/q3_report.html"
)
```

---

### Configuration

```yaml
# datainsight.config.yaml
data:
  default_encoding: utf-8
  missing_value_strategy: mean

analysis:
  significance_level: 0.05
  correlation_method: pearson

visualization:
  theme: plotly_white
  default_color_palette: viridis

report:
  default_format: html
  include_raw_data: false
```

Or programmatically:
```python
di.config.set("visualization.theme", "plotly_dark")
di.config.set("analysis.significance_level", 0.01)
```

---

### Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: openpyxl` | Excel dependency missing | `pip install datainsight[excel]` |
| `SQLAlchemyError` | Wrong connection string prefix | Use `postgresql://`, `mysql+pymysql://`, or `sqlite:///` |
| Plots not showing in Jupyter | Missing Plotly extension | `pip install jupyterlab && jupyter labextension install jupyterlab-plotly` |
| PDF generation fails | Missing weasyprint | `pip install weasyprint` |
| `MemoryError` on large files | File too large for single load | Use `load_csv("file.csv", chunksize=50000)` |

---

### Contributing

1. Fork the repository on GitHub
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and add tests in `/tests`
4. Ensure all tests pass: `pytest tests/`
5. Submit a pull request with a clear description of your changes

When reporting bugs, include your Python version, DataInsight version, a minimal reproducible example, and the full traceback.

---

### License

DataInsight is released under the MIT License. See `LICENSE` for full details.

---

## 3. Step-by-Step Guide — Prompt 2

> **Prompt used:**
> *"Please create a step-by-step guide for how to import and clean data in DataInsight. The guide should: start with prerequisites, break the process into clear numbered steps, include code blocks, highlight potential issues and common mistakes, and end with a troubleshooting section. Process overview: loading a CSV, inspecting raw data, handling missing values, removing duplicates, fixing data types, normalizing column names, and saving the cleaned result. User experience level: Beginner."*

---

### Guide: Importing and Cleaning Data in DataInsight

**User level:** Beginner

#### Prerequisites

- [ ] DataInsight installed (`pip install datainsight`)
- [ ] Python 3.8 or higher
- [ ] A data file ready (CSV, Excel, or database credentials)

---

#### Step 1 — Import DataInsight and Load Your File

```python
import datainsight as di
from datainsight.io import load_csv
from datainsight.transform import clean, normalize

df = load_csv("data/experiment_results.csv")
```

> **Common mistake:** Using backslashes on Windows. Use forward slashes or a raw string:
> ```python
> df = load_csv(r"C:\Users\yourname\data\results.csv")
> ```

---

#### Step 2 — Inspect the Raw Data

Before cleaning anything, understand what you have:

```python
print(df.head())                  # First 5 rows
print(f"Shape: {df.shape}")       # Row and column count
print(df.dtypes)                  # Column data types
print(df.isnull().sum())          # Missing values per column
```

**What to look for:**
- Columns with many missing values (more than 20% is a red flag)
- Numeric columns showing `object` type (text is mixed in)
- Unexpected column names with spaces or special characters

---

#### Step 3 — Handle Missing Values

```python
df = clean(df, fill_missing="mean")     # Fill with column mean
df = clean(df, fill_missing="median")   # Fill with median (better for skewed data)
df = clean(df, fill_missing="drop")     # Drop rows with any missing value
```

> **When to use mean vs median:** Use `mean` for symmetrical distributions. Use `median` when your data has outliers, since extreme values skew the mean but not the median.

---

#### Step 4 — Remove Duplicate Rows

```python
print(f"Duplicates found: {df.duplicated().sum()}")
df = clean(df, drop_duplicates=True)
print(f"Duplicates after cleaning: {df.duplicated().sum()}")
```

> **Tip:** If duplicates should not exist at all (e.g. unique IDs), investigate why they appeared before deleting — they may signal a data collection problem upstream.

---

#### Step 5 — Fix Data Types

```python
import pandas as pd

# Convert a column to numeric (coerce converts bad values to NaN)
df["yield"] = pd.to_numeric(df["yield"], errors="coerce")

# Convert to datetime
df["collected_at"] = pd.to_datetime(df["collected_at"])

# Convert to categorical (saves memory for low-cardinality text columns)
df["status"] = df["status"].astype("category")
```

> **Common mistake:** Running `astype(float)` directly on a column with non-numeric text — this raises `ValueError`. Always use `pd.to_numeric(..., errors="coerce")` first.

---

#### Step 6 — Normalize Column Names

```python
df.columns = df.columns.str.lower().str.replace(" ", "_").str.strip()
print(df.columns.tolist())
```

**Before:** `['Sample ID', 'Temperature (C)', 'Yield %']`
**After:** `['sample_id', 'temperature_(c)', 'yield_%']`

For columns with units, rename explicitly:
```python
df.rename(columns={"temperature_(c)": "temperature_celsius"}, inplace=True)
```

---

#### Step 7 — Save the Cleaned Data

```python
print(f"Missing values remaining: {df.isnull().sum().sum()}")
df.to_csv("data/experiment_results_cleaned.csv", index=False)
print("Cleaned data saved.")
```

---

#### Complete Workflow

```python
import pandas as pd
import datainsight as di
from datainsight.io import load_csv
from datainsight.transform import clean

df = load_csv("data/experiment_results.csv")

print(f"Raw shape: {df.shape}")
print(df.isnull().sum())

df = clean(df, fill_missing="median", drop_duplicates=True)
df["yield"] = pd.to_numeric(df["yield"], errors="coerce")
df["collected_at"] = pd.to_datetime(df["collected_at"])
df.columns = df.columns.str.lower().str.replace(" ", "_").str.strip()

print(f"Clean shape: {df.shape}")
df.to_csv("data/experiment_results_cleaned.csv", index=False)
```

---

#### Troubleshooting

| Problem | Likely Cause | Solution |
|---|---|---|
| `FileNotFoundError` | Wrong file path | Run `import os; print(os.getcwd())` to check working directory |
| `ValueError: could not convert` | Text in a numeric column | Use `pd.to_numeric(col, errors="coerce")` before casting |
| `KeyError: 'column_name'` | Name changed after normalization | Print `df.columns` to see updated names |
| `MemoryError` on large file | File too big for single load | Use `load_csv("file.csv", chunksize=10000)` |

---

## 4. FAQ Document — Prompt 3

> **Prompt used:**
> *"Please help me create a comprehensive FAQ document for DataInsight. Basic information: a data analysis and visualization framework for scientific data, target audience is researchers and analysts new to DataInsight, focus on getting started, core features, and troubleshooting. Include questions about getting started, common features and functionality, troubleshooting common issues, and data import/analysis/reporting. Known common questions: installation issues, missing value strategies, Excel support errors, plot rendering in Jupyter, PDF report generation, and SQL connection strings."*

---

### Getting Started

**Q: What is DataInsight and who is it for?**
DataInsight is a Python framework that handles the full data analysis pipeline — loading, cleaning, analysing, visualizing, and reporting — in one consistent toolkit. It is designed for researchers, data analysts, and scientists who want to spend less time on boilerplate and more time understanding their data.

**Q: What Python version do I need?**
Python 3.8 or higher. Check with: `python --version`

**Q: Do I need to know Pandas to use DataInsight?**
Not to get started. DataInsight's high-level functions work independently. However, since it returns standard Pandas DataFrames, some Pandas familiarity helps for advanced operations.

**Q: Is DataInsight compatible with Jupyter Notebooks?**
Yes. All visualizations render interactively inside JupyterLab and Jupyter Notebook. Example notebooks are in the `/examples` directory.

**Q: Where can I find example projects?**
The `/examples` folder contains four notebooks: data loading, cleaning, analysis, and visualization.

---

### Data Import

**Q: What data sources are supported?**
CSV, Excel (`.xlsx`, `.xls`), SQL databases (PostgreSQL, MySQL, SQLite), and REST APIs returning JSON.

**Q: How do I load a CSV with a semicolon separator?**
```python
df = load_csv("file.csv", sep=";")
```

**Q: How do I connect to a SQL database?**
```python
df = load_sql(
    query="SELECT * FROM experiments",
    connection_string="postgresql://username:password@host/database"
)
```
Prefixes: `postgresql://`, `mysql+pymysql://`, `sqlite:///path/to/file.db`

**Q: My CSV is very large and causes a MemoryError. What do I do?**
Use chunked loading: `df = load_csv("large_file.csv", chunksize=50000)`

---

### Data Cleaning and Transformation

**Q: How do I handle missing values?**
```python
df = clean(df, fill_missing="mean")    # or "median" or "drop"
```
Use `mean` for symmetrical data, `median` when outliers are present.

**Q: How do I remove duplicate rows?**
```python
df = clean(df, drop_duplicates=True)
```
To deduplicate on a specific key column: `df = df.drop_duplicates(subset=["experiment_id"])`

**Q: How do I normalize a numeric column to 0–1 scale?**
```python
df["temperature_norm"] = normalize(df["temperature"])
```

**Q: How do I encode categorical columns?**
```python
df = encode(df, columns=["status"], method="onehot")   # no natural order
df = encode(df, columns=["status"], method="label")    # natural order (low/medium/high)
```

---

### Statistical Analysis

**Q: How do I get summary statistics?**
```python
summary = describe(df)
print(summary)
```

**Q: How do I calculate correlations?**
```python
corr = correlate(df, method="pearson")  # or "spearman", "kendall"
```
Values near 1 or -1 = strong correlation. Values near 0 = little relationship.

**Q: How do I compare two groups statistically?**
```python
result = hypothesis_test(
    df[df["group"] == "A"]["yield"],
    df[df["group"] == "B"]["yield"],
    test="ttest"    # or "mannwhitney" for non-parametric data
)
print(f"p-value: {result.pvalue:.4f}")
```

**Q: What significance level is used by default?**
0.05. Change it with: `di.config.set("analysis.significance_level", 0.01)`

---

### Visualizations

**Q: What chart types are available?**
Scatter plots, line charts, bar charts, histograms, box plots, heatmaps, correlation matrices, and interactive dashboards.

**Q: How do I change the chart theme?**
```python
di.config.set("visualization.theme", "plotly_dark")
# Options: plotly, plotly_white, plotly_dark, ggplot2, seaborn
```

**Q: How do I save a chart to a file?**
```python
fig = scatter(df, x="temperature", y="yield")
fig.write_image("chart.png")   # static PNG
fig.write_html("chart.html")   # interactive HTML
```

**Q: Plots are not showing in Jupyter. What do I do?**
```bash
pip install jupyterlab
jupyter labextension install jupyterlab-plotly
```

---

### Report Generation

**Q: How do I generate a report?**
```python
generate(data=df, analysis=summary, title="Q3 Results",
         output_format="html", output_path="reports/q3.html")
```

**Q: Can I generate PDF reports?**
Yes, after installing: `pip install weasyprint`
On Linux also run: `sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0`

**Q: Can I add a logo to reports?**
```python
di.config.set("report.logo_path", "assets/logo.png")
```

---

### Troubleshooting Common Issues

**Q: `ModuleNotFoundError: No module named 'openpyxl'`**
Run: `pip install datainsight[excel]`

**Q: `FileNotFoundError` when loading a file**
Run `import os; print(os.getcwd())` to check where Python is looking, then adjust your path.

**Q: Column names changed after cleaning — how do I find them?**
Run: `print(df.columns.tolist())`

**Q: Analysis results look wrong — the mean seems too high**
Check for outliers: `print(df["column"].sort_values(ascending=False).head(10))`

**Q: Where do I report a bug?**
Open a GitHub issue with your Python version, DataInsight version, a minimal reproducible example, and the full error traceback.

---

## 5. Reflection

**How did the AI's explanation compare to documentation found online?**
Official docs and package pages describe *what* functions exist but rarely explain *why* you would choose one option over another (e.g. mean vs median for filling missing values). The AI-generated documentation added decision-making context — when to use each strategy — which is more useful for someone learning the tool for the first time.

**What aspects would have been difficult to document manually?**
The troubleshooting sections would have been the hardest to write from scratch, since they require knowledge of all the failure modes across different operating systems and environments. The AI was able to anticipate common errors (missing optional dependencies, wrong connection string prefixes, Jupyter rendering issues) that a developer close to the code might not think to include.

**How would you modify your code to provide better error messages in the future?**
Add descriptive error messages that tell the user what to do, not just what went wrong:
```python
# Instead of letting pip raise a generic ImportError:
try:
    import openpyxl
except ImportError:
    raise ImportError(
        "Excel support requires openpyxl. Install it with: pip install datainsight[excel]"
    )
```

**Did the AI help understand not just the fix, but the underlying concepts?**
Yes. Writing the FAQ required explaining *why* things work the way they do — the difference between `mean` and `median` imputation, why `yield` from a generator uses less memory than a list, how correlation values should be interpreted. Documenting a tool forces a deeper understanding of the concepts behind it, and the AI helped surface those explanations clearly.

---