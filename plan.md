# FastAPI Banking Backend: Phased Implementation Plan

This document outlines a phased strategy for building a database-agnostic, cookiecutter-ready FastAPI backend. The core philosophy is **incremental delivery**: each phase results in a standalone, deployable unit of working software. 

This template is designed to support both legacy integrations (SQL Server) and modern greenfield microservices (PostgreSQL) through dynamic environment configurations, while keeping AI agents (like Cursor, Copilot) strictly aligned with our coding standards.

---

## Phase 1: Foundation, Standards & Database Infrastructure
**Goal:** Establish the boilerplate, basic routing, dynamic database migration pipeline, and set strict guidelines for both human developers and AI agents.
**Working Software State:** A running API with health checks, connecting to either SQL Server or PostgreSQL based on `.env`, with a verifiable migration history and AI guardrails in place.

*   **1.1 Structure Initialization:** Set up the cookiecutter directory structure (e.g., `app/api`, `app/core`, `app/models`, `app/schemas`, `app/services`).
*   **1.2 Standards & Agent Rules (NEW):**
    *   **RESTful Guidelines (`RESTFUL_STANDARDS.md`):** Create documentation outlining strict API design rules (e.g., use plural nouns for routing like `/users`, standardize response models, map specific HTTP verbs to CRUD actions, strict dependency injection).
    *   **Agent Directives (`.cursorrules` or `AGENT_INSTRUCTIONS.md`):** Implement rules to govern AI tools like Cursor or GitHub Copilot. This file will instruct the AI to default to Pydantic v2 strict models (`ConfigDict`), enforce `async def` for async routes, prioritize `httpx.AsyncClient` for external calls, and prevent it from stripping PII redaction code.
*   **1.3 Dynamic Configuration:** Implement Pydantic `BaseSettings` for environment variables, parsing the `DATABASE_URL` to determine the dialect.
*   **1.4 SQLAlchemy & Alembic (Agnostic):**
    *   Configure the asynchronous SQLAlchemy engine factory to inject dialect-specific arguments (e.g., `fast_executemany=True` if `mssql` is detected).
    *   Initialize Alembic (`alembic init -t async`).
    *   Establish agnostic modeling guidelines (e.g., using `String(36)` or generic GUIDs instead of native DB UUIDs).
    *   Create the first migration: `users` and `local_admins` tables.
*   **1.5 Health Probes:** Implement `/health/liveness` and `/health/readiness` (executing a simple `SELECT 1` to verify DB health).
*   **1.6 Minimal Testing:** Configure `pytest`, `pytest-asyncio`, and `httpx`. Write integration tests using FastAPI's `TestClient` for the health probe endpoints against the active database.

## Phase 2: Telemetry & Structured Logging
**Goal:** Ensure the application is observable, Dynatrace-ready, and compliant with data privacy standards.
**Working Software State:** API logs all requests in structured JSON, correlates traces, and masks PII in both file and console outputs.

*   **2.1 Structlog Integration:** Replace standard logging with `structlog`. Configure JSON rendering for file sinks and console rendering for local development.
*   **2.2 W3C Trace Context Middleware:** Extract `traceparent` from headers and bind it to the `structlog` context variables.
*   **2.3 PII Redaction Processor:** Implement a custom log processor using regex to mask sensitive patterns (e.g., passwords, emails, financial IDs) before serialization.
*   **2.4 Minimal Testing:** Write unit tests for the PII regex redaction processor to guarantee sensitive strings are properly masked.

## Phase 3: Hybrid Authentication (AGAC & Local Admin)
**Goal:** Secure the API using a dual-authentication strategy.
**Working Software State:** Endpoints are protected. Users can authenticate via local admin bypass or the AGAC SOAP mock, receiving a JWT and mapped roles.

*   **3.1 JWT Infrastructure:** Implement PyJWT for token generation and verification. Set up FastAPI `Depends` for route protection.
*   **3.2 Local Admin Bypass:** Write authentication logic to check the `local_admins` DB table first (using bcrypt).
*   **3.3 AGAC SOAP Integration:**
    *   Build a SOAP client using `zeep` or `lxml` to communicate with AGAC.
    *   Parse the XML response to extract `PROFILE_CODE`.
    *   Implement role mapping to translate `PROFILE_CODE` to internal application roles.
*   **3.4 RBAC (Role-Based Access Control):** Create dependencies (e.g., `RequireRole("ROLE_OPERATOR")`) to lock down routes.
*   **3.5 Minimal Testing:** Use `pytest-mock` to intercept AGAC SOAP XML responses. Test local admin bypass, JWT decoding, and ensure RBAC dependencies return `403 Forbidden` for unauthorized roles.

## Phase 4: Audit Trail System
**Goal:** Guarantee non-repudiation by logging all state-changing actions.
**Working Software State:** POST/PUT/DELETE requests generate immutable audit records without adding latency.

*   **4.1 Audit Model:** Create an Alembic migration for an `audit_logs` table (Timestamp, UserID, IP, Action, Endpoint, Payload Diff).
*   **4.2 Audit Dependency:** Create a FastAPI dependency that captures the `Request` object and authenticated user state.
*   **4.3 Background Execution:** Use FastAPI `BackgroundTasks` to asynchronously write captured audit data to the database after the HTTP response completes.
*   **4.4 Minimal Testing:** Verify state-changing endpoints trigger the audit background task by checking the database state.

## Phase 5: Resiliency & Compliance Features
**Goal:** Harden the application for high-stakes operations.
**Working Software State:** API handles network failures gracefully, prevents duplicate transactions, and enforces dual-authorization.

*   **5.1 Circuit Breakers:** Wrap the AGAC SOAP call with a circuit breaker (e.g., `tenacity`) to prevent cascading failures.
*   **5.2 Idempotency Middleware:** Implement an idempotency key checker backed by Redis (or the active SQL database) to prevent double execution.
*   **5.3 Maker-Checker Implementation:**
    *   Build an `ApprovalRequest` workflow.
    *   Apply this to complex operations, requiring a "Maker" (ROLE_OPERATOR) to propose an adjustment and a "Checker" (ROLE_APPROVER) to execute it.
*   **5.4 Minimal Testing:** Write integration tests for the Maker-Checker workflow and test the idempotency key caching mechanism.