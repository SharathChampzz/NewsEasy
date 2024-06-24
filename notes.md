Celery has issues in task handler, So we will need a another pip module gvent

Start celery beat:
celery -A <module> beat -l info

Start Worker:
pip install gevent
celery -A <module> worker -l info -P gevent


