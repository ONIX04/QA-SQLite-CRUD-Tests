"""Функціональні тести веб-інтерфейсу (маршрути Flask)."""
import database_connector as db

FORM = {"title": "Інтернат", "author": "Сергій Жадан", "genre": "Роман",
        "year": "2017", "pages": "336", "status": "не прочитана"}


def test_index_empty(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "Книг ще немає" in r.get_data(as_text=True)


def test_add_form_opens(client):
    assert client.get("/add").status_code == 200


def test_create_via_form_redirects_and_shows_row(client):
    r = client.post("/add", data=FORM)
    assert r.status_code == 302
    page = client.get("/").get_data(as_text=True)
    assert "Інтернат" in page and "Усього книг: 1" in page


def test_edit_form_prefilled(client, book):
    a = db.insert_item(book)
    page = client.get(f"/edit/{a}").get_data(as_text=True)
    assert 'value="Кобзар"' in page


def test_update_via_form(client, book):
    a = db.insert_item(book)
    client.post(f"/edit/{a}", data={**FORM, "status": "читаю"})
    assert db.get_item_by_id(a)["status"] == "читаю"


def test_edit_missing_returns_404(client):
    assert client.get("/edit/999").status_code == 404


def test_delete_via_post(client, book):
    a = db.insert_item(book)
    assert client.post(f"/delete/{a}").status_code == 302
    assert db.get_item_by_id(a) is None


def test_delete_by_get_not_allowed(client, book):
    a = db.insert_item(book)
    assert client.get(f"/delete/{a}").status_code == 405
    assert db.get_item_by_id(a) is not None


def test_html_is_escaped(client):
    client.post("/add", data={**FORM, "title": "<script>alert(1)</script>"})
    page = client.get("/").get_data(as_text=True)
    assert "<script>alert(1)</script>" not in page
    assert "&lt;script&gt;" in page


def test_non_numeric_year_saved_as_empty(client):
    client.post("/add", data={**FORM, "year": "abc"})
    assert db.get_all_items()[0]["year"] is None
