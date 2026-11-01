from .dev import *  # noqa: F401,F403

# --- Test-only overrides ---

# Use in-memory cache so throttle state doesn't persist across test runs
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "test-cache",
    }
}

# Disable rate limiting in tests (we test the logic, not the counter)
REST_FRAMEWORK = {
    **REST_FRAMEWORK,
    "DEFAULT_THROTTLE_RATES": {
        "auth": "10000/min",
        "invitation": "10000/hour",
        "oauth": "10000/min",
    },
}

# Fast password hashing for tests only
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# Speed up tests
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
