# PyClimb

> A Python practice platform for writing and browsing coding problems.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Django](https://img.shields.io/badge/Django-6.0.1-0C4B33.svg)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Required-2496ED.svg)](https://www.docker.com/)

PyClimb is a learning-first project to build a complete end-to-end web app: database, backend, admin tooling, and eventually problem solving + submissions.

Right now, PyClimb supports:
- PostgreSQL-backed Django project
- `Problem` model (title, description, constraints, follow-up, difficulty, published)
- Admin UI to create/manage problems
- Problem list + detail pages (class-based views)