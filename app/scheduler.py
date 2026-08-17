from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Protocol
from zoneinfo import ZoneInfo

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from app.database import SessionLocal, engine
from app.models import ensure_config
from app.settings import settings

logger = logging.getLogger(__name__)
JOB_ID = "automatic-print"


class ScheduleConfig(Protocol):
    schedule_type: str
    interval_value: int
    interval_unit: str
    time_of_day: str
    days_of_week: str | list[int]
    days_of_month: str | list[int]
    last_day_of_month: bool
    timezone: str

scheduler = BackgroundScheduler(
    jobstores={"default": SQLAlchemyJobStore(engine=engine)},
    timezone=ZoneInfo(settings.timezone),
    job_defaults={"coalesce": True, "max_instances": 1, "misfire_grace_time": 300},
)


def _integer_list(value: str | list[int]) -> list[int]:
    if isinstance(value, str):
        return [int(item) for item in value.split(",") if item and item != "last"]
    return value


def _monthly_expression(config: ScheduleConfig) -> str:
    raw = config.days_of_month
    values = [str(day) for day in _integer_list(raw)]
    has_last = "last" in raw.split(",") if isinstance(raw, str) else config.last_day_of_month
    if has_last:
        values.append("last")
    return ",".join(values)


def build_trigger(config: ScheduleConfig, now: datetime | None = None):
    timezone = ZoneInfo(config.timezone)
    if config.schedule_type == "interval":
        kwargs = {config.interval_unit: config.interval_value, "timezone": timezone}
        if config.interval_unit in {"days", "weeks"}:
            current = (now or datetime.now(timezone)).astimezone(timezone)
            hour, minute = map(int, config.time_of_day.split(":"))
            start = current.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if start <= current:
                start += timedelta(days=1)
            kwargs["start_date"] = start
        return IntervalTrigger(**kwargs)
    hour, minute = map(int, config.time_of_day.split(":"))
    if config.schedule_type == "weekly":
        names = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        selected = _integer_list(config.days_of_week)
        return CronTrigger(
            day_of_week=",".join(names[index] for index in selected),
            hour=hour,
            minute=minute,
            timezone=timezone,
        )
    return CronTrigger(
        day=_monthly_expression(config),
        hour=hour,
        minute=minute,
        timezone=timezone,
    )


def preview_times(config: ScheduleConfig, count: int = 5, now: datetime | None = None) -> list[datetime]:
    trigger = build_trigger(config, now=now)
    current = now or datetime.now(ZoneInfo(config.timezone))
    previous = None
    result = []
    for _ in range(count):
        next_time = trigger.get_next_fire_time(previous, current)
        if next_time is None:
            break
        result.append(next_time)
        previous = next_time
        current = next_time
    return result


def sync_schedule(preserve_existing: bool = False) -> None:
    with SessionLocal() as session:
        config = ensure_config(session)
        session.commit()
        if not config.enabled:
            if scheduler.get_job(JOB_ID):
                scheduler.remove_job(JOB_ID)
            return
        if preserve_existing and scheduler.get_job(JOB_ID):
            logger.info("Przywrócono utrwalony termin automatycznego wydruku")
            return

        trigger = build_trigger(config)
        scheduler.add_job(
            "app.tasks:scheduled_print_job",
            trigger=trigger,
            id=JOB_ID,
            replace_existing=True,
            name="Automatyczny wydruk",
        )
        logger.info("Zaktualizowano harmonogram automatycznego drukowania")


def next_run_time() -> datetime | None:
    job = scheduler.get_job(JOB_ID) if scheduler.running else None
    return job.next_run_time if job else None


def start_scheduler() -> None:
    if not scheduler.running:
        scheduler.start()
    sync_schedule(preserve_existing=True)


def stop_scheduler() -> None:
    if scheduler.running:
        scheduler.shutdown(wait=False)
