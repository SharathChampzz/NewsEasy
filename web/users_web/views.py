from django.shortcuts import render

# Create your views here.
import logging
logger = logging.getLogger('web')

def login(request):
    logger.debug('Login page requested')
    return render(request, 'users_web/login.html')

def register(request):
    logger.info('Register page requested')
    return render(request, 'users_web/register.html')