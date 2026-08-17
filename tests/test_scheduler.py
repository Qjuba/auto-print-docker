from datetime import datetime
from types import SimpleNamespace
from zoneinfo import ZoneInfo

from app.scheduler import preview_times


def config(**overrides):
    values = {
        "schedule_type": "weekly",
        "interval_value": 1,
        "interval_unit": "days",
        "time_of_day": "08:00",
        "days_of_week": [0],
        "days_of_month": [1],
        "last_day_of_month": False,
        "timezone": "Europe/Warsaw",
    }
    values.update(overrides)
    return SimpleNamespace(**values)


def test_monthly_preview_supports_multiple_days_and_last_day():
    timezone = ZoneInfo("Europe/Warsaw")
    now = datetime(2026, 1, 30, 12, 0, tzinfo=timezone)
    result = preview_times(
        config(
            schedule_type="monthly",
            days_of_month=[1, 15],
            last_day_of_month=True,
        ),
        count=4,
        now=now,
    )
    assert [(item.month, item.day, item.hour) for item in result] == [
        (1, 31, 8),
        (2, 1, 8),
        (2, 15, 8),
        (2, 28, 8),
    ]


def test_daily_interval_uses_selected_time_for_first_run():
    timezone = ZoneInfo("Europe/Warsaw")
    now = datetime(2026, 4, 3, 9, 0, tzinfo=timezone)
    result = preview_times(
        config(schedule_type="interval", interval_value=2, interval_unit="days"),
        count=2,
        now=now,
    )
    assert result == [
        datetime(2026, 4, 4, 8, 0, tzinfo=timezone),
        datetime(2026, 4, 6, 8, 0, tzinfo=timezone),
    ]
