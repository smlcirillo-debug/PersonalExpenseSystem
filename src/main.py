import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "personal_expenses.db"


def connect_db():
    """Apre la connessione e abilita i vincoli delle chiavi esterne."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_db():
    """Crea le tabelle se non esistono e inserisce le categorie iniziali."""
    with connect_db() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE CHECK(length(trim(name)) > 0)
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_date TEXT NOT NULL
                CHECK(length(expense_date) = 10
                AND expense_date GLOB
                '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'),
            amount REAL NOT NULL CHECK(amount > 0),
            category_id INTEGER NOT NULL,
            description TEXT,
            FOREIGN KEY(category_id) REFERENCES categories(id)
                ON UPDATE CASCADE ON DELETE RESTRICT
        );

        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month TEXT NOT NULL
                CHECK(length(month) = 7
                AND month GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]'),
            category_id INTEGER NOT NULL,
            amount REAL NOT NULL CHECK(amount > 0),
            FOREIGN KEY(category_id) REFERENCES categories(id)
                ON UPDATE CASCADE ON DELETE CASCADE,
            UNIQUE(month, category_id)
        );
        """)
        conn.executemany(
            "INSERT OR IGNORE INTO categories(name) VALUES (?)",
            [("Alimentari",), ("Trasporti",), ("Svago",), ("Casa",)]
        )


def read_positive_amount(prompt):
    while True:
        raw = input(prompt).strip().replace(",", ".")
        try:
            amount = float(raw)
            if amount > 0:
                return amount
            print("Errore: l'importo deve essere maggiore di zero.")
        except ValueError:
            print("Inserire un importo numerico valido.")


