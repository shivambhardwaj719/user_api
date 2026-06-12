import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.api.deps import SessionLocal
from app.repositories.user_repo import user_repo

logger = logging.getLogger(__name__)

def log_total_activity():
    db = SessionLocal()
    try:
        active_users = user_repo.get_all(db, is_active=True)
        total_active = len(active_users)
        logger.info(f"End of day summary: Total active users = {total_active}")
        print(f"--- Scheduler Event: Total active users = {total_active} ---")
    except Exception as e:
        logger.error(f"Error executing scheduled task: {e}")
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        log_total_activity,
        trigger=CronTrigger(hour=23, minute=59),
        id="daily_activity_log",
        name="Log Total Active Users",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Background scheduler started.")
