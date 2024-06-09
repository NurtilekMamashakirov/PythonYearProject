from apscheduler.schedulers.background import BackgroundScheduler

from main.jobs.scheduler import notify_bot_about_updates


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(notify_bot_about_updates, 'interval', seconds=60)
    scheduler.start()
