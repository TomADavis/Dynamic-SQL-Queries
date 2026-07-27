from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional
from datetime import date


class Bound(Enum):
    INCLUSIVE = "inclusive"
    EXCLUSIVE = "exclusive"
    EQUAL = "equal"


@dataclass
class Range:
    minimum: Optional[Any] = None
    maximum: Optional[Any] = None
    bound: Bound = Bound.INCLUSIVE

    @classmethod
    def equal_to(cls, value: Any) -> "Range":
        return cls(minimum=value, bound=Bound.EQUAL)


@dataclass
class DateRange(Range):
    minimum: Optional[date] = None
    maximum: Optional[date] = None


@dataclass
class PriceRange(Range):
    minimum: Optional[int | float] = None
    maximum: Optional[int | float] = None


@dataclass
class FilmFilters:
    date_range: Optional[DateRange] = None


@dataclass
class InstacartFilters:
    date_range: Optional[DateRange] = None
