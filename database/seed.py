
from db import get_connection


def seed_database():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        # 1. Insert departments
        departments = [
            ("Finance", 5000000),
            ("Procurement", 3500000),
            ("Operations", 4000000)
        ]

        for name, budget in departments:
            cursor.execute(
                """
                INSERT OR IGNORE INTO departments
                (department_name, annual_budget)
                VALUES (?, ?)
                """,
                (name, budget)
            )

        # Get department IDs
        department_ids = {
            row["department_name"]: row["department_id"]
            for row in cursor.execute(
                "SELECT department_id, department_name FROM departments"
            ).fetchall()
        }

        # 2. Insert vendors without duplicating them
        vendors = [
            ("Vendor A", "Technology", 4.5),
            ("Vendor B", "Equipment", 4.0),
            ("Vendor C", "Services", 3.8),
            ("Vendor D", "Logistics", 4.7),
            ("Vendor E", "Consulting", 3.5)
        ]

        vendor_ids = {}

        for name, category, rating in vendors:
            existing = cursor.execute(
                "SELECT vendor_id FROM vendors WHERE vendor_name = ?",
                (name,)
            ).fetchone()

            if existing:
                vendor_id = existing["vendor_id"]
            else:
                cursor.execute(
                    """
                    INSERT INTO vendors
                    (vendor_name, category, rating)
                    VALUES (?, ?, ?)
                    """,
                    (name, category, rating)
                )
                vendor_id = cursor.lastrowid

            vendor_ids[name] = vendor_id

        # 3. Insert transactions only on first seed
        transaction_samples = [
            ("Finance", "Vendor A", "2026-01-05", 12000, "Completed", "Software subscription"),
            ("Procurement", "Vendor B", "2026-01-12", 8500, "Completed", "Equipment purchase"),
            ("Operations", "Vendor C", "2026-01-19", 14200, "Pending", "Field operations support"),
            ("Finance", "Vendor A", "2026-02-05", 15000, "Completed", "Annual software renewal"),
            ("Procurement", "Vendor D", "2026-02-14", 9200, "Pending", "Logistics services"),
            ("Operations", "Vendor C", "2026-02-21", 18000, "Completed", "Infrastructure maintenance"),
            ("Finance", "Vendor E", "2026-03-03", 13500, "Completed", "Consulting services"),
            ("Procurement", "Vendor B", "2026-03-11", 11000, "Completed", "Office equipment"),
            ("Operations", "Vendor D", "2026-03-23", 16000, "Pending", "Network deployment"),
            ("Finance", "Vendor A", "2026-04-04", 19000, "Completed", "Technology services"),
            ("Procurement", "Vendor E", "2026-04-13", 14500, "Completed", "Vendor consultation"),
            ("Operations", "Vendor C", "2026-04-25", 21000, "Pending", "Project support"),
            ("Finance", "Vendor E", "2026-05-06", 15500, "Completed", "Audit services"),
            ("Procurement", "Vendor B", "2026-05-15", 17500, "Completed", "Equipment upgrade"),
            ("Operations", "Vendor D", "2026-05-26", 22000, "Pending", "Operations support"),
            ("Finance", "Vendor A", "2026-06-05", 20000, "Completed", "Software services"),
            ("Procurement", "Vendor B", "2026-06-16", 18500, "Pending", "Infrastructure equipment"),
            ("Operations", "Vendor C", "2026-06-27", 25000, "Completed", "Field project services")
        ]

        count = cursor.execute(
            "SELECT COUNT(*) AS total FROM transactions"
        ).fetchone()["total"]

        if count == 0:
            for dept, vendor, txn_date, amount, status, description in transaction_samples:
                cursor.execute(
                    """
                    INSERT INTO transactions
                    (department_id, vendor_id, transaction_date,
                     amount, status, description)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        department_ids[dept],
                        vendor_ids[vendor],
                        txn_date,
                        amount,
                        status,
                        description
                    )
                )

        # 4. Insert projects
        project_samples = [
            ("Project Alpha", "Finance", "2026-01-01", "2026-12-30", 85, "In Progress"),
            ("Project Beta", "Operations", "2026-02-01", "2026-10-30", 65, "Delayed"),
            ("Project Gamma", "Procurement", "2026-03-01", "2026-11-30", 92, "In Progress"),
            ("Project Delta", "Operations", "2026-04-01", "2026-12-15", 45, "In Progress"),
            ("Project Epsilon", "Finance", "2026-05-01", "2026-12-20", 78, "In Progress")
        ]

        if cursor.execute(
            "SELECT COUNT(*) AS total FROM projects"
        ).fetchone()["total"] == 0:

            for name, dept, start, deadline, completion, status in project_samples:
                cursor.execute(
                    """
                    INSERT INTO projects
                    (project_name, department_id, start_date,
                     deadline, completion_percentage, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        name,
                        department_ids[dept],
                        start,
                        deadline,
                        completion,
                        status
                    )
                )

        # 5. Insert risk records
        risk_samples = [
            ("Duplicate payment", "Duplicate transaction", "High",
             "Potential duplicate payment identified."),
            ("Vendor verification", "Vendor documentation", "Medium",
             "Additional vendor documents required."),
            ("Delayed approval", "Operational delay", "High",
             "Approval pending beyond expected timeline."),
            ("Budget review", "Budget variance", "Low",
             "Department budget requires monitoring."),
            ("Missing documents", "Data quality", "Medium",
             "Supporting documents are incomplete.")
        ]

        if cursor.execute(
            "SELECT COUNT(*) AS total FROM risk_records"
        ).fetchone()["total"] == 0:

            for risk_type, category, severity, description in risk_samples:
                cursor.execute(
                    """
                    INSERT INTO risk_records
                    (risk_type, severity, description, status)
                    VALUES (?, ?, ?, ?)
                    """,
                    (category, severity, description, "Open")
                )

        # 6. Audit log
        cursor.execute(
            """
            INSERT INTO audit_logs
            (action, entity_type, entity_id)
            VALUES (?, ?, ?)
            """,
            ("Initial synthetic data seed", "SYSTEM", 1)
        )

        connection.commit()

        # Display record counts
        for table in [
            "departments",
            "vendors",
            "transactions",
            "projects",
            "risk_records",
            "audit_logs"
        ]:
            total = cursor.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]

            print(f"{table}: {total} records")

        print("\nEnterprise360 sample data loaded successfully!")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    seed_database()
