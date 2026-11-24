"""Модульні тести шару доступу до даних (database_connector.py)."""
import pytest
import database_connector as db


def test_table_created_empty():
    assert db.get_all_items() == []


def test_insert_returns_id_and_saves_all_fields(book):
    new_id = db.insert_item(book)
    row = db.get_item_by_id(new_id)
    assert new_id == 1
    for key, value in book.items():
        assert row[key] == value


def test_ids_autoincrement(book):
    ids = [db.insert_item(book) for _ in range(3)]
    assert ids == [1, 2, 3]


def test_get_all_ordered_by_id(book):
    db.insert_item({**book, "title": "Б"})
    db.insert_item({**book, "title": "А"})
    assert [r["title"] for r in db.get_all_items()] == ["Б", "А"]


def test_get_missing_id_returns_none():
    assert db.get_item_by_id(999) is None


def test_update_changes_only_target_row(book):
    a = db.insert_item(book)
    b = db.insert_item({**book, "title": "Тигролови"})
    db.update_item(a, {**book, "status": "читаю"})
    assert db.get_item_by_id(a)["status"] == "читаю"
    assert db.get_item_by_id(b)["title"] == "Тигролови"


def test_delete_removes_row(book):
    a = db.insert_item(book)
    db.delete_item(a)
    assert db.get_item_by_id(a) is None
    assert db.get_all_items() == []


def test_sql_injection_is_stored_as_text(book):
    evil = "x'); DROP TABLE books; --"
    a = db.insert_item({**book, "title": evil})
    assert db.get_item_by_id(a)["title"] == evil
    assert len(db.get_all_items()) == 1


@pytest.mark.parametrize("missing", ["title", "author"])
def test_not_null_fields_reject_none(book, missing):
    with pytest.raises(Exception):
        db.insert_item({**book, missing: None})
