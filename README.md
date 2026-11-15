# Enterprise360 – Business Intelligence & Risk Monitoring

Enterprise360 is a portfolio project that combines a Streamlit business intelligence dashboard with a Power BI executive report. It demonstrates how transaction, vendor, project, and risk data can be organized, analyzed, and presented to support business operations, performance monitoring, and risk management.

> **Project Data Note:** The current dashboard uses synthetic demonstration data. Figures shown in the application and screenshots are illustrative and do not represent actual company performance.

## Project Highlights

- **Executive Overview:** Displays business performance KPIs, transaction volume, transaction value, high-risk records, and data quality indicators.
- **Risk & Controls:** Monitors risk records, risk severity, risk types, and outstanding risk reviews.
- **Data Quality Management:** Identifies missing vendor information, missing descriptions, and duplicate transaction records.
- **Vendor Performance:** Analyzes vendor spending, transaction activity, completed transactions, and pending transactions.
- **Operations Management:** Tracks project progress, completion percentages, and delayed projects.
- **AI Business Insights:** Combines Python-based analytical rules with Google Gemini API to generate business summaries, key observations, and management recommendations.
- **Power BI Reporting:** Provides CSV exports and an interactive executive reporting dashboard.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development and business logic |
| Streamlit | Interactive dashboard |
| SQLite | Database management |
| SQL | Data querying and analysis |
| Pandas | Data processing and transformation |
| Plotly | Interactive charts and visualizations |
| Power BI Desktop | Executive reporting and analytics |
| Google Gemini API | AI-powered business insights |
| Google Gen AI SDK | Gemini API integration |

## Dashboard Modules

### 1. Executive Overview
- Total transactions processed
- Transaction value
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
- Transactions checked
- Missing vendor information
- Missing descriptions
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
- Priority management actions
- Data limitations and evidence-based recommendations

## AI Integration

Enterprise360 integrates the Google Gemini API to generate business insights from aggregate demonstration metrics.

The AI analysis provides:
- Executive summaries
- Key business observations
- Priority management recommendations
- Data limitations

The application is designed to send aggregate metrics rather than confidential row-level business records.

**Note:** AI-generated results depend on API availability, model capacity, and applicable usage limits. The application also includes Python-based analytical rules.

## Database and Data Reporting

The project uses a local SQLite database to store and retrieve demonstration data.

CSV exports are generated for Power BI reporting.

The export files include:

- `departments.csv`
- `vendors.csv`
- `transactions.csv`
- `projects.csv`
- `risk_records.csv`
- `transaction_analysis.csv`

## Power BI Executive Dashboard

The Power BI report demonstrates business reporting through:

- KPI cards
- Monthly transaction trends
- Department spending analysis
- Risk severity distribution
- Transaction status analysis
- Date slicer
- Vendor-category slicer

The report uses CSV files exported from the Enterprise360 database.

## Project Structure

```text
Enterprise360/
│
├── app.py
├── ai_insights.py
├── secrets.toml
│
├── database/
│   ├── schema.sql
│   ├── db.py
│   ├── seed.py
│   ├── queries.py
│   ├── export_data.py
│   └── enterprise360.db
│
├── reports/
│   └── powerbi/
│       ├── departments.csv
│       ├── vendors.csv
│       ├── transactions.csv
│       ├── projects.csv
│       ├── risk_records.csv
│       ├── transaction_analysis.csv
│       └── Enterprise360_Executive_Dashboard.pbix
│
├── README.md
└── requirements.txt
```

*This is a representative project structure. Adjust it to match the files actually included in your repository.*

## Installation and Setup

### Prerequisites

- Python 3.10 or later
- Visual Studio Code
- Git
- Power BI Desktop (for the reporting component)

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Enterprise360
```

Replace the placeholder with your actual repository URL.

### 2. Create a Virtual Environment

**Windows PowerShell:**

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

Use your own API key. Never upload this file or expose your API key in a public repository.

### 5. Run the Application

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal.

## Security Considerations

- API credentials are stored using Streamlit secrets.
- API keys must not be committed to GitHub.
- The AI integration is designed around aggregate metrics.
- Synthetic demonstration data is used in the portfolio version.
- Real business data should only be used with appropriate authorization and safeguards.

## Current Scope and Future Enhancements

**Implemented:**
- Six interactive Streamlit dashboard modules.
- SQLite database integration.
- Transaction and vendor analytics.
- Risk monitoring and data validation.
- Project progress tracking.
- Python-based business insights.
- Google Gemini API integration.
- CSV exports for Power BI.
- Power BI executive dashboard.

**Future Enhancements:**
- Role-based access control.
- Automated data refresh.
- Advanced data validation and exception reporting.
- Audit logging and control tracking.
- Natural-language business data queries.
- Cloud deployment.
- More advanced predictive risk analytics.

## Author

**Pottabathini Amrutha**

Electronics and Communication Engineering Graduate

Interested in Business Intelligence, Data Analytics, Risk Management, Compliance, and Enterprise Operations.

## Disclaimer

Enterprise360 is an educational portfolio project developed for learning and demonstration purposes. It is not affiliated with or endorsed by any real organization. All sample data and displayed business figures are illustrative.
