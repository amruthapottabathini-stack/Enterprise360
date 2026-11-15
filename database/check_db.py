
from db import get_connection

connection = get_connection()

try:
    print("ENTERPRISE360 DATABASE CHECK")
    print("-----------------------------")

    tables = [
        "departments",
        "vendors",
        "transactions",
        "projects",
        "risk_records",
        "audit_logs"
    ]

    for table in tables:
        result = connection.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()

        print(f"{table}: {result[0]} records")

    print("\nRecent business transactions:")

    rows = connection.execute("""
        SELECT
            t.transaction_id,
            d.department_name,
            v.vendor_name,
            t.amount,
            t.status
        FROM transactions t
        JOIN departments d
            ON t.department_id = d.department_id
        LEFT JOIN vendors v
            ON t.vendor_id = v.vendor_id
        LIMIT 5
    """).fetchall()

    for row in rows:
        print(dict(row))

finally:
    connection.close()
