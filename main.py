import sys
from datetime import date

sys.stdout.reconfigure(encoding="utf-8")

from sqlalchemy import text

from filters import FilmFilters, InstacartFilters, DateRange
from config import films, instacart
from query_builder import build as build_query


def run(filters:FilmFilters|InstacartFilters) -> tuple[list[str], list]:

    rendered_sql, params = build_query(filters)

    engine = films["engine"] if isinstance(filters, FilmFilters) else instacart["engine"]

    with engine.connect() as connection:
        result = connection.execute(text(rendered_sql), params)
        return list(result.keys()), result.fetchall()


if __name__ == "__main__":

    mode = "instacart"

    if mode == "films":
        film_filters = FilmFilters(date_range=DateRange(minimum=date(2024, 3, 1), maximum=date(2024, 3, 31)))

        columns, rows = run(filters=film_filters)

        for row in rows:
            print(row)

    elif mode == "instacart":
        instacart_filters = InstacartFilters(date_range=DateRange(minimum=date(2024, 3, 1), maximum=date(2024, 3, 31)))

        columns, rows = run(filters=instacart_filters)

        for row in rows:
            print(row)