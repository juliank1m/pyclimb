def submissions_enabled(request):
    """Expose submission availability to templates."""
    from django.conf import settings
    from submissions.services.runner import get_secure_execution_status

    enabled = getattr(settings, 'SUBMISSIONS_ENABLED', True)
    reason = ''
    secure_status = get_secure_execution_status()
    if enabled and secure_status['required'] and not secure_status['active']:
        enabled = False
        reason = secure_status['reason'] or (
            'Secure sandboxed execution is required for this deployment.'
        )

    return {
        'submissions_enabled': enabled,
        'submissions_disabled_reason': reason,
    }
