# Commit Analyzer Database Challenge

This coding exercise builds on the existing `commit_analyzer_db.py` script, which currently fetches commit data from the GitHub API, aggregates the monthly statistics, and posts the summary to a webhook. Your task is to extend the script by introducing a SQL database layer that stores, manages, and reports on the commit data.

## Objective
Augment the script so that commit metadata is persisted in a relational database before it is summarized and reported. The final solution should demonstrate the full lifecycle of working with a database: initializing the schema, creating relationships, performing CRUD-style operations, and exporting insights.

## Prerequisites
- Python 3.10+
- A lightweight SQL database such as SQLite (preferred for the challenge) or PostgreSQL/MySQL if you prefer.
- The [`requests`](https://docs.python-requests.org/) library (already used in the script).
- Any additional libraries required for interacting with your chosen database (e.g., `sqlite3` from the standard library or an ORM like `SQLAlchemy`).

## Tasks
1. **Initialize the database**
   - Decide where the database file or connection parameters should live.
   - Ensure the database is created (for SQLite, create the `.db` file; for other systems, ensure the connection succeeds and the schema is created on first run).

2. **Create database tables and relationships**
   - Design tables to store commit metadata (e.g., commits, authors, monthly summaries).
   - Define appropriate primary keys, foreign keys, and indexes to model relationships between commits and authors.
   - Include any necessary constraints to maintain data integrity.

3. **Perform database operations**
   - Insert commit and author records as the script processes the GitHub API response.
   - Demonstrate at least one update or delete operation (for example, handling duplicate commits or cleaning stale data).
   - Query the database to generate the monthly summary that was previously produced in-memory.

4. **Generate a text report**
   - Extract key insights from the stored data (e.g., top contributors, busiest months, average message length).
   - Save the report as a human-readable text file (e.g., `commit_report.txt`) alongside or within the project directory.
   - Ensure the report clearly references the data derived from the database.

## Deliverables
- Updated `commit_analyzer_db.py` implementing the above requirements.
- Any new modules or helper scripts you create to manage the database layer.
- The generated text report (it can be created dynamically when the script runs).

## Stretch Ideas (Optional)
- Add command-line arguments to control database path or report output location.
- Implement retry logic or caching for GitHub API calls before persisting data.
- Expose summary statistics via an API or additional webhook.

## Evaluation Criteria
- Correctness and robustness of the database schema and operations.
- Code readability and adherence to Python best practices.
- Thoughtful handling of edge cases (e.g., API failures, duplicate commits).
- Clarity of the text report and its alignment with the stored data.

Good luck, and have fun building the database-powered commit analyzer!
