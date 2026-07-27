from sqlalchemy import create_engine

instacart = {
    "engine": create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/instacart"),
    "sql_file": "orders.sql",
}

films = {
    "engine": create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/films_db"),
    "sql_file": "films_db.sql"
}

