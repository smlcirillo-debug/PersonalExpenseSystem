-- Personal Expense System
-- Database relazionale SQLite

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE CHECK (length(trim(name)) > 0)
);

CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_date TEXT NOT NULL
        CHECK (
            length(expense_date) = 10
            AND expense_date GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'
        ),
    amount REAL NOT NULL CHECK (amount > 0),
    category_id INTEGER NOT NULL,
    description TEXT,
    FOREIGN KEY (category_id) REFERENCES categories(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    month TEXT NOT NULL
        CHECK (
            length(month) = 7
            AND month GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]'
        ),
    category_id INTEGER NOT NULL,
    amount REAL NOT NULL CHECK (amount > 0),
    FOREIGN KEY (category_id) REFERENCES categories(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    UNIQUE (month, category_id)
);

-- Dati dimostrativi
INSERT OR IGNORE INTO categories (name) VALUES
    ('Alimentari'),
    ('Trasporti'),
    ('Svago'),
    ('Casa');

INSERT INTO expenses (expense_date, amount, category_id, description)
SELECT '2025-01-15', 25.00, id, 'Pranzo'
FROM categories WHERE name = 'Alimentari';

INSERT INTO expenses (expense_date, amount, category_id, description)
SELECT '2025-01-18', 45.50, id, 'Spesa supermercato'
FROM categories WHERE name = 'Alimentari';

INSERT INTO expenses (expense_date, amount, category_id, description)
SELECT '2025-01-20', 30.00, id, 'Carburante'
FROM categories WHERE name = 'Trasporti';

INSERT INTO expenses (expense_date, amount, category_id, description)
SELECT '2025-02-03', 18.00, id, 'Cinema'
FROM categories WHERE name = 'Svago';

INSERT INTO budgets (month, category_id, amount)
SELECT '2025-01', id, 60.00
FROM categories WHERE name = 'Alimentari'
ON CONFLICT(month, category_id) DO UPDATE SET amount = excluded.amount;

INSERT INTO budgets (month, category_id, amount)
SELECT '2025-01', id, 50.00
FROM categories WHERE name = 'Trasporti'
ON CONFLICT(month, category_id) DO UPDATE SET amount = excluded.amount;

INSERT INTO budgets (month, category_id, amount)
SELECT '2025-02', id, 40.00
FROM categories WHERE name = 'Svago'
ON CONFLICT(month, category_id) DO UPDATE SET amount = excluded.amount;
