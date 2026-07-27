from datetime import date

import pandas as pd
import streamlit as st

from filters import DateRange, FilmFilters, InstacartFilters
from main import run

st.set_page_config(page_title="Dynamic SQL Queries", layout="wide")
st.title("Dynamic SQL Queries")

TABS = {
    "Films": FilmFilters,
    "Instacart Orders": InstacartFilters,
}

tabs = st.tabs(list(TABS.keys()))

for tab, (label, filter_cls) in zip(tabs, TABS.items()):
    with tab:
        apply_filter = st.checkbox("Filter by date range", value=True, key=f"{label}_apply")

        col1, col2 = st.columns(2)
        start_date = col1.date_input(
            "Start date", value=date(2024, 3, 1), key=f"{label}_start", disabled=not apply_filter
        )
        end_date = col2.date_input(
            "End date", value=date(2024, 3, 31), key=f"{label}_end", disabled=not apply_filter
        )

        if st.button("Run query", key=f"{label}_run"):
            date_range = DateRange(minimum=start_date, maximum=end_date) if apply_filter else DateRange()
            filters = filter_cls(date_range=date_range)

            rendered_sql, _ = filters.build()
            with st.expander("Generated SQL"):
                st.code(rendered_sql, language="sql")

            try:
                columns, rows = run(filters=filters)
                df = pd.DataFrame(rows, columns=columns)
                st.dataframe(df, use_container_width=True)
                st.caption(f"{len(df)} row(s)")
            except Exception as exc:
                st.error(f"Query failed: {exc}")
