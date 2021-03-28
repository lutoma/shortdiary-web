# shortdiary

```
poetry install
poetry run ./manage.py migrate
poetry run ./manage.py runserver
```

## Tasks

In production, the following tasks need to be scheduled in the Django-Q settings:

process_mails_for_today: Once daily
update_leaderboard: Every five minutes
send_reminder_mails: Once daily
send_active_users_overview: Once a week or so
