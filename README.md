# PersonalExpenseSystem

Sistema da console per la gestione delle spese personali e dei budget mensili di un singolo utente.

## Requisiti per l'esecuzione
- Python 3.10 o superiore (necessario per il costrutto `match/case`).
- SQLite, utilizzato tramite il modulo standard `sqlite3` incluso in Python.
- Librerie esterne: nessuna.

## Struttura del repository
```text
PersonalExpenseSystem/
├── src/
│   └── main.py
├── sql/
│   ├── database.sql
│   └── schema_logico.png
├── demo/
│   └── demo_video.mp4
└── README.md
```

## Avvio del programma
Aprire il terminale nella cartella principale del progetto ed eseguire:

```bash
python src/main.py
```

Se il sistema utilizza il comando `python3`, eseguire:

```bash
python3 src/main.py
```

Il database SQLite `personal_expenses.db` viene creato automaticamente al primo avvio. Il programma inserisce anche alcune categorie iniziali.

## Creazione manuale del database con lo script SQL
Dalla cartella principale, se è installato il programma a riga di comando di SQLite, eseguire:

```bash
sqlite3 personal_expenses.db < sql/database.sql
```

## Funzionalità
1. Gestione delle categorie con controllo dei duplicati.
2. Inserimento delle spese con data, importo, categoria e descrizione facoltativa.
3. Definizione o aggiornamento del budget mensile per categoria.
4. Report del totale per categoria, confronto mensile spese/budget ed elenco cronologico.

## Dimostrazione
Il video presente in `demo/demo_video.mp4` illustra l'avvio, il menu, la gestione delle spese, il budget e i report.
