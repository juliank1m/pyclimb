# PyClimb Deployment Guide

This guide covers deploying PyClimb to a production environment.

## Quick Deploy to Railway

Railway is the recommended platform for quick deployment.

### 1. Prerequisites

- A [Railway](https://railway.app) account
- Git repository with your code

### 2. Deploy Steps

1. **Create a new project** on Railway and connect your GitHub repository.

2. **Add a PostgreSQL database** from the Railway dashboard:
   - Click "New" → "Database" → "PostgreSQL"
   - Railway will automatically set `DATABASE_URL`

3. **Configure environment variables** in your Railway service settings:

   | Variable | Value |
   |----------|-------|
   | `SECRET_KEY` | Generate with: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
   | `DEBUG` | `false` |
   | `ALLOWED_HOSTS` | Your custom domain (optional, Railway domain is auto-configured) |

4. **Deploy** - Railway will automatically:
   - Detect the Django project
   - Install dependencies from `requirements.txt`
   - Run migrations (via `Procfile` release command)
   - Start gunicorn

5. **Create a superuser** (one-time setup):
   ```bash
   # In Railway shell or via railway CLI
   railway run python manage.py createsuperuser
   ```

### 3. Custom Domain (Optional)

1. Go to Settings → Domains in your Railway service
2. Add your custom domain
3. Update DNS records as instructed
4. Add the domain to `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` env vars

### Railway Notes

- Static files are served via WhiteNoise (no nginx required)
- `DATABASE_URL` is automatically provided when you add PostgreSQL
- `RAILWAY_PUBLIC_DOMAIN` is set automatically for ALLOWED_HOSTS
- The `release` command in `Procfile` runs migrations on each deploy

---

## Traditional Server Deployment

For deploying to a VPS or dedicated server.

## Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Docker (if using sandboxed code execution)
- A Linux server (Ubuntu 22.04+ recommended)

## Environment Variables

Create a `.env` file or set these environment variables:

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key (generate a new one!) | `django-insecure-...` |
| `DEBUG` | Must be `false` in production | `false` |
| `ALLOWED_HOSTS` | Comma-separated list of domains | `pyclimb.example.com,www.pyclimb.example.com` |
| `DB_NAME` | PostgreSQL database name | `pyclimb` |
| `DB_USER` | PostgreSQL username | `pyclimb_user` |
| `DB_PASSWORD` | PostgreSQL password | `secure_password_here` |
| `DB_HOST` | PostgreSQL host | `localhost` |
| `DB_PORT` | PostgreSQL port | `5432` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_SSLMODE` | PostgreSQL SSL mode | `disable` |
| `PYCLIMB_USE_SANDBOX` | Enable Docker sandboxing | `false` |
| `PYCLIMB_REQUIRE_SANDBOX` | Refuse to run code without sandbox | `false` (auto-enabled when `DEBUG=false` if not explicitly set) |
| `PYCLIMB_SANDBOX_IMAGE` | Docker image for sandbox | `pyclimb-sandbox` |
| `PYCLIMB_SANDBOX_TIMEOUT` | Sandbox timeout (seconds) | `5` |
| `PYCLIMB_SANDBOX_MEMORY` | Sandbox memory limit | `128m` |
| `PYCLIMB_SANDBOX_CPUS` | Sandbox CPU limit | `0.5` |

### Email Configuration (for password reset)

| Variable | Description | Default |
|----------|-------------|---------|
| `EMAIL_HOST` | SMTP server hostname | `smtp.gmail.com` |
| `EMAIL_PORT` | SMTP port | `587` |
| `EMAIL_USE_TLS` | Use TLS | `true` |
| `EMAIL_HOST_USER` | SMTP username | - |
| `EMAIL_HOST_PASSWORD` | SMTP password or app password | - |
| `DEFAULT_FROM_EMAIL` | From address for emails | `noreply@pyclimb.local` |

## PostgreSQL Setup

1. Install PostgreSQL:
   ```bash
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   ```

2. Create database and user:
   ```bash
   sudo -u postgres psql
   ```
   ```sql
   CREATE DATABASE pyclimb;
   CREATE USER pyclimb_user WITH PASSWORD 'your_secure_password';
   GRANT ALL PRIVILEGES ON DATABASE pyclimb TO pyclimb_user;
   ALTER DATABASE pyclimb OWNER TO pyclimb_user;
   \q
   ```

3. For newer PostgreSQL (15+), also grant schema permissions:
   ```sql
   \c pyclimb
   GRANT ALL ON SCHEMA public TO pyclimb_user;
   ```

## Application Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pyclimb.git
   cd pyclimb
   ```

2. Create virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file with your configuration.

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Collect static files:
   ```bash
   python manage.py collectstatic --noinput
   ```

## Docker Sandbox Setup (Recommended for Production)

The sandbox provides secure, isolated code execution using Docker.

### 1. Build the sandbox image

```bash
cd sandbox
docker build -t pyclimb-sandbox .
```

### 2. Enable sandboxing

Set in your environment:
```bash
PYCLIMB_USE_SANDBOX=true
```

### 3. Verify Docker access

The web application user must be able to run Docker commands:
```bash
sudo usermod -aG docker www-data  # or your web server user
```

### Security Notes

- The sandbox runs with `--network none` (no network access)
- Memory is limited (default 128MB)
- CPU is limited (default 0.5 cores)
- Filesystem is read-only except for `/tmp`
- All Linux capabilities are dropped
- In production (`DEBUG=false`), the app refuses to run code without the sandbox unless `PYCLIMB_REQUIRE_SANDBOX` is explicitly disabled

**WARNING**: Without the sandbox enabled, code runs in a subprocess with minimal isolation. This is NOT safe for untrusted public users. See `SECURITY.md` for details.

## Running with Gunicorn

1. Install gunicorn (included in requirements.txt):
   ```bash
   pip install gunicorn
   ```

2. Run:
   ```bash
   gunicorn pyclimb.wsgi:application --bind 0.0.0.0:8000 --workers 3
   ```

### Systemd Service

Create `/etc/systemd/system/pyclimb.service`:

```ini
[Unit]
Description=PyClimb Gunicorn Daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/pyclimb
EnvironmentFile=/path/to/pyclimb/.env
ExecStart=/path/to/pyclimb/venv/bin/gunicorn pyclimb.wsgi:application --bind 127.0.0.1:8000 --workers 3

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable pyclimb
sudo systemctl start pyclimb
```

## Nginx Configuration

Example `/etc/nginx/sites-available/pyclimb`:

```nginx
server {
    listen 80;
    server_name pyclimb.example.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name pyclimb.example.com;
    
    # SSL configuration (use certbot for Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/pyclimb.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/pyclimb.example.com/privkey.pem;
    
    location /static/ {
        alias /path/to/pyclimb/staticfiles/;
        expires 30d;
    }
    
    location /media/ {
        alias /path/to/pyclimb/media/;
        expires 30d;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/pyclimb /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## SSL/HTTPS with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d pyclimb.example.com
```

## Static Files

For production, you need to configure static file serving:

1. Add to settings (already configured):
   ```python
   STATIC_ROOT = BASE_DIR / 'staticfiles'
   ```

2. Collect static files:
   ```bash
   python manage.py collectstatic
   ```

3. Serve via nginx (see nginx config above).

## Media Files (Lesson Images)

Lessons support image uploads. Configure media file serving:

1. Create media directory:
   ```bash
   mkdir -p /path/to/pyclimb/media/lessons
   chown www-data:www-data /path/to/pyclimb/media
   ```

2. Add to nginx configuration:
   ```nginx
   location /media/ {
       alias /path/to/pyclimb/media/;
       expires 30d;
   }
   ```

3. For production with cloud storage (recommended), configure Django Storages:
   ```bash
   pip install django-storages boto3  # For AWS S3
   ```
   
   Then update settings.py for your storage backend.

## Running Tests

```bash
# Install test dependencies
pip install pytest pytest-django

# Run tests
pytest

# Run with coverage
pip install pytest-cov
pytest --cov=submissions --cov=problems --cov=accounts --cov=lessons
```

## Lessons & Content Management

PyClimb includes a full content management system for learning materials.

### Teacher Dashboard

Staff users can access the teacher dashboard at `/learn/teach/` to:
- Create and edit courses and lessons
- Upload images for lesson content
- Preview lessons before publishing
- Toggle publish/draft status

### Creating Content

1. Log in as a staff user (superuser or user with `is_staff=True`)
2. Navigate to `/learn/teach/`
3. Click "New Course" or "New Lesson"
4. Use the rich markdown editor with toolbar for formatting
5. Preview content before publishing

### Markdown Features

The lesson editor supports:
- **Headings** (H1-H6)
- **Bold**, *italic*, ~~strikethrough~~
- Bullet and numbered lists
- Code blocks with syntax highlighting
- Links and images
- Blockquotes
- Tables

### Image Uploads

- Images are stored in `/media/lessons/`
- Maximum file size: 5MB
- Supported formats: JPEG, PNG, GIF, WebP
- Drag-and-drop upload supported

## Monitoring

### Check service status
```bash
sudo systemctl status pyclimb
sudo journalctl -u pyclimb -f
```

### Check nginx logs
```bash
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Sandbox health check
```bash
curl https://your-domain/health/sandbox/
```
Returns a JSON summary indicating whether sandboxing is enabled, required, and active (Docker available).

## Backup

### Database backup
```bash
pg_dump -U pyclimb_user pyclimb > backup_$(date +%Y%m%d).sql
```

### Restore from backup
```bash
psql -U pyclimb_user pyclimb < backup_20240115.sql
```

## Security Checklist

Before going live:

- [ ] `DEBUG=false` in production
- [ ] Strong `SECRET_KEY` (generate new one)
- [ ] `ALLOWED_HOSTS` configured correctly
- [ ] HTTPS enabled (SSL certificate)
- [ ] Database password is strong and unique
- [ ] Sandbox enabled (`PYCLIMB_USE_SANDBOX=true`)
- [ ] Sandbox required (`PYCLIMB_REQUIRE_SANDBOX=true` or rely on the default production behavior)
- [ ] Firewall configured (only 80, 443 open)
- [ ] Regular backups configured
- [ ] Rate limiting enabled (automatic when `DEBUG=false`)

## Limitations & Disclaimers

1. **Code Execution**: Even with sandboxing, running untrusted code carries risks. Monitor for abuse.

2. **Execution Time**: Displayed times are wall-clock time and include Docker overhead. They are approximate.

3. **Single Server**: This guide covers single-server deployment. For high availability, consider load balancing and database replication.

4. **Email Delivery**: Use a transactional email service (SendGrid, Mailgun, SES) for reliable delivery in production.

## Troubleshooting

### "Database connection refused"
- Check PostgreSQL is running: `sudo systemctl status postgresql`
- Verify connection settings in `.env`
- Check `pg_hba.conf` allows connections

### "Static files not loading"
- Run `python manage.py collectstatic`
- Check nginx `alias` path is correct
- Check file permissions

### "Docker sandbox not working"
- Verify Docker is installed: `docker --version`
- Check user is in docker group: `groups www-data`
- Check image exists: `docker images | grep pyclimb-sandbox`
- Check Docker socket permissions
 - If `DEBUG=false`, set `PYCLIMB_REQUIRE_SANDBOX=false` only temporarily to unblock local testing (not recommended for production)

### "Email not sending"
- In development, check console output for email
- Verify SMTP credentials
- Check spam folder
- Use app passwords for Gmail
