Celery has issues in task handler, So we will need a another pip module gvent

Start celery beat:
celery -A NewsEasy beat -l info

Start Worker:
pip install gevent
celery -A NewsEasy worker -l info -P gevent


