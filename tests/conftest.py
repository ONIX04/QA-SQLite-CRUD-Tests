"""Спільні фікстури: тестова база в тимчасовій папці та клієнт Flask."""
import os
import sys
import pytest

APP_DIR = os.environ.get("APP_DIR", os.path.join(os.path.dirname(__file__), "..", "..", "SQLite-CRUD-Syniuk"))
sys.path.insert(0, os.path.abspath(APP_DIR))

import database_connector as db  # noqa: E402
import app as app_module  # noqa: E402


@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    """Кожен тест працює з власною чистою базою, data.db застосунку не чіпається."""
    monkeypatch.setattr(db, "DB_NAME", str(tmp_path / "test.db"))
    db.create_db_table()
    yield


@pytest.fixture
def client():
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as c:
        yield c


@pytest.fixture
def book():
    return {"title": "Кобзар", "author": "Тарас Шевченко", "genre": "Поезія",
            "year": 1840, "pages": 114, "status": "прочитана"}
