"""Перевірка валідації вхідних даних. Тести, що падають, відповідають знайденим дефектам (див. docs/bug-reports.md)."""
import pytest
import database_connector as db

FORM = {"title": "Інтернат", "author": "Сергій Жадан", "genre": "Роман",
        "year": "2017", "pages": "336", "status": "не прочитана"}


@pytest.mark.xfail(strict=True, reason="BUG-001 відкритий, див. docs/bug-reports.md")
def test_bug001_title_of_spaces_rejected(client):
    """BUG-001: назва з одних пробілів не повинна зберігатися."""
    client.post("/add", data={**FORM, "title": "   "})
    assert db.get_all_items() == [], "книга з порожньою назвою збережена"


@pytest.mark.xfail(strict=True, reason="BUG-002 відкритий, див. docs/bug-reports.md")
def test_bug002_year_in_future_rejected(client):
    """BUG-002: рік видання не може бути більшим за поточний."""
    client.post("/add", data={**FORM, "year": "3025"})
    assert db.get_all_items() == [], "книга з роком 3025 збережена"


@pytest.mark.xfail(strict=True, reason="BUG-003 відкритий, див. docs/bug-reports.md")
def test_bug003_zero_pages_rejected(client):
    """BUG-003: кількість сторінок має бути більшою за 0."""
    client.post("/add", data={**FORM, "pages": "0"})
    assert db.get_all_items() == [], "книга з 0 сторінок збережена"


@pytest.mark.xfail(strict=True, reason="BUG-004 відкритий, див. docs/bug-reports.md")
def test_bug004_unknown_status_rejected(client):
    """BUG-004: статус має бути одним із трьох допустимих значень."""
    client.post("/add", data={**FORM, "status": "загублена"})
    assert db.get_all_items() == [], "збережено недопустимий статус"


def test_missing_title_field_returns_400(client):
    data = dict(FORM)
    del data["title"]
    assert client.post("/add", data=data).status_code == 400


@pytest.mark.xfail(strict=True, reason="BUG-005 відкритий, див. docs/bug-reports.md")
def test_bug005_viewport_meta_present(client):
    """BUG-005: сторінка має містити meta viewport для мобільних пристроїв."""
    assert '<meta name="viewport"' in client.get("/").get_data(as_text=True)
