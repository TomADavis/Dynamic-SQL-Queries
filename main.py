import sys
from datetime import date

sys.stdout.reconfigure(encoding="utf-8")

from sqlalchemy import text

from filters import FilmFilters, InstacartFilters, DateRange
from config import *


def run(filters:FilmFilters|InstacartFilters) -> None:

    rendered_sql, context = filters.build()

    engine = films["engine"] if isinstance(filters, FilmFilters) else instacart["engine"]

    with engine.connect() as connection:
        return connection.execute(text(rendered_sql), context).fetchall()


if __name__ == "__main__":

    mode = "instacart"

    if mode == "films":
        film_filters = FilmFilters(date_range=DateRange(minimum=date(2024, 3, 1), maximum=date(2024, 3, 31)))

        rows = run(filters=film_filters)

        for row in rows:
            print(row)

    elif mode == "instacart":
        instacart_filters = InstacartFilters(date_range=DateRange(minimum=date(2024, 3, 1), maximum=date(2024, 3, 31)))
        
        rows = run(filters=instacart_filters)
        
        for row in rows:
            print(row)