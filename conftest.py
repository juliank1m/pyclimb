"""
Pytest configuration for PyClimb tests.
"""
import os

# Configure Django settings before running tests
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pyclimb.settings')


def pytest_configure():
    """Configure Django for testing."""
    from django.conf import settings
    
    # Use SQLite for tests (faster, no external DB needed)
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'ATOMIC_REQUESTS': False,
        'AUTOCOMMIT': True,
        'CONN_MAX_AGE': 0,
        'CONN_HEALTH_CHECKS': False,
        'OPTIONS': {},
        'TIME_ZONE': None,
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'TEST': {
            'CHARSET': None,
            'COLLATION': None,
            'MIGRATE': True,
            'MIRROR': None,
            'NAME': None,
        },
    }
    # Disable rate limiting in tests
    settings.RATELIMIT_ENABLE = False
