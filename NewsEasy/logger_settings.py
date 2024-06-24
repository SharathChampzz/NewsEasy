from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
import os

"""
DEBUG: Detailed information, typically of interest only when diagnosing problems.
INFO: Confirmation that things are working as expected.
WARNING: An indication that something unexpected happened or indicative of some problem in the near future (e.g., ‘disk space low’). The software is still working as expected.
ERROR: Due to a more serious problem, the software has not been able to perform some function.
CRITICAL: A very serious error, indicating that the program itself may be unable to continue running.
"""

# Note: Setting 'DEBUG' will log all the messages. Setting 'CRITICAL' will log only the critical messages. DEBUG < INFO < WARNING < ERROR < CRITICAL

log_level = os.getenv('DJANGO_LOG_LEVEL', 'DEBUG')
log_files_directory = os.path.join(BASE_DIR, 'Log Files')

# Create the "Log Files" directory if it doesn't exist
if not os.path.exists(log_files_directory):
    os.makedirs(log_files_directory)

logging_settings = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'advanced': {
            'format': '{levelname} {asctime} {module} {filename}:{lineno} {funcName} {message}',
            'style': '{',
        },
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'django': {
            'level': log_level,
            'class': 'logging.FileHandler',
            'filename': os.path.join(log_files_directory, 'Django.log'),  # Ensure BASE_DIR is defined
            'formatter': 'advanced',
        },
        'backend': {
            'level': log_level,
            'class': 'logging.FileHandler',
            'filename': os.path.join(log_files_directory, 'WebServer.log'),
            'formatter': 'advanced',
        },
        'web': {
            'level': log_level,
            'class': 'logging.FileHandler',
            'filename': os.path.join(log_files_directory, 'UI.log'),
            'formatter': 'advanced',
        },
        'scheduler': {
            'level': log_level,
            'class': 'logging.FileHandler',
            'filename': os.path.join(log_files_directory, 'Scheduler.log'),
            'formatter': 'advanced',
        },
        # Add any new file handlers here - To create a new log file
    },
    'root': {
        'handlers': ['django'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['django'],
            'level': log_level,
            'propagate': True,
        },
        'webserver': {
            'handlers': ['backend'],
            'level': log_level,
            'propagate': True,
        },
        'web': {
            'handlers': ['web'],
            'level': log_level,
            'propagate': True,
        },
        'scheduler': {
            'handlers': ['scheduler'],
            'level': log_level,
            'propagate': True,
        },
        # Add any new loggers here and assign the appropriate handler to log the messages to the respective log file
    },
}
