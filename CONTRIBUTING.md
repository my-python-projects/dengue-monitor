# Contributing Guidelines

## Language

This project uses English for:

- Source code identifiers
- Function, class, variable, and file names
- Technical comments
- Logs
- API schemas and endpoints
- Technical documentation

Portuguese may be used for:

- Dashboard user-facing labels
- Domain-specific public health terms when appropriate
- Official dataset column names and acronyms

## Folder Organization

- `api`: FastAPI routes, schemas, and API services
- `core`: domain models and repository functions
- `data`: ingestion, transformation, lookup data, and analytical queries
- `dashboard`: Streamlit application and dashboard helpers
- `infra`: configuration, database setup, and logging
- `visualization`: chart-building functions

## Naming Conventions

- Functions and variables use `snake_case`
- Classes use `PascalCase`
- Constants use `UPPER_SNAKE_CASE`
- Files and modules use lowercase `snake_case`
- Official dataset column names and domain acronyms may be preserved when needed

## Code Style

This project uses:

- Black for code formatting
- Ruff for linting and import checks

Before opening a pull request, run:

```bash
black .
ruff check .
python -m compileall .
```