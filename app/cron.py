from __future__ import annotations

import re
from zoneinfo import ZoneInfo

from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger


WEEKDAY_NAMES = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
WEEKDAY_NUMBERS = {name: index for index, name in enumerate(WEEKDAY_NAMES)}


def _validate_standard_field(field: str, label: str, allow_names: bool = False) -> None:
    pattern = r"[0-9A-Za-z*/,-]+" if allow_names else r"[0-9*/,-]+"
    if not re.fullmatch(pattern, field):
        raise ValueError(f"Pole „{label}” zawiera składnię nieobsługiwaną przez crontab")


def normalize_crontab(expression: str) -> str:
    fields = expression.split()
    if len(fields) != 5:
        raise ValueError("Wyrażenie crontab musi zawierać dokładnie 5 pól")
    normalized = " ".join(fields)
    # Building the trigger is also the authoritative syntax validation.
    build_crontab_trigger(normalized, ZoneInfo("UTC"))
    return normalized


def _weekday_number(value: str) -> int:
    lowered = value.lower()
    if lowered in WEEKDAY_NUMBERS:
        return WEEKDAY_NUMBERS[lowered]
    try:
        number = int(value)
    except ValueError as exc:
        raise ValueError(f"Nieprawidłowy dzień tygodnia: {value}") from exc
    if number == 7:
        return 0
    if number < 0 or number > 6:
        raise ValueError(f"Nieprawidłowy dzień tygodnia: {value}")
    return number


def _expand_weekday_part(part: str) -> set[int]:
    base, separator, raw_step = part.partition("/")
    if separator:
        try:
            step = int(raw_step)
        except ValueError as exc:
            raise ValueError("Krok dnia tygodnia musi być liczbą") from exc
        if step < 1:
            raise ValueError("Krok dnia tygodnia musi być większy od zera")
    else:
        step = 1

    if base == "*":
        values = list(range(7))
    elif "-" in base:
        start_raw, end_raw = base.split("-", 1)
        start = _weekday_number(start_raw)
        end = _weekday_number(end_raw)
        if end == 0 and start > 0 and end_raw.lower() in {"7", "sun"}:
            end = 7
        if start > end:
            raise ValueError("Zakres dni tygodnia nie może przechodzić przez koniec tygodnia")
        values = [number % 7 for number in range(start, end + 1)]
    else:
        start = _weekday_number(base)
        upper_bound = 8 if start > 0 else 7
        values = [number % 7 for number in range(start, upper_bound)] if separator else [start]
    return set(values[::step])


def normalize_weekdays(field: str) -> str:
    if not field:
        raise ValueError("Pole dnia tygodnia nie może być puste")
    selected: set[int] = set()
    for part in field.split(","):
        if not part:
            raise ValueError("Nieprawidłowa lista dni tygodnia")
        selected.update(_expand_weekday_part(part))
    if not selected:
        raise ValueError("Wybierz co najmniej jeden dzień tygodnia")
    if selected == set(range(7)):
        return "*"
    # APScheduler numbers weekdays from Monday; names avoid that mismatch.
    aps_order = [1, 2, 3, 4, 5, 6, 0]
    return ",".join(WEEKDAY_NAMES[number] for number in aps_order if number in selected)


def build_crontab_trigger(expression: str, timezone: ZoneInfo):
    fields = expression.split()
    if len(fields) != 5:
        raise ValueError("Wyrażenie crontab musi zawierać dokładnie 5 pól")
    minute, hour, day, month, weekday = fields
    _validate_standard_field(minute, "minuta")
    _validate_standard_field(hour, "godzina")
    _validate_standard_field(day, "dzień miesiąca")
    _validate_standard_field(month, "miesiąc", allow_names=True)
    normalized_weekday = normalize_weekdays(weekday)
    common = {"minute": minute, "hour": hour, "month": month, "timezone": timezone}

    # POSIX cron treats restricted day-of-month and day-of-week fields as OR.
    # APScheduler combines them with AND, so two triggers are required.
    if day != "*" and weekday != "*":
        return OrTrigger(
            [
                CronTrigger(day=day, day_of_week="*", **common),
                CronTrigger(day="*", day_of_week=normalized_weekday, **common),
            ]
        )
    return CronTrigger(day=day, day_of_week=normalized_weekday, **common)
