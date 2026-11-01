class APITrailingSlashMiddleware:
    """
    Normalizes /api/... URLs to always end with a slash BEFORE URL resolution.

    This lets clients call either /api/v1/health or /api/v1/health/ and get
    the same response — without APPEND_SLASH's 500 error on POST/PUT/PATCH.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info
        if path.startswith("/api/") and not path.endswith("/"):
            request.path_info = path + "/"
            request.path = request.path + "/"
        return self.get_response(request)
