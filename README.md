# PyClimb

> A Python practice platform for writing, browsing, and solving coding problems.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Django](https://img.shields.io/badge/Django-6.0.1-0C4B33.svg)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Required-2496ED.svg)](https://www.docker.com/)


**PyClimb** is a learning-first, end-to-end web application.  
The goal of the project is to understand how a real production-style web app is built, intentionally developed step-by-step, focusing on **clarity, correctness, and backend fundamentals** rather than rushing features.

---

## Table of Contents
- [Current Features](#current-features)
- [Security Notice](#security-notice)
- [Why This Project Exists](#why-this-project-exists)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure-simplified)
- [Running Locally (Development)](#running-locally-development)
- [Planned Next Steps](#planned-next-steps)
- [License](#license)
- [Notes](#notes)

---

## Current Features

At its current stage, PyClimb supports:

### Problem Management
- `Problem` model with title, description, constraints, follow-up, difficulty, and publish state
- `TestCase` model with machine-readable inputs/outputs and human-readable display versions
- Sample vs hidden test cases
- Django Admin UI with inline test case editing

### Submission System
- `Submission` model tracking code, status, verdict, and per-test-case results
- **Code execution** via subprocess with safety guardrails
- **Verdicts:** Accepted, Wrong Answer, Runtime Error, Time Limit Exceeded, Compilation Error
- **Detailed feedback** showing expected vs actual output for sample tests
- stdin/stdout execution model (not function-call style)

### User Interface
- Problem list and detail pages
- Submission form with format guidance and code template
- Submission result page with test case breakdown

### Infrastructure
- PostgreSQL-backed Django project (database in Docker)
- Slug-based URLs for problems

---

## Security Notice

⚠️ **The current code execution system is for local development only.**

The judge runs user-submitted Python code with basic safeguards (subprocess isolation, timeouts, output limits), but **lacks full sandboxing**. A malicious user could:
- Read files from the host system
- Make network connections
- Exhaust system resources

**Do not deploy to the public internet without implementing container isolation.**

See **[SECURITY.md](SECURITY.md)** for:
- Current safeguards and their limitations
- Known attack vectors
- Production deployment requirements
- Implementation roadmap

---

## Why This Project Exists

PyClimb is built as a **learning project** to practice:

- Relational database modeling
- Django ORM and migrations
- Admin tooling and developer UX
- Separation of human-facing vs machine-facing data
- Clean backend architecture before adding complexity

Rather than copying LeetCode’s UI or features directly, PyClimb prioritizes **understanding the “why” behind backend design decisions**.

---

## Tech Stack

- **Backend:** Django 6.x
- **Database:** PostgreSQL 16
- **Database Runtime:** Docker
- **Frontend:** Django templates (for now)

---

## Project Structure (Simplified)
```
pyclimb/
├── problems/              # Problem browsing app
│   ├── models.py          # Problem, TestCase
│   ├── views.py           # List and detail views
│   ├── admin.py           # Admin configuration
│   └── templates/
├── submissions/           # Code submission app
│   ├── models.py          # Submission
│   ├── views.py           # Create and detail views
│   ├── services/          # Judge logic
│   │   ├── judge.py       # Main judge orchestration
│   │   ├── runner.py      # Subprocess execution
│   │   └── normalize.py   # Output comparison
│   └── templates/
├── pyclimb/               # Project settings
│   ├── settings.py
│   └── urls.py
├── manage.py
├── SECURITY.md            # Security documentation
└── README.md
```


---

## Running Locally (Development)

> PyClimb is intended to be self-hosted, but the project is fully runnable locally for development and learning purposes.

### Requirements
- Python 3.11+
- Docker
- Docker Compose (or Docker Desktop)

### Setup (High-Level)

1. Clone the repository
2. Create a `.env` file with database credentials
3. Start PostgreSQL via Docker
4. Run Django migrations
5. Create a superuser
6. Start the development server

Detailed step-by-step setup may be added as the project stabilizes.

---

## Planned Next Steps

### Recently Completed
- ✅ Problem submission interface
- ✅ Code execution via subprocess
- ✅ Test case evaluation engine
- ✅ Submission results with detailed feedback

### Next Up
- [ ] User authentication
- [ ] Submission history per user
- [ ] Saved code drafts
- [ ] Container-based sandboxing for production safety
- [ ] Basic progress tracking

### Future
- [ ] Rate limiting
- [ ] Async execution queue (Celery)
- [ ] Multiple test case formats
- [ ] Performance metrics (execution time, memory)

---

## License

This project is licensed under the **MIT License**.

---

## Notes

This repository reflects an **in-progress learning project**.  
Design decisions may evolve as new concepts are explored and refined.
