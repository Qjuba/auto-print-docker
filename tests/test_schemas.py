import pytest
from pydantic import ValidationError

from app.schemas import AddPrinterRequest, ScheduleUpdate


def test_schedule_accepts_weekly_days():
    model = ScheduleUpdate(
        enabled=False,
        schedule_type="weekly",
        time_of_day="07:45",
        days_of_week=[0, 2, 4],
        timezone="Europe/Warsaw",
    )
    assert model.days_of_week == [0, 2, 4]


@pytest.mark.parametrize("uri", ["http://printer/", "file:///etc/passwd", "ipp://host/print\n--evil"])
def test_printer_uri_rejects_unsafe_schemes(uri):
    with pytest.raises(ValidationError):
        AddPrinterRequest(name="safe-name", uri=uri)


def test_schedule_rejects_empty_days():
    with pytest.raises(ValidationError):
        ScheduleUpdate(enabled=False, schedule_type="weekly", days_of_week=[])


def test_schedule_accepts_days_and_weeks_as_intervals():
    daily = ScheduleUpdate(enabled=False, schedule_type="interval", interval_unit="days")
    weekly = ScheduleUpdate(enabled=False, schedule_type="interval", interval_unit="weeks")
    assert daily.interval_unit == "days"
    assert weekly.interval_unit == "weeks"


def test_schedule_accepts_multiple_monthly_days_and_last_day():
    model = ScheduleUpdate(
        enabled=False,
        schedule_type="monthly",
        days_of_month=[1, 15, 31],
        last_day_of_month=True,
        time_of_day="09:30",
        days_of_week=[],
    )
    assert model.days_of_month == [1, 15, 31]
    assert model.last_day_of_month is True


def test_schedule_rejects_monthly_rule_without_any_day():
    with pytest.raises(ValidationError):
        ScheduleUpdate(
            enabled=False,
            schedule_type="monthly",
            days_of_month=[],
            last_day_of_month=False,
        )
