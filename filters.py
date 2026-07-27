import os
from dataclasses import dataclass
from typing import Optional, NamedTuple
from datetime import date
from jinja2 import Environment, FileSystemLoader, Template

from config import instacart, films

HERE = os.path.dirname(os.path.abspath(__file__))

env = Environment(
    loader=FileSystemLoader(os.path.join(HERE, "queries")),
    trim_blocks=True,
    lstrip_blocks=True
)

class DateRange(NamedTuple):
    minimum: Optional[date] = None
    maximum: Optional[date] = None

class PriceRange(NamedTuple):
    minimum: Optional[int | float] = None
    maximum: Optional[int | float] = None


@dataclass
class FilmFilters:
    date_range: Optional[DateRange] = None

    def build(self) -> tuple[str, dict[str, date | None]]:

        sql_file = films["sql_file"]

        context = {
            "start_date": self.date_range.minimum if self.date_range else None,
            "end_date": self.date_range.maximum if self.date_range else None,
        }

        template = env.get_template(sql_file)
        sql = template.render(**context)

        return sql, context

@dataclass
class InstacartFilters:
    date_range: Optional[DateRange]

    def build(self) -> tuple[str, dict[str, date | None]]:

        sql_file = instacart["sql_file"]

        context = {
            "start_date": self.date_range.minimum if self.date_range else None,
            "end_date": self.date_range.maximum if self.date_range else None,
        }

        template = env.get_template(sql_file)
        sql = template.render(**context)

        return sql, context