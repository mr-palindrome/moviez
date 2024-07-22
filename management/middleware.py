import threading
from django.urls import reverse


class RequestCounterMiddleware:
    _lock = threading.Lock()
    _request_count = 0

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        excluded_paths = [
            reverse('request-count'),
            reverse('request-count-reset')
        ]

        if request.path not in excluded_paths:
            with self._lock:
                RequestCounterMiddleware._request_count += 1

        response = self.get_response(request)
        return response


    @classmethod
    def get_request_count(cls):
        """
        Get the current count of requests made.

        Args:
        cls: The class object.

        Returns:
        int: The count of requests made.
        """
        with cls._lock:
            return cls._request_count

    @classmethod
    def reset_request_count(cls):
        """
        Resets the request count to zero in a thread-safe manner.
        
        This method acquires a lock to ensure that the request count is reset
        without interference from other threads.
        """
        with cls._lock:
            cls._request_count = 0
