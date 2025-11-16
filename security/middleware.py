from django.http import JsonResponse
from rest_framework.status import HTTP_403_FORBIDDEN
from environment import ON_WAY_STUDY_API_KEY_SIGNARURE


class RequiredHeaderMiddleware:
    """
    Middleware that requires a specific header to be present on incoming requests.

    This middleware checks for the presence and correctness of the
    `X-On-Way-Study-Api-Signature` header. It is bypassed for admin URLs and OPTIONS requests.
    """

    def __init__(self, get_response):
        """
        Initializes the middleware.

        Args:
            get_response: The next middleware or view in the chain.
        """
        self.get_response = get_response
        self.header_name = "HTTP_X_ON_WAY_STUDY_API_SIGNATURE"
        self.expected_value = ON_WAY_STUDY_API_KEY_SIGNARURE

    def __call__(self, request):
        """
        Processes the incoming request.

        This method checks for the required header and validates its value.
        It bypasses the check for admin paths and OPTIONS requests.

        Args:
            request (HttpRequest): The incoming request.

        Returns:
            HttpResponse: The response from the next middleware or view.
        """
        if request.path.startswith("/admin/"):
            return self.get_response(request)

        if request.method == "OPTIONS":
            return self.get_response(request)

        self._validate_header_value(request.META.get(self.header_name, None))

        return self.get_response(request)

    def _validate_header_value(self, header_value: str):
        if header_value is None:
            return JsonResponse(
                {"error": "Missing header required API Signature"},
                status=HTTP_403_FORBIDDEN,
            )

        if header_value != self.expected_value:
            return JsonResponse(
                {"error": "Invalid header API Signature"}, status=HTTP_403_FORBIDDEN
            )
