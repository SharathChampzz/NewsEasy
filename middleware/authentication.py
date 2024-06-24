from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse

import logging
logger = logging.getLogger('webserver')

class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if '/api/' not in request.path: # only check authentication for API requests
            return None
        excluded_paths = ['/api/users/login', '/api/users/logout', '/api/users/'] # add more paths to exclude from authentication
        if request.headers.get('SkipAuth', False) == 'true':
            return None
        if request.path in excluded_paths:
            return None
        
        print('Checking authentication...')
        auth = JWTAuthentication()
        header = auth.get_header(request)
        if header is None:
            logger.error('Token is missing in the header')
            return JsonResponse({'error': 'Token is missing in the header'}, status=401)
        
        raw_token = auth.get_raw_token(header)
        if raw_token is None:
            logger.error('Invalid token')
            return JsonResponse({'error': 'Invalid token'}, status=401)
        
        try:
            validated_token = auth.get_validated_token(raw_token)
        except Exception as e:
            logger.error(f'Invalid token: {str(e)}')
            return JsonResponse({'error': 'Invalid token'}, status=401)
        
        # If everything is fine, attach the user to the request
        request.user = auth.get_user(validated_token)
        return None

    def process_response(self, request, response):
        return response
