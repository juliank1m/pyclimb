def submissions_enabled(request):
    """Expose submission availability to templates."""
    from django.conf import settings
    return {
        'submissions_enabled': getattr(settings, 'SUBMISSIONS_ENABLED', True)
    }
