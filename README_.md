# PersonalExpenseSystem

Sistema da console per la gestione delle spese personali e dei budget mensili.

## Requisiti
- Python 3.10 o superiore (necessario per `match/case`).
- SQLite, incluso nel modulo standard `sqlite3` di Python.
- Non sono necessarie librerie esterne.

## Struttura
- `src/main.py`: codice sorgente Python.
- `sql/database.sql`: creazione del database e dati SQL dimostrativi.
- `sql/schema_logico.png`: schema logico delle tabelle e relazioni.
- `demo/demo_video.mp4`: video dimostrativo del funzionamento del programma.

## Avvio
Dalla cartella principale del progetto eseguire:

```bash
python src/main.py
```

Su alcuni sistemi il comando può essere:

```bash
python3 src/main.py
```

Il programma crea automaticamente `personal_expenses.db` nella cartella principale al primo avvio. Le categorie iniziali vengono inserite automaticamente.

## Database SQL
Per creare e popolare manualmente il database con lo script SQL:

```bash
sqlite3 personal_expenses.db < sql/database.sql
```

Il programma abilita le foreign key a ogni connessione. Lo script SQL contiene `PRIMARY KEY`, `FOREIGN KEY`, `CHECK`, `UNIQUE` e `NOT NULL`.

## Funzionalità
1. Inserimento e controllo delle categorie.
2. Registrazione di spese con data, importo, categoria e descrizione facoltativa.
3. Inserimento o aggiornamento del budget mensile per categoria.
4. Report delle spese per categoria, confronto mensile con il budget ed elenco cronologico.

## Demo video
Il file `demo_video.mp4` mostra l'avvio del programma, i menu, l'inserimento di una spesa, la definizione di un budget e la generazione dei report. La sequenza video è stata prodotta a partire da un'esecuzione di prova del programma.

## Nota
Il menu usa `match/case`, disponibile da Python 3.10, come costrutto di selezione equivalente allo `switch` richiesto nella traccia.
