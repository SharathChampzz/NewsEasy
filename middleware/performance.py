import time
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('webserver')

class PerformanceMonitoringMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()
    
    def process_response(self, request, response):
        duration = time.time() - request.start_time
        logger.info(f'Performance: {request.method} {request.get_full_path()} took {duration:.2f}s')
        return response
