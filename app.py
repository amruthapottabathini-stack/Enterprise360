from ai_insights import generate_ai_insights
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

from database.queries import (
    load_transactions,
    load_risks,
    load_vendor_performance,
    load_data_quality_summary,
    load_projects,
)

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="Enterprise360 | Business Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================
# 2. PREMIUM DESIGN
# =====================================================
st.markdown(
    """
    <style>
    .stApp { background: #F3F6FB; }
    .block-container {
        max-width: 1500px;
        padding: 2rem 2.5rem 3rem;
    }
    h1, h2, h3 {
        color: #14233B;
        font-weight: 750;
        letter-spacing: -0.5px;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0D1B2A 0%, #173657 100%);
    }
    [data-testid="stSidebar"] * { color: #F5F8FC; }
    [data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E1E8F1;
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 5px 18px rgba(20,35,59,0.06);
        min-height: 120px;
    }
    [data-testid="stMetricLabel"] p {
        color: #718096;
        font-size: 14px;
        font-weight: 600;
    }
    [data-testid="stMetricValue"] {
        color: #14233B;
        font-size: 28px;
        font-weight: 800;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF;
        border: 1px solid #E3EAF3;
        border-radius: 16px;
        box-shadow: 0 5px 18px rgba(20,35,59,0.04);
    }
    [data-testid="stDataFrame"] {
        border: 1px solid #E2E8F0;
        border-radius: 12px;
    }
    div[data-baseweb="select"] > div { border-radius: 10px; }
    hr { border-color: #DFE6EF; }
    .top-header {
        background: #FFFFFF;
        padding: 13px 18px;
        border-radius: 12px;
        border: 1px solid #E3EAF3;
        text-align: right;
        color: #475467;
        font-size: 13px;
        font-weight: 600;
    }
    .section-label {
        color: #718096;
        font-size: 11px;
        letter-spacing: 1.4px;
        font-weight: 700;
        padding-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =====================================================
# 3. LOAD BUSINESS DATA FROM SQLITE
# =====================================================
df = load_transactions()
sql_risks = load_risks()
vendor_df = load_vendor_performance()
quality_summary = load_data_quality_summary()
projects_df = load_projects()

if df.empty:
    st.error("No transactions were found in the database. Run database/seed.py first.")
    st.stop()

# Risk distribution and risk register are derived from SQLite.
risk_distribution = (
    sql_risks["severity"]
    .value_counts()
    .reindex(["Low", "Medium", "High"], fill_value=0)
    .rename_axis("Risk Level")
    .reset_index(name="Records")
)

risk_records = pd.DataFrame(
    {
        "Reference": [f"RSK-{int(risk_id):04d}" for risk_id in sql_risks["risk_id"]],
        "Risk Type": sql_risks["risk_type"].tolist(),
        "Severity": sql_risks["severity"].tolist(),
        "Description": sql_risks["description"].tolist(),
        "Status": sql_risks["status"].tolist(),
    }
)

high_risk_count = int((sql_risks["severity"] == "High").sum())
open_risk_count = int((sql_risks["status"].str.lower() == "open").sum())

# Project information is currently illustrative; it will be moved to SQL
# when the projects module is connected in a later development step.
operations_data = pd.DataFrame(
    {
        "Project": ["Project Alpha", "Project Beta", "Project Gamma", "Project Delta", "Project Epsilon"],
        "Department": ["Finance", "Operations", "Procurement", "Operations", "Finance"],
        "Completion (%)": [85, 65, 92, 45, 78],
        "Status": ["On Track", "Delayed", "On Track", "In Progress", "In Progress"],
    }
)

# =====================================================
# 4. SIDEBAR NAVIGATION
# =====================================================
st.sidebar.markdown("# ◈ Enterprise360")
st.sidebar.caption("BUSINESS INTELLIGENCE")
st.sidebar.divider()

page = st.sidebar.radio(
    "WORKSPACE",
    [
        "Executive Overview",
        "Risk & Controls",
        "Data Quality",
        "Vendor Performance",
        "Operations",
        "AI Business Insights",
    ],
)

st.sidebar.divider()
st.sidebar.caption("ENVIRONMENT")
st.sidebar.success("● Demo system online")
st.sidebar.markdown("---")
st.sidebar.caption("ENTERPRISE360 | VERSION 1.0")

# =====================================================
# 5. SHARED PAGE HEADER
# =================================================
def page_header(title: str, description: str) -> None:
    left, right = st.columns([5, 2])

    with left:
        st.markdown(
            '<div class="section-label">ENTERPRISE INTELLIGENCE / WORKSPACE</div>',
            unsafe_allow_html=True,
        )

    with right:
        today = datetime.now().strftime("%d %b %Y")
        st.markdown(
            f'<div class="top-header">🟢 DEMO ENVIRONMENT&nbsp; | &nbsp;{today}&nbsp; | &nbsp;ADMIN</div>',
            unsafe_allow_html=True,
        )

    st.title(title)
    st.write(description)
    st.divider()

# =====================================================
# 6. EXECUTIVE OVERVIEW
# =====================================================
if page == "Executive Overview":
    page_header(
        "Executive Dashboard",
        "Monitor business performance, operational health and enterprise risks.",
    )

    filter_left, filter_right = st.columns(2)
    available_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

    with filter_left:
        period = st.selectbox("Reporting Period", ["All available months", "Last 3 available months"])

    with filter_right:
        department = st.selectbox(
            "Business Unit",
            ["All units", "Finance", "Procurement", "Operations"],
        )

    selected_months = available_months if period == "All available months" else available_months[-3:]
    filtered = df[df["Month"].isin(selected_months)].copy()

    if department != "All units":
        filtered = filtered[filtered["Department"] == department]

    total_transactions = int(len(filtered))
    total_value = float(filtered["amount"].sum())

    st.markdown("### Business Performance")
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Transactions Processed", f"{total_transactions:,}")
    c2.metric("Transaction Value", f"${total_value:,.0f}")
    c3.metric(
        "High-Risk Records",
        high_risk_count,
        delta=f"{open_risk_count} open risks (all severity levels)",
        delta_color="inverse",
    )

    quality_issues = (
        quality_summary["missing_vendor"]
        + quality_summary["missing_description"]
        + quality_summary["duplicate_records"]
    )
    total_quality_rows = max(int(quality_summary["total_transactions"]), 1)
    quality_score = max(0.0, 100.0 * (1 - quality_issues / total_quality_rows))
    c4.metric("Data Quality Score", f"{quality_score:.1f}%")

    st.markdown("### Performance Analytics")
    chart_left, chart_right = st.columns(2)

    monthly = filtered.groupby("Month", as_index=False)["Transactions"].sum()
    monthly["Month"] = pd.Categorical(monthly["Month"], categories=available_months, ordered=True)
    monthly = monthly.sort_values("Month")

    with chart_left:
        with st.container(border=True):
            st.markdown("**Transaction Trends**")
            st.caption("Monthly transaction volume from SQLite")
            fig = px.bar(
                monthly,
                x="Month",
                y="Transactions",
                text="Transactions",
                color_discrete_sequence=["#2878D0"],
            )
            fig.update_traces(textposition="outside", marker_line_width=0)
            fig.update_layout(
                height=350,
                margin=dict(l=10, r=10, t=25, b=10),
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(color="#475467"),
                showlegend=False,
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="#EDF1F6", title="Transactions"),
            )
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

    with chart_right:
        with st.container(border=True):
            st.markdown("**Enterprise Risk Distribution**")
            st.caption("Risk records grouped by severity from SQLite")
            fig2 = px.pie(
                risk_distribution,
                names="Risk Level",
                values="Records",
                hole=0.65,
                color="Risk Level",
                color_discrete_map={"Low": "#2878D0", "Medium": "#F5B942", "High": "#E76F51"},
            )
            fig2.update_traces(textinfo="percent")
            fig2.update_layout(
                height=350,
                margin=dict(l=10, r=10, t=20, b=10),
                paper_bgcolor="white",
                legend=dict(orientation="h", y=-0.1),
            )
            st.plotly_chart(fig2, width="stretch", config={"displayModeBar": False})

    st.markdown("### Recent Transactions")
    recent_transactions = filtered[
        ["transaction_id", "transaction_date", "Department", "vendor_name", "amount", "status"]
    ].sort_values("transaction_date", ascending=False).head(10).copy()
    recent_transactions.columns = ["Transaction ID", "Date", "Department", "Vendor", "Amount", "Status"]
    st.dataframe(recent_transactions, width="stretch", hide_index=True)

# =====================================================
# 7. RISK & CONTROLS
# =====================================================
elif page == "Risk & Controls":
    page_header("Risk & Controls", "Monitor enterprise risks, control exceptions and outstanding reviews.")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Risk Records", len(sql_risks))
    c2.metric("High-Risk Records", high_risk_count)
    c3.metric("Open Risk Records", open_risk_count)

    st.markdown("### Risk Distribution")
    fig = px.bar(
        risk_distribution,
        x="Risk Level",
        y="Records",
        color="Risk Level",
        color_discrete_map={"Low": "#2878D0", "Medium": "#F5B942", "High": "#E76F51"},
        text="Records",
    )
    fig.update_layout(height=350, plot_bgcolor="white", paper_bgcolor="white", showlegend=False)
    st.plotly_chart(fig, width="stretch")

    st.markdown("### Risk Register")
    st.dataframe(risk_records, width="stretch", hide_index=True)
    st.caption("Risk records are retrieved from the Enterprise360 SQLite database.")

# =====================================================
# 8. DATA QUALITY
# =====================================================
# =====================================================
# DATA QUALITY
# =====================================================

elif page == "Data Quality":

    page_header(
        "Data Quality Management",
        "Monitor data completeness, consistency and "
        "transaction integrity."
    )

    total = quality_summary["total_transactions"]
    missing_vendor = quality_summary["missing_vendor"]
    missing_description = quality_summary["missing_description"]
    duplicates = quality_summary["duplicate_records"]

    # KPI CARDS
    st.markdown("### Data Quality Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Transactions Checked", total)
    c2.metric("Missing Vendor", missing_vendor)
    c3.metric("Missing Description", missing_description)
    c4.metric("Duplicate Rows", duplicates)

    st.divider()

    # VALIDATION RESULTS
    st.markdown("### Data Validation Report")

    checks = pd.DataFrame({
        "Validation Check": [
            "Total transactions",
            "Missing vendor information",
            "Missing descriptions",
            "Duplicate transaction rows"
        ],
        "Records Flagged": [
            total,
            missing_vendor,
            missing_description,
            duplicates
        ],
        "Status": [
            "Completed",
            "Passed" if missing_vendor == 0 else "Review",
            "Passed" if missing_description == 0 else "Review",
            "Passed" if duplicates == 0 else "Review"
        ]
    })

    st.dataframe(
        checks,
        width="stretch",
        hide_index=True
    )

    st.divider()

    if missing_vendor == 0 and missing_description == 0 and duplicates == 0:
        st.success(
            "All configured data-quality checks passed "
            "for the current sample dataset."
        )
    else:
        st.warning(
            "Some records require data-quality investigation."
        )

    st.caption(
        "Source: Enterprise360 SQLite database. "
        "Validation checks currently cover vendor links, "
        "descriptions and duplicate transaction combinations."
    )


# =====================================================
# 9. VENDOR PERFORMANCE
# =====================================================
elif page == "Vendor Performance":
    page_header("Vendor Performance", "Analyze vendor spending, transaction activity and supplier status.")

    total_vendors = len(vendor_df)
    total_spend = float(vendor_df["total_spend"].sum())
    total_completed = int(vendor_df["completed_transactions"].sum())
    total_pending = int(vendor_df["pending_transactions"].sum())

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Vendors", total_vendors)
    c2.metric("Total Vendor Spend", f"${total_spend:,.0f}")
    c3.metric("Completed Transactions", total_completed)
    c4.metric("Pending Transactions", total_pending)

    chart_left, chart_right = st.columns(2)
    with chart_left:
        with st.container(border=True):
            st.markdown("**Vendor Spending**")
            st.caption("Total transaction value by vendor")
            fig = px.bar(
                vendor_df,
                x="vendor_name",
                y="total_spend",
                text_auto=".2s",
                color_discrete_sequence=["#2878D0"],
            )
            fig.update_layout(height=350, plot_bgcolor="white", paper_bgcolor="white", showlegend=False, xaxis_title="Vendor", yaxis_title="Total Spend")
            st.plotly_chart(fig, width="stretch")

    with chart_right:
        with st.container(border=True):
            st.markdown("**Vendor Transaction Activity**")
            st.caption("Completed versus pending transactions")
            activity = vendor_df[["vendor_name", "completed_transactions", "pending_transactions"]].melt(
                id_vars="vendor_name",
                var_name="Transaction Status",
                value_name="Number of Transactions",
            )
            activity["Transaction Status"] = activity["Transaction Status"].replace(
                {"completed_transactions": "Completed", "pending_transactions": "Pending"}
            )
            fig2 = px.bar(
                activity,
                x="vendor_name",
                y="Number of Transactions",
                color="Transaction Status",
                barmode="group",
                color_discrete_map={"Completed": "#249B70", "Pending": "#F5B942"},
            )
            fig2.update_layout(height=350, plot_bgcolor="white", paper_bgcolor="white", xaxis_title="Vendor", yaxis_title="Transactions")
            st.plotly_chart(fig2, width="stretch")

    st.markdown("### Vendor Register")
    display_vendors = vendor_df[[
        "vendor_name", "category", "rating", "status", "transaction_count",
        "total_spend", "completed_transactions", "pending_transactions",
    ]].copy()
    display_vendors.columns = [
        "Vendor", "Category", "Rating", "Status", "Total Transactions",
        "Total Spend", "Completed", "Pending",
    ]
    st.dataframe(display_vendors, width="stretch", hide_index=True)
    st.caption("Vendor information is retrieved from the Enterprise360 SQLite database. Delivery performance is not yet tracked in the database.")

# =====================================================
# 10. OPERATIONS
# =====================================================

# =====================================================
# OPERATIONS MANAGEMENT – SQL CONNECTED
# =====================================================

elif page == "Operations":

    page_header(
        "Operations Management",
        "Monitor project progress, delivery timelines "
        "and operational performance."
    )

    # Calculate actual project metrics
    total_projects = len(projects_df)

    delayed_projects = int(
        (projects_df["status"].str.lower() == "delayed").sum()
    )

    average_completion = (
        projects_df["completion_percentage"].mean()
        if total_projects > 0 else 0
    )

    # KPI CARDS
    st.markdown("### Project Performance")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Projects",
        total_projects
    )

    c2.metric(
        "Average Completion",
        f"{average_completion:.1f}%"
    )

    c3.metric(
        "Delayed Projects",
        delayed_projects
    )

    st.divider()

    # PROJECT PROGRESS CHART
    st.markdown("### Project Progress Analytics")

    if not projects_df.empty:

        with st.container(border=True):

            fig = px.bar(
                projects_df,
                x="project_name",
                y="completion_percentage",
                color="status",
                text="completion_percentage",
                color_discrete_map={
                    "In Progress": "#2878D0",
                    "Delayed": "#E76F51",
                    "Completed": "#249B70"
                },
                labels={
                    "project_name": "Project",
                    "completion_percentage": "Completion (%)",
                    "status": "Project Status"
                }
            )

            fig.update_traces(
                texttemplate="%{text}%",
                textposition="outside"
            )

            fig.update_layout(
                height=380,
                plot_bgcolor="white",
                paper_bgcolor="white",
                yaxis=dict(
                    range=[0, 110],
                    title="Completion (%)",
                    gridcolor="#EDF1F6"
                ),
                xaxis=dict(showgrid=False),
                legend_title="Project Status"
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

        # PROJECT REGISTER
        st.markdown("### Project Register")

        display_projects = projects_df[
            [
                "project_name",
                "department_name",
                "start_date",
                "deadline",
                "completion_percentage",
                "status"
            ]
        ].copy()

        display_projects.columns = [
            "Project",
            "Department",
            "Start Date",
            "Deadline",
            "Completion (%)",
            "Status"
        ]

        st.dataframe(
            display_projects,
            width="stretch",
            hide_index=True
        )

        st.caption(
            "Project records retrieved directly from "
            "the Enterprise360 SQLite database."
        )

    else:
        st.info("No project records found in the database.")


# =====================================================
# 11. AI BUSINESS INSIGHTS
# =====================================================

# =====================================================
# AI BUSINESS INSIGHTS ENGINE
# =====================================================

elif page == "AI Business Insights":

    page_header(
        "AI Business Insights",
        "Convert business data into actionable management insights."
    )

    # ANALYZE SQL DATA

    total_transactions = len(df)
    total_value = df["amount"].sum()

    pending_transactions = int(
        (df["status"].str.lower() == "pending").sum()
    )

    completed_transactions = int(
        (df["status"].str.lower() == "completed").sum()
    )

    high_risks = int(
        (sql_risks["severity"].str.lower() == "high").sum()
    )

    open_risks = int(
        (sql_risks["status"].str.lower() == "open").sum()
    )

    delayed_projects = int(
        (projects_df["status"].str.lower() == "delayed").sum()
    )

    data_quality_issues = (
        quality_summary["missing_vendor"]
        + quality_summary["missing_description"]
        + quality_summary["duplicate_records"]
    )

    # BUSINESS SUMMARY

    st.markdown("### Enterprise Performance Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Transactions Analyzed",
        total_transactions
    )

    c2.metric(
        "Transaction Value",
        f"${total_value:,.0f}"
    )

    c3.metric(
        "High-Risk Records",
        high_risks
    )

    c4.metric(
        "Pending Transactions",
        pending_transactions
    )

    st.divider()

    # OBSERVATION ENGINE

    st.markdown("### Business Intelligence Observations")

    insights = []

    if high_risks > 0:
        insights.append(
            ("High Risk",
             f"{high_risks} high-severity risk records "
             "require management review.")
        )

    if pending_transactions > 0:
        insights.append(
            ("Pending Transactions",
             f"{pending_transactions} transactions are pending. "
             "Follow up on outstanding approvals.")
        )

    if delayed_projects > 0:
        insights.append(
            ("Project Delays",
             f"{delayed_projects} project(s) are marked delayed. "
             "Review timelines and resource allocation.")
        )

    if data_quality_issues > 0:
        insights.append(
            ("Data Quality",
             f"{data_quality_issues} configured validation "
             "findings require investigation.")
        )

    if not insights:
        insights.append(
            ("Business Status",
             "No issues were detected by the configured rules.")
        )

    for category, message in insights:

        with st.container(border=True):
            st.markdown(f"**{category}**")
            st.write(message)

    # SPENDING ANALYSIS

    st.divider()

    st.markdown("### Department Spending Analysis")

    department_spend = (
        df.groupby("Department", as_index=False)
        ["amount"].sum()
        .sort_values("amount", ascending=False)
    )

    left, right = st.columns(2)

    with left:

        st.markdown("**Department Transaction Value**")

        fig = px.bar(
            department_spend,
            x="Department",
            y="amount",
            text_auto=",.0f",
            color_discrete_sequence=["#2878D0"]
        )

        fig.update_layout(
            height=350,
            paper_bgcolor="white",
            plot_bgcolor="white",
            showlegend=False
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    with right:

        st.markdown("**Transaction Status**")

        status_data = pd.DataFrame({
            "Status": ["Completed", "Pending"],
            "Count": [
                completed_transactions,
                pending_transactions
            ]
        })

        fig2 = px.pie(
            status_data,
            names="Status",
            values="Count",
            hole=0.6,
            color="Status",
            color_discrete_map={
                "Completed": "#249B70",
                "Pending": "#F5B942"
            }
        )

        fig2.update_layout(
            height=350,
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig2,
            width="stretch"
        )

    # MANAGEMENT RECOMMENDATIONS

    st.divider()

    st.markdown("### Recommended Management Actions")

    recommendations = []

    if high_risks > 0:
        recommendations.append(
            "Investigate high-severity risk records and "
            "document corrective actions."
        )

    if pending_transactions > 0:
        recommendations.append(
            "Review pending transactions and follow up "
            "with the responsible departments."
        )

    if delayed_projects > 0:
        recommendations.append(
            "Review delayed projects and assess their "
            "delivery schedules."
        )

    if data_quality_issues > 0:
        recommendations.append(
            "Resolve missing information and duplicate "
            "transaction findings."
        )

    if not recommendations:
        recommendations.append(
            "Continue routine monitoring of business performance."
        )

    for index, recommendation in enumerate(recommendations, 1):
        st.write(f"**{index}.** {recommendation}")
    # GEMINI AI BUSINESS ANALYSIS

    st.divider()
    st.markdown("### 🤖 Gemini AI Business Analysis")

    if st.button("Generate AI Business Insights", type="primary"):

        metrics = {
            "total_transactions": total_transactions,
            "total_transaction_value": float(total_value),
            "completed_transactions": completed_transactions,
            "pending_transactions": pending_transactions,
            "high_risks": high_risks,
            "delayed_projects": delayed_projects,
            "data_quality_issues": data_quality_issues
        }

        api_key = st.secrets.get("GEMINI_API_KEY", "")

        try:
            with st.spinner("Gemini is analyzing business performance..."):
                ai_result = generate_ai_insights(api_key, metrics)

            st.markdown("#### AI Analysis")
            st.markdown(ai_result)

        except Exception as e:
            st.error(f"AI analysis failed: {e}")
    st.caption(
        "Enterprise360 Insights Engine | "
        "Python-based analytical rules using SQLite data. "
        "Powered by Google Gemini AI for evidence-based business insights."
    )


# =====================================================
# 12. FOOTER
# =====================================================
st.divider()
st.caption("Enterprise360 | Business Intelligence & Risk Monitoring | Developed by Amrutha | Synthetic demonstration data")
