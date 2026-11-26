# PR Review Demo

A tiny Django order API used in the **Dev Workflows** live call on pull requests and code review.

It is intentionally small so the whole diff of a pull request fits on one screen.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py test
python manage.py runserver
```

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/orders/<id>/` | Returns an order. Login required, owner only. |
| POST | `/api/orders/<id>/coupon/` | Applies a coupon code to an order. Body: `{"code": "WELCOME10"}` |

## Session material

The program for the live call is in [`docs/LIVE_CALL_PROGRAM.md`](docs/LIVE_CALL_PROGRAM.md).

How to install and use the AI pull request reviewer: [`docs/AI_REVIEWER.md`](docs/AI_REVIEWER.md).
