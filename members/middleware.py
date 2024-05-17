import logging
from django.http import Http404, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render

logger = logging.getLogger(__name__)

class ExceptionLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        logger.error(f'Exception occurred: {exception}', exc_info=True)
        
        if isinstance(exception, Http404):
            return render(request, '404.html', status=404)
        elif isinstance(exception, HttpResponseForbidden):
            return render(request, '403.html', status=403)
        elif isinstance(exception, HttpResponseBadRequest):
            return render(request, '400.html', status=400)
        else:
            return render(request, '500.html', status=500)
