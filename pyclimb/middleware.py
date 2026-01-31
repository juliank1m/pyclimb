"""
Custom middleware for PyClimb.
"""

import time
from django.core.cache import cache
from django.http import HttpResponse
from django.conf import settings


class HttpResponseTooManyRequests(HttpResponse):
    """HTTP 429 Too Many Requests response."""
    status_code = 429


class RateLimitMiddleware:
    """
    Rate limiting middleware for submission endpoints.
    
    Limits:
    - Submissions: 10 per minute per user/IP
    - Registration: 5 per hour per IP
    
    Configure via settings:
    - RATELIMIT_ENABLE: Enable/disable rate limiting (default: True in production)
    - RATELIMIT_SUBMISSION_LIMIT: Max submissions per minute (default: 10)
    - RATELIMIT_REGISTER_LIMIT: Max registrations per hour (default: 5)
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.enabled = getattr(settings, 'RATELIMIT_ENABLE', not settings.DEBUG)
    
    def __call__(self, request):
        if not self.enabled:
            return self.get_response(request)
        
        # Check rate limits for specific paths
        path = request.path
        
        # Rate limit submissions
        if path.startswith('/submissions/create/') and request.method == 'POST':
            if not self._check_rate_limit(request, 'submission', 
                                          limit=getattr(settings, 'RATELIMIT_SUBMISSION_LIMIT', 10),
                                          window=60):
                return HttpResponseTooManyRequests(
                    "Rate limit exceeded. Please wait before submitting again.",
                    content_type="text/plain"
                )
        
        # Rate limit registration
        if path == '/accounts/register/' and request.method == 'POST':
            if not self._check_rate_limit(request, 'register',
                                          limit=getattr(settings, 'RATELIMIT_REGISTER_LIMIT', 5),
                                          window=3600):
                return HttpResponseTooManyRequests(
                    "Too many registration attempts. Please try again later.",
                    content_type="text/plain"
                )
        
        # Rate limit login attempts
        if path == '/accounts/login/' and request.method == 'POST':
            if not self._check_rate_limit(request, 'login',
                                          limit=getattr(settings, 'RATELIMIT_LOGIN_LIMIT', 10),
                                          window=300):
                return HttpResponseTooManyRequests(
                    "Too many login attempts. Please try again in a few minutes.",
                    content_type="text/plain"
                )
        
        return self.get_response(request)
    
    def _get_client_key(self, request):
        """Get a unique key for the client (user ID or IP)."""
        if request.user.is_authenticated:
            return f"user:{request.user.id}"
        
        # Get IP address (handle proxies)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', 'unknown')
        
        return f"ip:{ip}"
    
    def _check_rate_limit(self, request, action, limit, window):
        """
        Check if the request is within rate limits.
        
        Args:
            request: The HTTP request
            action: Name of the action being rate limited
            limit: Maximum number of requests allowed
            window: Time window in seconds
        
        Returns:
            True if within limits, False if exceeded
        """
        client_key = self._get_client_key(request)
        cache_key = f"ratelimit:{action}:{client_key}"
        
        # Get current count and timestamp
        data = cache.get(cache_key)
        now = time.time()
        
        if data is None:
            # First request in this window
            cache.set(cache_key, {'count': 1, 'start': now}, window)
            return True
        
        count = data['count']
        start = data['start']
        
        # Check if window has expired
        if now - start >= window:
            # Reset the window
            cache.set(cache_key, {'count': 1, 'start': now}, window)
            return True
        
        # Check if limit exceeded
        if count >= limit:
            return False
        
        # Increment count
        data['count'] = count + 1
        cache.set(cache_key, data, window - int(now - start))
        return True
