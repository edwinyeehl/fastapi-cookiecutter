# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

This project was bootstrapped using the FastAPI Cookiecutter template.

## Development Setup

### Prerequisites

1.  **Python {{ cookiecutter.python_version }}+**
2.  **uv** (Python package and environment manager) installed on your host system.
    If you do not have `uv` installed, get it via:
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
3.  **ODBC Driver for SQL Server** (if connecting to the primary SQL Server database locally).

### Environment Setup

This project uses environment variables for configuration. Sensitive credentials and environment-specific settings must be kept in a local `.env` file, which is ignored by git.

1.  **Create your local `.env` file** by copying the example file:
    ```bash
    cp .env.example .env
    ```

2.  **Configure your settings** in the newly created `.env`:
    *   **App Settings**: Change `APP_ENV` (e.g., `local`), toggle `DEBUG` mode, and set a unique, secure `SECRET_KEY` for JWT token signature verification.
    *   **Database Dialect (`DB_DIALECT`)**: Specify either `mssql` (SQL Server - primary dialect) or `postgresql` (PostgreSQL - supporting dialect).
    *   **Database URL (`DATABASE_URL`)**:
        *   **SQL Server (Main)**: By default, the template uses `mssql+aioodbc://...` to enable async database connections. Ensure the ODBC Driver for SQL Server is installed on your host system and update the credentials/host accordingly.
        *   **PostgreSQL (Supporting)**: If using PostgreSQL, comment out the SQL Server URI and uncomment the `postgresql+asyncpg://...` URI, replacing it with your Postgres username, password, host, port, and database name.

### Dependency Installation

Sync dependencies and setup the virtual environment using `uv`:
```bash
uv sync
```

### Running the Application

Start the FastAPI local development server:
```bash
uv run fastapi dev
```
Your API will be running at [http://localhost:8000](http://localhost:8000) and interactive Swagger documentation will be available at [http://localhost:8000/docs](http://localhost:8000/docs).

### Running Tests

To execute the test suite:
```bash
uv run pytest
```

## Project Structure

- `main.py` — Application entrypoint.
- `pyproject.toml` — Project dependencies and configuration managed by `uv`.
- `.env.example` — Template for local environment variables.
