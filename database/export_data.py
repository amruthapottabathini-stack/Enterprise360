
from pathlib import Path
import pandas as pd

from db import get_connection

# Create Power BI export folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

EXPORT_DIR = PROJECT_DIR / "reports" / "powerbi"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def export_powerbi_data():

    connection = get_connection()

    try:
        tables = [
            "departments",
            "vendors",
            "transactions",
            "projects",
            "risk_records"
        ]

        print("ENTERPRISE360 - POWER BI EXPORT")
        print("--------------------------------")

        for table in tables:

            data = pd.read_sql_query(
                f"SELECT * FROM {table}",
                connection
            )

            file_path = EXPORT_DIR / f"{table}.csv"

            data.to_csv(
                file_path,
                index=False
            )

            print(
                f"{table}: {len(data)} records exported"
            )

        # Create an enriched transaction report
        query = """
            SELECT
                t.transaction_id,
                t.transaction_date,
                d.department_name,
                v.vendor_name,
                v.category AS vendor_category,
                t.amount,
                t.status,
                t.description
            FROM transactions t
            JOIN departments d
                ON t.department_id = d.department_id
            LEFT JOIN vendors v
                ON t.vendor_id = v.vendor_id
            ORDER BY t.transaction_date
        """

        enriched = pd.read_sql_query(
            query,
            connection
        )

        enriched.to_csv(
            EXPORT_DIR / "transaction_analysis.csv",
            index=False
        )

        print("\nPower BI export completed!")
        print(f"Files saved to: {EXPORT_DIR}")

    finally:
        connection.close()


if __name__ == "__main__":
    export_powerbi_data()
