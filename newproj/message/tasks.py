from celery import shared_task
from celery.utils.log import get_task_logger
# from time import sleep

logger = get_task_logger(__name__)


@shared_task
def todo_notification(*args) :
    from message.views import bot_send_notification
    logger.info("initialized a notification for todo")
    print(args)
    bot_send_notification(args[0])
    