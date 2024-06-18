from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler

from main.jobs.scheduler import notify_bot_about_updates


def start():
    # настройка количества потоков для выполнения регулярных задач
    executors = {
        'default': ThreadPoolExecutor(1),
        'processpool': ProcessPoolExecutor(1)
    }

    # настрока модуля для выполнения регулярных задач
    scheduler = BackgroundScheduler(executors=executors)
    scheduler.add_job(notify_bot_about_updates, 'interval', seconds=100)
    scheduler.start()
