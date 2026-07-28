from datetime import date

import pandas as pd
import streamlit as st

from filters import Bound, DateRange, FilmFilters, InstacartFilters
from main import run
from utils import build_query

st.set_page_config(page_title="Dynamic SQL Queries", layout="wide")
st.title("Dynamic SQL Queries")

TABS = {
    "Films": FilmFilters,
    "Instacart Orders": InstacartFilters,
}

BOUND_OPTIONS = {
    "≤": Bound.INCLUSIVE,
    "<": Bound.EXCLUSIVE,
}

tabs = st.tabs(list(TABS.keys()))

for tab, (label, filter_cls) in zip(tabs, TABS.items()):
    with tab:
        apply_filter = st.checkbox("Filter by date range", value=True, key=f"{label}_apply")
        exact_match = st.checkbox(
            "Match an exact date", value=False, key=f"{label}_exact_toggle", disabled=not apply_filter
        )

        if exact_match:
            exact_date = st.date_input(
                "Date", value=date(2024, 3, 1), key=f"{label}_exact", disabled=not apply_filter
            )
        else:
            col1, col2, col3, col4 = st.columns(4)
            start_date = col1.date_input(
                "Start date", value=date(2024, 3, 1), key=f"{label}_start", disabled=not apply_filter
            )
            min_bound = col2.selectbox(
                "Start bound", list(BOUND_OPTIONS), key=f"{label}_min_bound", disabled=not apply_filter
            )
            max_bound = col3.selectbox(
                "End bound", list(BOUND_OPTIONS), key=f"{label}_max_bound", disabled=not apply_filter
            )
            end_date = col4.date_input(
                "End date", value=date(2024, 3, 31), key=f"{label}_end", disabled=not apply_filter
            )

        if st.button("Run query", key=f"{label}_run"):
            if not apply_filter:
                date_range = DateRange()
            elif exact_match:
                date_range = DateRange.equal_to(exact_date)
            else:
                date_range = DateRange(
                    minimum=start_date,
                    maximum=end_date,
                    min_bound=BOUND_OPTIONS[min_bound],
                    max_bound=BOUND_OPTIONS[max_bound],
                )
            filters = filter_cls(date_range=date_range)

            rendered_sql, params = build_query(filters)
            with st.expander("Generated SQL"):
                st.code(rendered_sql, language="sql")

            try:
                columns, rows = run(filters=filters)
                df = pd.DataFrame(rows, columns=columns)
                st.dataframe(df, use_container_width=True)
                st.caption(f"{len(df)} row(s)")
            except Exception as exc:
                st.error(f"Query failed: {exc}")
