# Enterprise360 – Business Intelligence & Risk Monitoring

Enterprise360 is a Business Intelligence and Risk Monitoring platform developed using Python, Streamlit, SQL, Power BI and Google Gemini AI.

The project demonstrates how business transaction, vendor, project and risk data can be collected, analyzed, validated and transformed into meaningful insights to support enterprise operations, performance monitoring and risk management.

**Project Data Note:** This project uses synthetic demonstration data. All figures, transactions, vendors, risks and project metrics displayed in the application are illustrative and do not represent actual company performance.

---

## Project Highlights

- **Executive Overview:** Displays key business performance indicators, transaction volume, transaction value, high-risk records and data quality metrics.
- **Risk & Controls:** Monitors risk records, severity levels, risk categories and outstanding risk reviews.
- **Data Quality Management:** Identifies missing vendor information, missing descriptions and duplicate transaction records.
- **Vendor Performance:** Analyzes vendor spending, transaction activity, completed transactions and pending transactions.
- **Operations Management:** Tracks project progress, completion percentages and delayed projects.
- **AI Business Insights:** Combines Python-based analytical rules with Google Gemini AI to generate business summaries, observations and management recommendations.
- **Power BI Reporting:** Provides CSV exports and an interactive executive reporting dashboard.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development and business logic |
| Streamlit | Interactive dashboard development |
| SQLite | Database management |
| SQL | Data querying and analysis |
| Pandas | Data processing and transformation |
| Plotly | Interactive charts and visualizations |
| Power BI Desktop | Executive reporting and analytics |
| Google Gemini API | AI-powered business insights |
| Google Gen AI SDK | Generative AI integration |
| Git & GitHub | Version control and project hosting |

---

## Dashboard Modules

### 1. Executive Overview

- Total transactions processed
- Total transaction value
- High-risk records
- Data quality score
- Monthly transaction trends
- Enterprise risk distribution
- Recent transaction records

### 2. Risk & Controls

- Total risk records
- High-risk records
- Open risk records
- Risk severity distribution
- Risk register and status monitoring

### 3. Data Quality Management

- Total transactions checked
- Missing vendor information
- Missing transaction descriptions
- Duplicate transaction detection
- Data validation report

### 4. Vendor Performance

- Total vendors
- Total vendor spending
- Completed and pending transactions
- Vendor spending comparison
- Vendor transaction activity
- Vendor register

### 5. Operations Management

- Total projects
- Average project completion
- Delayed projects
- Project progress analytics
- Project register and delivery status

### 6. AI Business Insights

- Python-based analytical observations
- Gemini-powered executive summaries
- Key business performance observations
- Priority management recommendations
- Data limitations and evidence-based recommendations

---

## AI Integration

Enterprise360 integrates the Google Gemini API to generate business insights from aggregate demonstration metrics.

The AI integration supports:

- Executive summaries
- Key business observations
- Priority management recommendations
- Identification of business performance patterns
- Data limitations and recommendations

The application is designed to send aggregate metrics rather than confidential row-level business records.

**Note:** AI-generated results depend on API availability, model capacity and applicable usage limits. Python-based analytical rules are also included in the application.

---

## Database and Data Reporting

The project uses a local SQLite database to store and retrieve demonstration data.

Python and SQL are used for database operations, data processing and analytical queries.

CSV exports are generated for Power BI reporting.

The exported datasets include:

- `departments.csv`
- `vendors.csv`
- `transactions.csv`
- `projects.csv`
- `risk_records.csv`
- `transaction_analysis.csv`

---

## Power BI Executive Dashboard

The Power BI report demonstrates business intelligence and executive reporting through:

- KPI cards
- Monthly transaction trends
- Department spending analysis
- Risk severity distribution
- Transaction status analysis
- Date slicer
- Vendor-category slicer

The dashboard uses CSV datasets exported from the Enterprise360 database.

---

## Project Structure

```text
Enterprise360/
│
├── app.py
├── ai_insights.py
├── .gitignore
│
├── .streamlit/
│   └── config.toml
│
├── database/
│   ├── schema.sql
│   ├── db.py
│   ├── check_db.py
│   ├── seed.py
│   ├── queries.py
│   ├── export_data.py
│   ├── enterprise360.db
│   └── Enterprise360_Executive_Dashboard.pbix
│
├── reports/
│   └── powerbi/
│       ├── departments.csv
│       ├── vendors.csv
│       ├── transactions.csv
│       ├── projects.csv
│       ├── risk_records.csv
│       └── transaction_analysis.csv
│
├── README.md
└── requirements.txt
```

**Note:** `.streamlit/secrets.toml` is a local configuration file containing the Gemini API key. It is intentionally excluded from the public GitHub repository.

---

## Installation and Setup

### Prerequisites

- Python 3.10 or later
- Visual Studio Code
- Git
- Power BI Desktop (for the reporting component)

### 1. Clone the Repository

```bash
git clone https://github.com/amruthapottabathini-stack/Enterprise360.git
cd Enterprise360
```

### 2. Create a Virtual Environment

For Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Gemini API

Create a Streamlit secrets file at:

```text
.streamlit/secrets.toml
```

Add your Gemini API key:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

Replace the placeholder with your own API key.

**Security:** Never upload your API key, passwords or private credentials to GitHub.

### 5. Run the Application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal to access the dashboard.

---

## Security Considerations

- API credentials are stored using Streamlit secrets.
- API keys are excluded from the public GitHub repository through `.gitignore`.
- The AI integration is designed around aggregate metrics.
- Synthetic demonstration data is used in the portfolio version.
- Real business data should only be used with appropriate authorization and safeguards.

---

## Current Scope and Future Enhancements

### Implemented Features

- Six interactive Streamlit dashboard modules.
- SQLite database integration.
- Transaction and vendor analytics.
- Risk monitoring and data validation.
- Project progress tracking.
- Python-based business insights.
- Google Gemini API integration.
- CSV exports for Power BI.
- Power BI executive dashboard.
- GitHub version control and project documentation.

### Future Enhancements

- Role-based access control.
- Automated data refresh.
- Advanced data validation and exception reporting.
- Audit logging and control tracking.
- Natural-language business data queries.
- Cloud deployment.
- More advanced predictive risk analytics.

---

## Author

**Pottabathini Amrutha**

Electronics and Communication Engineering Graduate

Interested in Business Intelligence, Data Analytics, Risk Management, Compliance, Governance and Enterprise Operations.

---

## Disclaimer

Enterprise360 is an educational portfolio project developed for learning and demonstration purposes. It is not affiliated with or endorsed by any real organization.

All sample data, business figures and analytical outputs are illustrative and should not be interpreted as actual company performance or professional business advice.