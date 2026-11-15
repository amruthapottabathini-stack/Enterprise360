
import pandas as pd
from .db import get_connection


def load_transactions():
    """Retrieve business transactions from SQLite."""

    connection = get_connection()

    try:
        query = """
            SELECT
                t.transaction_id,
                t.transaction_date,
                t.amount,
                t.status,
                t.description,
                d.department_name,
                v.vendor_name
            FROM transactions t
            JOIN departments d
                ON t.department_id = d.department_id
            LEFT JOIN vendors v
                ON t.vendor_id = v.vendor_id
            ORDER BY t.transaction_date
        """

        df = pd.read_sql_query(query, connection)

        if not df.empty:
            df["transaction_date"] = pd.to_datetime(
                df["transaction_date"]
            )

            df["Month"] = df[
                "transaction_date"
            ].dt.strftime("%b")

            df["Department"] = df["department_name"]

            df["Transactions"] = 1

            df["Value_USD_M"] = df["amount"] / 1_000_000

        return df

    finally:
        connection.close()


def load_risks():
    """Retrieve risk records from SQLite."""

    connection = get_connection()

    try:
        query = """
            SELECT
                risk_id,
                risk_type,
                severity,
                description,
                status,
                created_at
            FROM risk_records
            ORDER BY created_at DESC
        """

        return pd.read_sql_query(query, connection)

    finally:
        connection.close()

def load_vendor_performance():
    """Retrieve vendor performance from SQLite."""

    connection = get_connection()

    try:
        query = """
            SELECT
                v.vendor_id,
                v.vendor_name,
                v.category,
                v.rating,
                v.status,
                COUNT(t.transaction_id) AS transaction_count,
                COALESCE(SUM(t.amount), 0) AS total_spend,
                SUM(
                    CASE
                        WHEN t.status = 'Completed' THEN 1
                        ELSE 0
                    END
                ) AS completed_transactions,
                SUM(
                    CASE
                        WHEN t.status = 'Pending' THEN 1
                        ELSE 0
                    END
                ) AS pending_transactions
            FROM vendors v
            LEFT JOIN transactions t
                ON v.vendor_id = t.vendor_id
            GROUP BY
                v.vendor_id,
                v.vendor_name,
                v.category,
                v.rating,
                v.status
            ORDER BY total_spend DESC
        """

        return pd.read_sql_query(query, connection)

    finally:
        connection.close()


def load_data_quality_summary():
    """Calculate basic data-quality indicators."""

    connection = get_connection()

    try:
        total = connection.execute(
            "SELECT COUNT(*) FROM transactions"
        ).fetchone()[0]

        missing_vendor = connection.execute("""
            SELECT COUNT(*)
            FROM transactions
            WHERE vendor_id IS NULL
        """).fetchone()[0]

        missing_description = connection.execute("""
            SELECT COUNT(*)
            FROM transactions
            WHERE description IS NULL
               OR TRIM(description) = ''
        """).fetchone()[0]

        duplicates = connection.execute("""
            SELECT COALESCE(SUM(duplicate_count - 1), 0)
            FROM (
                SELECT COUNT(*) AS duplicate_count
                FROM transactions
                GROUP BY
                    department_id,
                    vendor_id,
                    transaction_date,
                    amount
                HAVING COUNT(*) > 1
            )
        """).fetchone()[0]

        return {
            "total_transactions": total,
            "missing_vendor": missing_vendor,
            "missing_description": missing_description,
            "duplicate_records": duplicates
        }

    finally:
        connection.close()

def load_projects():
    """Retrieve project information from SQLite."""

    connection = get_connection()

    try:
        query = """
            SELECT
                p.project_id,
                p.project_name,
                d.department_name,
                p.start_date,
                p.deadline,
                p.completion_percentage,
                p.status
            FROM projects p
            LEFT JOIN departments d
                ON p.department_id = d.department_id
            ORDER BY p.project_id
        """

        return pd.read_sql_query(query, connection)

    finally:
        connection.close()