def read_date():
    while True:
        value = input("Data (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("Data non valida. Usare il formato YYYY-MM-DD.")


def read_month():
    while True:
        value = input("Mese (YYYY-MM): ").strip()
        try:
            datetime.strptime(value, "%Y-%m")
            return value
        except ValueError:
            print("Mese non valido. Usare il formato YYYY-MM.")


def list_categories():
    with connect_db() as conn:
        rows = conn.execute(
            "SELECT id, name FROM categories ORDER BY name"
        ).fetchall()
    if not rows:
        print("Nessuna categoria presente.")
    else:
        print("\nCategorie disponibili:")
        for category_id, name in rows:
            print(f"{category_id}. {name}")


def add_category():
    name = input("Nome della categoria: ").strip()
    if not name:
        print("Errore: il nome della categoria non può essere vuoto.")
        return

    with connect_db() as conn:
        exists = conn.execute(
            "SELECT id FROM categories WHERE name = ? COLLATE NOCASE",
            (name,)
        ).fetchone()
        if exists:
            print("La categoria esiste già.")
            return
        conn.execute("INSERT INTO categories(name) VALUES (?)", (name,))
    print("Categoria inserita correttamente.")


def get_category_id(name):
    with connect_db() as conn:
        row = conn.execute(
            "SELECT id FROM categories WHERE name = ? COLLATE NOCASE",
            (name,)
        ).fetchone()
    return row[0] if row else None


def add_expense():
    expense_date = read_date()
    amount = read_positive_amount("Importo: ")
    list_categories()
    category = input("Nome della categoria: ").strip()
    category_id = get_category_id(category)

    if category_id is None:
        print("Errore: la categoria non esiste.")
        return

    description = input("Descrizione (facoltativa): ").strip()
    with connect_db() as conn:
        conn.execute(
            """INSERT INTO expenses
               (expense_date, amount, category_id, description)
               VALUES (?, ?, ?, ?)""",
            (expense_date, amount, category_id, description or None)
        )
    print("Spesa inserita correttamente.")


def save_budget():
    month = read_month()
    list_categories()
    category = input("Nome della categoria: ").strip()
    category_id = get_category_id(category)
    if category_id is None:
        print("Errore: la categoria non esiste.")
        return

    amount = read_positive_amount("Importo del budget: ")
    with connect_db() as conn:
        conn.execute(
            """INSERT INTO budgets(month, category_id, amount)
               VALUES (?, ?, ?)
               ON CONFLICT(month, category_id)
               DO UPDATE SET amount = excluded.amount""",
            (month, category_id, amount)
        )
    print("Budget mensile salvato correttamente.")


def report_totals_by_category():
    query = """
        SELECT c.name, COALESCE(SUM(e.amount), 0)
        FROM categories c
        LEFT JOIN expenses e ON e.category_id = c.id
        GROUP BY c.id, c.name
        ORDER BY c.name
    """
    with connect_db() as conn:
        rows = conn.execute(query).fetchall()

    print("\nCategoria                  Totale speso")
    print("----------------------------------------")
    for name, total in rows:
        print(f"{name:<27} {total:>10.2f} EUR")


def report_budget_comparison():
    month = read_month()
    query = """
        SELECT c.name, b.amount,
               COALESCE(SUM(e.amount), 0) AS spent
        FROM budgets b
        JOIN categories c ON c.id = b.category_id
        LEFT JOIN expenses e
            ON e.category_id = b.category_id
            AND substr(e.expense_date, 1, 7) = b.month
        WHERE b.month = ?
        GROUP BY b.id, c.name, b.amount
        ORDER BY c.name
    """
    with connect_db() as conn:
        rows = conn.execute(query, (month,)).fetchall()

    if not rows:
        print("Non sono presenti budget per il mese selezionato.")
        return

    for name, budget, spent in rows:
        status = "SUPERAMENTO BUDGET" if spent > budget else "NEL BUDGET"
        print(f"\nMese: {month}")
        print(f"Categoria: {name}")
        print(f"Budget: {budget:.2f} EUR")
        print(f"Speso: {spent:.2f} EUR")
        print(f"Stato: {status}")


def report_all_expenses():
    query = """
        SELECT e.expense_date, c.name, e.amount,
               COALESCE(e.description, '')
        FROM expenses e
        JOIN categories c ON c.id = e.category_id
        ORDER BY e.expense_date, e.id
    """
    with connect_db() as conn:
        rows = conn.execute(query).fetchall()

    print("\nData        Categoria             Importo       Descrizione")
    print("---------------------------------------------------------------")
    for date, category, amount, description in rows:
        print(f"{date:<11} {category:<21} {amount:>8.2f} EUR  {description}")


def reports_menu():
    while True:
        print("""
========== MENU REPORT ==========
1. Totale spese per categoria
2. Spese mensili vs budget
3. Elenco completo delle spese
4. Ritorna al menu principale
=================================
""")
        try:
            choice = int(input("Inserisci la tua scelta: "))
        except ValueError:
            print("Scelta non valida. Riprovare.")
            continue

        match choice:
            case 1:
                report_totals_by_category()
            case 2:
                report_budget_comparison()
            case 3:
                report_all_expenses()
            case 4:
                return
            case _:
                print("Scelta non valida. Riprovare.")


def main():
    initialize_db()
    print("Benvenuto nel Sistema di Gestione delle Spese Personali!")

    while True:
        print("""
-------------------------------
    SISTEMA SPESE PERSONALI
-------------------------------
1. Gestione Categorie
2. Inserisci Spesa
3. Definisci Budget Mensile
4. Visualizza Report
5. Esci
-------------------------------
""")
        try:
            choice = int(input("Inserisci la tua scelta: "))
        except ValueError:
            print("Scelta non valida. Riprovare.")
            continue

        # In Python 3.10+ match/case svolge il ruolo di selezione switch.
        match choice:
            case 1:
                add_category()
            case 2:
                add_expense()
            case 3:
                save_budget()
            case 4:
                reports_menu()
            case 5:
                print("Chiusura del programma. Arrivederci!")
                break
            case _:
                print("Scelta non valida. Riprovare.")


if __name__ == "__main__":
    main()
