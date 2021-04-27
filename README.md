# shortdiary

Shortdiary consists of two parts: A Python/Django-based backend that exposes a REST API, and a Vue/Nuxt.js frontend that consumes that API.

## Backend


```
poetry install
poetry run ./manage.py migrate
poetry run ./manage.py runserver
```

### Tasks

In production, the following tasks need to be scheduled in the Django-Q settings:

  * diary.tasks.process_mails_for_today: Once daily
  * diary.leaderboard.update_leaderboard: Every five minutes
  * diary.tasks.send_reminder_mails: Once daily
  * diary.tasks.send_active_users_overview: Once a week or so

## Frontend

```
yarn install
yarn dev
```

More details can be found in frontend/README.md
