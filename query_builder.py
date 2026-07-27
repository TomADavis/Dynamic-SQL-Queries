import os
from typing import Optional

from jinja2 import Environment, FileSystemLoader

from config import films, instacart
from filters import Bound, FilmFilters, InstacartFilters, Range

HERE = os.path.dirname(os.path.abspath(__file__))

env = Environment(
    loader=FileSystemLoader(os.path.join(HERE, "queries")),
    trim_blocks=True,
    lstrip_blocks=True
)

CONFIG_BY_FILTERS = {
    FilmFilters: films,
    InstacartFilters: instacart,
}


def _range_conditions(column: str, param_prefix: str, range_: Optional[Range]) -> tuple[list[str], dict]:
    if range_ is None:
        return [], {}

    is_equal = (
        range_.minimum is not None
        and range_.minimum == range_.maximum
        and range_.min_bound is Bound.INCLUSIVE
        and range_.max_bound is Bound.INCLUSIVE
    )
    if is_equal:
        return [f"{column} = :{param_prefix}"], {param_prefix: range_.minimum}

    conditions = []
    params = {}

    if range_.minimum is not None:
        op = ">=" if range_.min_bound is Bound.INCLUSIVE else ">"
        conditions.append(f"{column} {op} :{param_prefix}_min")
        params[f"{param_prefix}_min"] = range_.minimum

    if range_.maximum is not None:
        op = "<=" if range_.max_bound is Bound.INCLUSIVE else "<"
        conditions.append(f"{column} {op} :{param_prefix}_max")
        params[f"{param_prefix}_max"] = range_.maximum

    return conditions, params


def build(filters: FilmFilters | InstacartFilters) -> tuple[str, dict]:
    config = CONFIG_BY_FILTERS[type(filters)]

    conditions: list[str] = []
    params: dict = {}

    for field_name, column in config["columns"].items():
        field_conditions, field_params = _range_conditions(column, field_name, getattr(filters, field_name))
        conditions.extend(field_conditions)
        params.update(field_params)

    template = env.get_template(config["sql_file"])
    sql = template.render(FILTERS=" AND ".join(conditions))

    return sql, params
