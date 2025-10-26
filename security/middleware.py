from django.http import JsonResponse
from rest_framework.status import HTTP_403_FORBIDDEN
from environment import ON_WAY_STUDY_API_KEY_SIGNARURE


class RequiredHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.header_name = "HTTP_X_ON_WAY_STUDY_API_SIGNATURE"
        self.expected_value = ON_WAY_STUDY_API_KEY_SIGNARURE

    def __call__(self, request):
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
