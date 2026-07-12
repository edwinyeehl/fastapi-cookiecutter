# FastAPI Cookiecutter Template

An enterprise-ready, database-agnostic [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for bootstrapping modern [FastAPI](https://fastapi.tiangolo.com/) backends.

This template is designed to easily initialize a robust FastAPI backend with support for both legacy systems (such as SQL Server) and modern databases (such as PostgreSQL), environment-driven configuration, structured logging, JWT authentication, and maker-checker workflows.

## Features

This template is built following the phased design outlined in [plan.md](plan.md):

*   **Phase 1: Foundation & Agnostic Database Setup**
    *   Boilerplate structure setup under `app/` (APIs, core, models, schemas, services).
    *   Unified Pydantic `BaseSettings` parsing database connection URLs.
    *   SQLAlchemy & Alembic configuration tailored for both PostgreSQL and SQL Server (including `fast_executemany` optimizations).
    *   Health probe endpoints (`/health/liveness` and `/health/readiness`).
    *   `pytest` framework set up with async testing tools.
*   **Phase 2: Telemetry & Observability**
    *   Structured JSON logging using `structlog`.
    *   W3C trace context propagation (correlating requests with a request-bound trace context).
    *   PII Redaction custom log processor to mask sensitive user credentials, tokens, and PII.
*   **Phase 3: Hybrid Authentication**
    *   JWT token issuance and validation.
    *   Dual authentication path: Local Admin DB bypass (using bcrypt) and AGAC SOAP mock integration.
    *   FastAPI Dependency Injection for Role-Based Access Control (RBAC).
*   **Phase 4: Audit Trails**
    *   Database-backed audit logs tracking state-changing operations.
    *   Executed asynchronously using FastAPI `BackgroundTasks` to avoid API request latency.
*   **Phase 5: Resiliency & Compliance**
    *   Circuit breakers on external SOAP calls.
    *   Idempotency middleware using Redis/database cache.
    *   **Maker-Checker (Dual Authorization)** workflows for high-security tasks.

## Project Structure

*   `cookiecutter.json`: Template variable configuration (defines project name, slug, author, etc.).
*   `{{ cookiecutter.project_slug }}/`: The FastAPI application template directory.
    *   Managed by `uv` for lightning-fast dependency resolution and virtual environments.
*   `hooks/`: Post-generation hooks (e.g., automatically runs `uv sync` to set up your environment).
*   `plan.md`: The detailed roadmap outlining implementation phases.

## Getting Started

### Prerequisites

*   [Python 3.12+](https://www.python.org/)
*   [uv](https://github.com/astral-sh/uv) (recommended package and project manager)
*   [Cookiecutter](https://cookiecutter.readthedocs.io/) CLI tool

### Usage

1.  **Generate a new project** from this template:
    ```bash
    cookiecutter https://github.com/edwinyeehl/fastapi-cookiecutter
    ```
    *Or locally:*
    ```bash
    cookiecutter /path/to/fastapi-cookiecutter
    ```

2.  **Fill in the prompt prompts** when requested (project name, author, python version, etc.).

3.  Once completed, the post-generation hook will automatically run `uv sync` to configure the python virtual environment.

4.  **Run the application**:
    ```bash
    cd <your-project-slug>
    uv run fastapi dev
    ```

## License

This project is licensed under the MIT License.
