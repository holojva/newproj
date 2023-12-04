from celery import shared_task
from celery.utils.log import get_task_logger
# from time import sleep

logger = get_task_logger(__name__)

def task_maker(text):
    print(f"task_maker: {text}")


@shared_task
def message_task(*args) :
    logger.info("message_task")
    task_maker(args)