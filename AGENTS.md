# AGENTS.md

## Layout
- Django project root is `canaco/` (not repo root); `manage.py` is there, project package is `canaco/canaco`, single app is `home`. Run `manage.py` commands from `canaco/`.
- `promp.md` is the source spec for Labs 11–13; its CRUD/detail/context-processor work is implemented in `home/views.py`, `home/urls.py`, templates and `home/context_processors.py`. `home/tests.py` is still empty.

## Environment / commands
- Use existing `canaco.venv` (Python 3.13, Django 6.1.1). `requirements.txt` is stale (Django 5.2 + mysqlclient) and differs from installed packages (PyMySQL/django-mysql); don't reinstall from it unless changing toolchain deliberately.
- MariaDB is required: `docker compose -f canaco/docker/compose.yaml up -d` from repo root. Settings use `localhost:3306`, `canaco_db`, hardcoded user/pass. `canaco/db.sqlite3` is tracked but unused.
- From `canaco/`: `../canaco.venv/bin/python manage.py check` and `../canaco.venv/bin/python manage.py test` (0 tests today; no lint/typecheck/CI config). `../canaco.venv/bin/python manage.py runserver` for manual checks.

## Gotchas
- `home/models.py` defines `Perfil` twice; the second class wins and emits a RuntimeWarning on every startup. The initial migration contains only one.
- `home/urls.py` has four `path("", ...)` entries and duplicate name `crear_usuario`; `reverse()` by name works, but `/` resolves to `home:index`.
- `home/signals.py` creates a `Perfil` on every `User` creation via `HomeConfig.ready()`; profile views still use `get_or_create` as a fallback.
- `es_operador`, `operador_required` and `guardar_archivo` live at the top of `home/views.py`; keep them there when extending the guide's views.
