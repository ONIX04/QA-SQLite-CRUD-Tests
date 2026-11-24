# QA-SQLite-CRUD-Tests

Тестування веб-застосунку «Домашня бібліотека» ([SQLite-CRUD-Syniuk](https://github.com/ONIX04/SQLite-CRUD-Syniuk)): ручні тест-кейси, чек-лист, баг-репорти та автотести на pytest.

## Що всередині
- `docs/test-cases.md` — 16 тест-кейсів (позитивні, негативні, безпека, адаптивність)
- `docs/checklist.md` — чек-лист регресії
- `docs/bug-reports.md` — 5 знайдених дефектів (валідація, адаптивність)
- `tests/` — 26 автотестів: шар даних (DAL), маршрути Flask, валідація

Відомі дефекти позначені `xfail(strict=True)`: тест «падає очікувано», поки баг не виправлено, і стане червоним, щойно поведінка зміниться.

## Запуск
```
git clone https://github.com/ONIX04/SQLite-CRUD-Syniuk.git
git clone https://github.com/ONIX04/QA-SQLite-CRUD-Tests.git
cd QA-SQLite-CRUD-Tests
pip install -r requirements.txt
pytest
```
Шлях до застосунку можна змінити змінною середовища `APP_DIR`.

Результат: **21 passed, 5 xfailed**.
