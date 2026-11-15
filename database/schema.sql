
PRAGMA foreign_keys = ON;

-- 1. Departments
CREATE TABLE IF NOT EXISTS departments (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT NOT NULL UNIQUE,
    annual_budget REAL DEFAULT 0
);

-- 2. Vendors
CREATE TABLE IF NOT EXISTS vendors (
    vendor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vendor_name TEXT NOT NULL,
    category TEXT,
    rating REAL,
    status TEXT DEFAULT 'Active'
);

-- 3. Transactions
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_id INTEGER NOT NULL,
    vendor_id INTEGER,
    transaction_date TEXT NOT NULL,
    amount REAL NOT NULL CHECK (amount >= 0),
    status TEXT DEFAULT 'Pending',
    description TEXT,
    FOREIGN KEY (department_id)
        REFERENCES departments(department_id),
    FOREIGN KEY (vendor_id)
        REFERENCES vendors(vendor_id)
);

-- 4. Projects
CREATE TABLE IF NOT EXISTS projects (
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT NOT NULL,
    department_id INTEGER,
    start_date TEXT,
    deadline TEXT,
    completion_percentage REAL DEFAULT 0,
    status TEXT DEFAULT 'In Progress',
    FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);

-- 5. Risk records
CREATE TABLE IF NOT EXISTS risk_records (
    risk_id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id INTEGER,
    risk_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'Open',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (transaction_id)
        REFERENCES transactions(transaction_id)
);

-- 6. Audit logs
CREATE TABLE IF NOT EXISTS audit_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT NOT NULL,
    entity_type TEXT,
    entity_id INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Database indexes
CREATE INDEX IF NOT EXISTS idx_transaction_date
ON transactions(transaction_date);

CREATE INDEX IF NOT EXISTS idx_transaction_department
ON transactions(department_id);

CREATE INDEX IF NOT EXISTS idx_risk_severity
ON risk_records(severity);
