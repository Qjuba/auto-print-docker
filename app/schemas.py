from __future__ import annotations

import re
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import BaseModel, Field, field_validator, model_validator


class ScheduleRule(BaseModel):
    schedule_type: str
    interval_value: int = Field(default=60, ge=1, le=10080)
    interval_unit: str = "minutes"
    time_of_day: str = "08:00"
    days_of_week: list[int] = Field(default_factory=lambda: list(range(7)))
    days_of_month: list[int] = Field(default_factory=lambda: [1])
    last_day_of_month: bool = False
    timezone: str = Field(default="Europe/Warsaw", max_length=64)

    @field_validator("schedule_type")
    @classmethod
    def valid_type(cls, value: str) -> str:
        if value not in {"interval", "weekly", "monthly"}:
            raise ValueError("Nieobsługiwany rodzaj harmonogramu")
        return value

    @field_validator("interval_unit")
    @classmethod
    def valid_unit(cls, value: str) -> str:
        if value not in {"minutes", "hours", "days", "weeks"}:
            raise ValueError("Nieobsługiwana jednostka interwału")
        return value

    @field_validator("time_of_day")
    @classmethod
    def valid_time(cls, value: str) -> str:
        if not re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", value):
            raise ValueError("Godzina musi mieć format HH:MM")
        return value

    @field_validator("days_of_week")
    @classmethod
    def valid_days(cls, value: list[int]) -> list[int]:
        days = sorted(set(value))
        if any(day < 0 or day > 6 for day in days):
            raise ValueError("Nieprawidłowy dzień tygodnia")
        return days

    @field_validator("days_of_month")
    @classmethod
    def valid_month_days(cls, value: list[int]) -> list[int]:
        days = sorted(set(value))
        if any(day < 1 or day > 31 for day in days):
            raise ValueError("Nieprawidłowy dzień miesiąca")
        return days

    @field_validator("timezone")
    @classmethod
    def valid_timezone(cls, value: str) -> str:
        try:
            ZoneInfo(value)
        except ZoneInfoNotFoundError as exc:
            raise ValueError("Nieznana strefa czasowa") from exc
        return value

    @model_validator(mode="after")
    def validate_rule(self):
        if self.schedule_type == "weekly" and not self.days_of_week:
            raise ValueError("Wybierz co najmniej jeden dzień tygodnia")
        if self.schedule_type == "monthly" and not (self.days_of_month or self.last_day_of_month):
            raise ValueError("Wybierz co najmniej jeden dzień miesiąca")
        return self


class ScheduleUpdate(ScheduleRule):
    enabled: bool
    printer_name: str | None = Field(default=None, max_length=127)

    @model_validator(mode="after")
    def validate_enabled(self):
        if self.enabled and not self.printer_name:
            raise ValueError("Wybierz drukarkę przed włączeniem automatyzacji")
        return self


class AddPrinterRequest(BaseModel):
    name: str = Field(min_length=1, max_length=127, pattern=r"^[A-Za-z0-9._-]+$")
    uri: str = Field(min_length=5, max_length=500)
    location: str = Field(default="", max_length=127)

    @field_validator("uri")
    @classmethod
    def valid_uri(cls, value: str) -> str:
        if not value.lower().startswith(("ipp://", "ipps://")):
            raise ValueError("Dozwolone są wyłącznie adresy ipp:// i ipps://")
        if any(ch in value for ch in ("\n", "\r", "\x00")):
            raise ValueError("Nieprawidłowy adres drukarki")
        return value


class LoginRequest(BaseModel):
    username: str = Field(max_length=255)
    password: str = Field(max_length=1024)
