"""Birthday service: find contacts with birthdays within a given number of days."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from enum import Enum
from typing import Any

from models.contact import Record

DATE_OUTPUT_FORMAT = "%d.%m.%Y"
WEEKDAY_OUTPUT_FORMAT = "%A"
WEEKEND_SHIFTS = {5: 2, 6: 1}  # Saturday: +2 days, Sunday: +1 day
WEEKEND_NAMES = {5: "Saturday", 6: "Sunday"}


class JubileeType(Enum):
    """Enum for jubilee types."""

    NONE = ""
    REGULAR = "jubilee"
    BIG = "big jubilee"


@dataclass
class BirthdayRecord:
    """Birthday record with useful methods."""

    actual_birthday: date
    contact: Record
    original_birth_date: date

    @property
    def congratulation_date(self) -> date:
        """Get congratulation date (shifted to Monday if weekend)."""
        shift_days = WEEKEND_SHIFTS.get(self.actual_birthday.weekday(), 0)
        return self.actual_birthday + timedelta(days=shift_days)

    @property
    def is_shifted(self) -> bool:
        """Check if date was shifted to Monday."""
        return self.congratulation_date != self.actual_birthday

    @property
    def shift_reason(self) -> str:
        """Get weekend day name if shifted."""
        return (
            WEEKEND_NAMES.get(self.actual_birthday.weekday(), "")
            if self.is_shifted
            else ""
        )

    @property
    def age(self) -> int:
        """Calculate age in years."""
        return self.actual_birthday.year - self.original_birth_date.year

    @property
    def jubilee_type(self) -> str:
        """Get jubilee type."""
        if self.age <= 0:
            return JubileeType.NONE.value
        if self.age % 10 == 0:
            return JubileeType.BIG.value
        if self.age % 5 == 0:
            return JubileeType.REGULAR.value
        return JubileeType.NONE.value

    def __lt__(self, other: BirthdayRecord) -> bool:
        """Compare records by congratulation date and name."""
        if self.congratulation_date != other.congratulation_date:
            return self.congratulation_date < other.congratulation_date
        return self.contact.name.value.lower() < other.contact.name.value.lower()


class BirthdayService:
    """Service to find contacts with birthdays within a specified number of days."""

    def __init__(self, repository) -> None:
        """Initialize with a contact repository."""
        self._repository = repository

    def find_near(self, days: int) -> list[dict[str, Any]]:
        """Find contacts with birthdays within the specified number of days."""
        if days < 0:
            raise ValueError("Parameter 'days' must be non-negative.")

        records = self._collect_records(days)
        return [self._format_record(record) for record in sorted(records)]

    def find_on_date(self, target_date: str | date) -> list[dict[str, Any]]:
        """Find contacts with birthdays on a specific date (ignoring year)."""
        # Parse target date if it's a string
        if isinstance(target_date, str):
            try:
                target_date = datetime.strptime(target_date, "%d.%m.%Y").date()
            except ValueError:
                raise ValueError(
                    f"Invalid date format: {target_date}. Expected format: DD.MM.YYYY"
                )

        records = []
        today = date.today()

        for contact in self._repository.get_all_contacts():
            if not contact.birthday:
                continue

            try:
                birth_date = self._extract_date(contact.birthday)

                # Check if day and month match (ignoring year)
                if (
                    birth_date.day == target_date.day
                    and birth_date.month == target_date.month
                ):
                    # Calculate the birthday in the current year or next year
                    birthday_this_year = self._get_next_birthday(birth_date, today)

                    records.append(
                        BirthdayRecord(
                            actual_birthday=birthday_this_year,
                            contact=contact,
                            original_birth_date=birth_date,
                        )
                    )
            except (TypeError, ValueError):
                continue

        # Sort by name
        records.sort(key=lambda r: r.contact.name.value.lower())
        return [self._format_record(record) for record in records]

    def find_today(self) -> list[dict[str, Any]]:
        """Find contacts with birthdays today."""
        return self.find_on_date(date.today())

    def _collect_records(self, days: int) -> list[BirthdayRecord]:
        """Collect contacts whose birthdays fall within the specified days."""
        records = []
        today = date.today()

        for contact in self._repository.get_all_contacts():
            if not contact.birthday:
                continue

            try:
                birth_date = self._extract_date(contact.birthday)
                birthday_this_year = self._get_next_birthday(birth_date, today)

                if 0 <= (birthday_this_year - today).days <= days:
                    records.append(
                        BirthdayRecord(
                            actual_birthday=birthday_this_year,
                            contact=contact,
                            original_birth_date=birth_date,
                        )
                    )
            except (TypeError, ValueError):
                continue

        return records

    def _get_next_birthday(self, birth_date: date, today: date) -> date:
        """Get next birthday date (this year or next year)."""
        birthday = self._replace_year(birth_date, today.year)
        if birthday < today:
            birthday = self._replace_year(birth_date, today.year + 1)
        return birthday

    @staticmethod
    def _replace_year(birth_date: date, year: int) -> date:
        """Replace year in date (handle Feb 29 in non-leap years)."""
        try:
            return birth_date.replace(year=year)
        except ValueError:
            return birth_date.replace(year=year, day=28)

    @staticmethod
    def _extract_date(birthday_obj: Any) -> date:
        """Extract date from Birthday object."""
        if not birthday_obj:
            raise TypeError("Birthday value is missing.")

        if hasattr(birthday_obj, "value"):
            value = birthday_obj.value
            return value.date() if isinstance(value, datetime) else value

        raise TypeError(f"Invalid birthday type: {type(birthday_obj)!r}")

    @staticmethod
    def _format_record(record: BirthdayRecord) -> dict[str, Any]:
        """Format a single birthday record into a dictionary."""
        phones = [p.value for p in record.contact.phones]
        emails = [e.value for e in record.contact.emails]

        return {
            "date": record.congratulation_date.strftime(DATE_OUTPUT_FORMAT),
            "weekday": record.congratulation_date.strftime(WEEKDAY_OUTPUT_FORMAT),
            "actual_birthday_date": record.actual_birthday.strftime(DATE_OUTPUT_FORMAT),
            "actual_birthday_weekday": record.actual_birthday.strftime(
                WEEKDAY_OUTPUT_FORMAT
            ),
            "is_shifted": record.is_shifted,
            "shift_reason": record.shift_reason,
            "name": record.contact.name.value,
            "age": record.age,
            "is_jubilee": bool(record.jubilee_type),
            "jubilee_type": record.jubilee_type,
            "phone": next(iter(phones), ""),
            "email": next(iter(emails), ""),
            "phones": phones,
            "emails": emails,
        }
