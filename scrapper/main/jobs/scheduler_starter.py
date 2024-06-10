from apscheduler.schedulers.background import BackgroundScheduler

from main.jobs.scheduler import notify_bot_about_updates


def start():
    scheduler = BackgroundScheduler({
        'apscheduler.executors.processpool': {
            'type': 'processpool',
            'max_workers': '1'
        }
    })
    scheduler.add_job(notify_bot_about_updates, 'interval', seconds=300)
    scheduler.start()
