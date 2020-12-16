from .celery import app
from .models import User
from celery.utils.log import get_task_logger

logger = get_task_logger('myLogger')


@app.task
def null_balance():
	try:
		User.objects.all().update(current_balance=0)
		logger.info('Обнуляю баланс')
	except Exception as e:
		logger.error(e)



