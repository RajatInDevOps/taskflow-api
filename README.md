# TaskFlow API

A small task tracker with a REST API, written in Flask.

## Running it

```bash
pip install -r requirements.txt
python app.py          # http://localhost:8000
```

## The API

| Method | Path                | What it does                  |
|--------|---------------------|-------------------------------|
| GET    | `/health`           | liveness, plus the task count |
| GET    | `/tasks`            | all tasks; `?status=open|done`|
| POST   | `/tasks`            | create one from `{"title":…}` |
| GET    | `/tasks/<id>`       | one task                      |
| POST   | `/tasks/<id>/done`  | mark it complete              |
| DELETE | `/tasks/<id>`       | remove it                     |

## Tests

```bash
pytest
```
