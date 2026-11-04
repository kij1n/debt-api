# debt-api

A REST API for tracking personal debts and repayments, built with FastAPI and PostgreSQL.

> **Status: work in progress.** The MVP (debts, payments, automatic allocation, tests, CI, deployment) is planned for the end of 2026. See [Roadmap](#roadmap).

## What it does

debt-api keeps track of who owes whom and how much. Instead of storing a mutable "remaining balance" on each debt, it records payments and links them to debts through allocations, so every change in a balance can be traced back to a concrete payment.

- Record debts in both directions (`borrowed` / `lent`)
- Record payments and have them allocated to open debts automatically
- Query debts with filtering (date range, amount range) and pagination

## Tech stack

| Area | Tools |
| ------ | ------- |
| API | FastAPI, Pydantic v2 |
| Database | PostgreSQL 18, SQLAlchemy 2.0, Alembic |
| Tooling | uv, ruff, mypy, pre-commit |
| Testing | pytest |
| CI | GitHub Actions |

## Design decisions

**Double-entry model instead of a balance column.** Data is split into `Debt`, `Payment` and `Allocation`. A payment is never written directly into a debt; an allocation links a part of a payment to a specific debt. This gives a full audit trail and avoids a balance that can drift out of sync with the history.

**`amount_settled` is computed, not stored.** The settled amount exists only on the read schema (`DebtRead`) and is derived from allocations. There is no column that can be updated by mistake.

**Automatic allocation with row locking.** Creating a debt or a payment (`POST /debts`, `POST /payments`) runs a shared `allocate()` routine. It uses `SELECT ... FOR UPDATE` so that two concurrent requests cannot allocate the same payment or debt twice.

**Separate schemas for create, update and read.** `DebtCreate`, `DebtUpdate` and `DebtRead` are distinct, so clients cannot set server-controlled fields and responses can include computed values.

**Composable filters.** Query parameters are built from small Pydantic mixins (`Pagination`, `DateRange`, `AmountRange`) rather than one large base filter class, so each endpoint takes only the filters that make sense for it.

**Synchronous endpoints.** The API uses plain `def` endpoints run in FastAPI's threadpool. For a CRUD service with a synchronous ORM this keeps the code simpler without a meaningful performance cost.

## Getting started

### Requirements

- Python 3.13
- [uv](https://docs.astral.sh/uv/)
- Docker (for PostgreSQL)

### Run locally

```bash
git clone https://github.com/kij1n/debt-api.git
cd debt-api

# install dependencies
uv sync

# start PostgreSQL
docker compose up -d

# copy and fill in environment variables
cp .env.example .env

# start the API
uv run fastapi run
```

The interactive API docs are available at `http://localhost:8000/docs`.

### Run tests and checks

```bash
uv run ty check src
uv run ruff check .
```

## Project structure

```md
src/debt_api/
├── api/            # HTTP layer: FastAPI routers and app entry point (main.py)
├── services/       # business logic: allocation, validation, use cases
│   └── models/     # Pydantic schemas (Debt, Debtor, Payment, Allocation, filters)
└── db/             # persistence: SQLAlchemy models and queries
```

Requests flow one way: `api` → `services` → `db`. Routers contain no business logic, and services don't know about HTTP.

## Roadmap

### MVP

- [ ] Debts: create, read, update, filter
- [ ] Payments with automatic allocation
- [ ] Test coverage for allocation logic, including concurrent requests
- [ ] CI pipeline (lint, type check, tests)
- [ ] Public deployment

### After MVP

- [ ] API keys with per-user scoping and operation-level permissions
- [ ] Infrastructure on AWS managed with Terraform
- [ ] Discord bot for querying debts in natural language
