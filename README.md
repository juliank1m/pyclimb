# PyClimb

> A Python practice platform for writing, browsing, and solving coding problems with integrated learning content.

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
- Tag-based categorization and filtering
- Django Admin UI with inline test case editing

### Submission System
- `Submission` model tracking code, status, verdict, and per-test-case results
- **Code execution** via subprocess with safety guardrails
- **Verdicts:** Accepted, Wrong Answer, Runtime Error, Time Limit Exceeded, Compilation Error
- **Detailed feedback** showing expected vs actual output for sample tests
- stdin/stdout and function-call (LeetCode-style) execution modes

### Lessons & Learning Content
- **Courses** - Organize lessons into structured learning paths
- **Lessons** - Markdown-based content with code blocks and formatting
- **Rich Editor** - EasyMDE-powered editor with:
  - Full formatting toolbar (bold, italic, headings, lists, quotes, links)
  - Code block insertion with language selection
  - Image upload (file upload or URL)
  - Drag-and-drop image support
  - Side-by-side live preview
  - Fullscreen editing mode
  - Autosave
- **Draft/Published states** - Preview content before publishing
- **Problem linking** - Connect lessons to practice problems
- **Navigation** - Previous/next lesson navigation within courses
- **Teacher Dashboard** - Staff-only interface at `/learn/teach/` for content management

### User System
- User registration with email verification
- Login/logout authentication
- Password reset via email
- User profiles with statistics
- Leaderboard with solve counts

### User Interface
- Problem list with difficulty and tag filtering
- Submission form with format guidance and code template
- Submission result page with test case breakdown
- Learning section at `/learn/` with course and lesson views

### Infrastructure
- PostgreSQL-backed Django project (database in Docker)
- Slug-based URLs for problems and lessons
- Rate limiting for submissions and authentication
- Media file storage for lesson images

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
- Content management systems

Rather than copying LeetCode's UI or features directly, PyClimb prioritizes **understanding the "why" behind backend design decisions**.

---

## Tech Stack

- **Backend:** Django 6.x
- **Database:** PostgreSQL 16
- **Database Runtime:** Docker
- **Frontend:** Django templates
- **Markdown:** Python-Markdown with Pygments syntax highlighting
- **Editor:** EasyMDE (markdown editor)

---

## Project Structure (Simplified)
```
pyclimb/
├── problems/              # Problem browsing app
│   ├── models.py          # Problem, TestCase, Tag
│   ├── views.py           # List and detail views
│   ├── admin.py           # Admin configuration
│   └── templates/
├── submissions/           # Code submission app
│   ├── models.py          # Submission
│   ├── views.py           # Create and detail views
│   ├── services/          # Judge logic
│   │   ├── judge.py       # Main judge orchestration
│   │   ├── runner.py      # Subprocess execution
│   │   ├── sandbox.py     # Docker sandbox
│   │   └── normalize.py   # Output comparison
│   └── templates/
├── lessons/               # Learning content app
│   ├── models.py          # Course, Lesson
│   ├── views.py           # Public views + teacher dashboard
│   ├── forms.py           # Course and lesson forms
│   ├── admin.py           # Admin configuration
│   └── templates/
│       └── lessons/
│           ├── index.html         # Course/lesson list
│           ├── course_detail.html # Course page
│           ├── lesson_detail.html # Lesson with markdown content
│           └── teach/             # Teacher dashboard templates
├── accounts/              # User authentication
│   ├── models.py          # UserProfile, EmailVerification
│   └── signals.py         # Profile auto-creation
├── pyclimb/               # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── templates/         # Base templates
├── media/                 # User uploads (gitignored)
├── manage.py
├── DEPLOYMENT.md          # Production deployment guide
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

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pyclimb.git
   cd pyclimb
   ```

2. Create virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with database credentials:
   ```bash
   DB_NAME=pyclimb_db
   DB_USER=your_user
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

5. Start PostgreSQL via Docker:
   ```bash
   docker run -d \
     --name pyclimb-postgres \
     -e POSTGRES_DB=pyclimb_db \
     -e POSTGRES_USER=your_user \
     -e POSTGRES_PASSWORD=your_password \
     -p 5432:5432 \
     postgres:16
   ```

6. Run Django migrations:
   ```bash
   python manage.py migrate
   ```

7. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

8. Start the development server:
   ```bash
   python manage.py runserver
   ```

9. Visit:
   - Problems: http://localhost:8000/problems/
   - Learning: http://localhost:8000/learn/
   - Teacher Dashboard: http://localhost:8000/learn/teach/ (staff only)
   - Admin: http://localhost:8000/admin/

---

## Planned Next Steps

### Recently Completed
- ✅ Problem submission interface
- ✅ Code execution via subprocess
- ✅ Test case evaluation engine
- ✅ Submission results with detailed feedback
- ✅ User authentication with email verification
- ✅ Leaderboard and user statistics
- ✅ Rate limiting
- ✅ Docker sandbox for secure code execution
- ✅ Function-call (LeetCode-style) judge mode
- ✅ **Lessons system with markdown editor**
- ✅ **Teacher dashboard for content management**
- ✅ **Image upload support for lessons**

### Next Up
- [ ] Learner progress tracking (mark lessons as complete)
- [ ] Course completion certificates
- [ ] Code syntax highlighting in lessons
- [ ] Search functionality

### Future
- [ ] Async execution queue (Celery)
- [ ] Discussion forums
- [ ] Hints system for problems
- [ ] Video embeds in lessons

---

## License

This project is licensed under the **MIT License**.

---

## Notes

This repository reflects an **in-progress learning project**.  
Design decisions may evolve as new concepts are explored and refined.
