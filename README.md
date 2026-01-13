# PyClimb

> A Python practice platform for writing, browsing, and eventually solving coding problems.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Django](https://img.shields.io/badge/Django-6.0.1-0C4B33.svg)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Required-2496ED.svg)](https://www.docker.com/)


**PyClimb** is a learning-first, end-to-end web application.  
The goal of the project is to understand how a real production-style web app is built, intentionally developed step-by-step, focusing on **clarity, correctness, and backend fundamentals** rather than rushing features.

---

## Table of Contents
- [Current Features](#current-features)
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

- PostgreSQL-backed Django project
- Dockerized PostgreSQL database
- `Problem` model with:
  - title, description, constraints, follow-up
  - difficulty levels
  - published/unpublished state
- `TestCase` model with:
  - machine-readable inputs & expected outputs
  - human-readable display inputs/outputs
  - optional explanations
  - sample vs hidden test cases
- Django Admin UI:
  - create and manage problems
  - inline test case editing
  - filtering, searching, and publishing control
- Public problem list page
- Problem detail pages using class-based views

This stage primarily focuses on **content management and data modeling**, ensuring problems and test cases are structured correctly before introducing execution or submissions.

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
├── problems/
│ ├── migrations/
│ ├── models.py
│ ├── views.py
│ ├── admin.py
│ └── urls.py
├── pyclimb/
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── manage.py
├── .env
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

Short-term roadmap (not yet implemented):

- User authentication
- Problem submission interface
- Safe execution environment for Python code
- Test case evaluation engine
- Submission results & feedback
- Basic progress tracking

These features are intentionally deferred until the **data model and admin workflows feel solid**.

---

## License

This project is licensed under the **MIT License**.

---

## Notes

This repository reflects an **in-progress learning project**.  
Design decisions may evolve as new concepts are explored and refined.
