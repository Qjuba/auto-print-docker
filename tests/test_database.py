from sqlalchemy import create_engine, inspect, text

from app import database


def test_migration_adds_crontab_expression_to_existing_database(tmp_path, monkeypatch):
    engine = create_engine(f"sqlite:///{tmp_path / 'legacy.db'}")
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                CREATE TABLE app_config (
                    id INTEGER PRIMARY KEY,
                    schedule_type VARCHAR(20) NOT NULL DEFAULT 'interval',
                    daily_time VARCHAR(5) NOT NULL DEFAULT '08:00',
                    monthly_day INTEGER NOT NULL DEFAULT 1,
                    time_of_day VARCHAR(5) NOT NULL DEFAULT '08:00',
                    days_of_month VARCHAR(100) NOT NULL DEFAULT '1'
                )
                """
            )
        )
        connection.execute(text("INSERT INTO app_config (id) VALUES (1)"))

    monkeypatch.setattr(database, "engine", engine)
    database.migrate_database()

    columns = {column["name"] for column in inspect(engine).get_columns("app_config")}
    assert "cron_expression" in columns
    with engine.connect() as connection:
        value = connection.scalar(text("SELECT cron_expression FROM app_config WHERE id = 1"))
    assert value == "0 8 * * *"
