# Django + Celery: Installation & Configuration (with Redis)

## What Is Celery?

**Celery** is a powerful, production-ready asynchronous task queue.
It lets you run long or resource-intensive operations — such as sending emails, generating reports, or processing images — **in the background** instead of blocking user requests.

> Think of it as a way to **run Python functions asynchronously** outside your main Django thread.

---

## Why Use Celery with Django?

✅ Offload slow or CPU-heavy tasks
✅ Schedule recurring jobs (with **Celery Beat**)
✅ Retry failed jobs automatically
✅ Integrates well with brokers like **Redis** or **RabbitMQ**
✅ Scales horizontally across multiple workers

---

## Installation

Install Celery and Redis (as the message broker):

```bash
pip install celery redis
```

If you want periodic (scheduled) tasks:

```bash
pip install django-celery-beat
```

---

## Step 1. Configure Celery in Your Django Project

Inside your **main Django project folder** (where `settings.py` lives):

### Create `your_project_name/celery.py`

```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')

app = Celery('your_project_name')

# Load configuration from Django settings using the CELERY_ namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all installed Django apps
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
```

---

### Update `your_project_name/__init__.py`

This ensures Celery starts when Django starts.

```python
from .celery import app as celery_app

__all__ = ('celery_app',)
```

---

## Step 2. Configure Django Settings for Celery

In your **`settings.py`**, add:

```python
# Celery configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
```

If you use **Celery Beat** (optional):

```python
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
```

---

## Step 3. Create a Celery Task

In one of your Django apps (e.g. `application/tasks.py`):

```python
from celery import shared_task

@shared_task
def send_email_task(email):
    print(f"Sending email to {email}")
    # actual email sending logic here
```

---

## Step 4. Start Redis

If Redis isn’t already running, start it with Docker:

```bash
docker run -d --name redis -p 6379:6379 redis
```

Check that it’s active:

```bash
docker ps
```

---

## Step 5. Run Celery Worker

From your project root (same folder as `manage.py`):

```bash
celery -A your_project_name worker --loglevel=info
```

You should see output like:

```
[INFO/MainProcess] Connected to redis://localhost:6379/0
[INFO/MainProcess] celery@yourhost ready.
```

---

## Step 6. Run Celery Beat for Scheduled Tasks

(We will study the use of periodic tasks in detail in Lecture 22)

If you installed `django-celery-beat`:

1. Add `'django_celery_beat'` to `INSTALLED_APPS`
2. Run migrations:

   ```bash
   python manage.py migrate
   ```
3. Start the Beat scheduler:

   ```bash
   celery -A your_project_name beat --loglevel=info
   ```

Now you can define periodic tasks through the Django Admin.

---

## ✅ Summary

| Component         | Purpose                         | Example Command                                        |
| ----------------- | ------------------------------- | ------------------------------------------------------ |
| **Redis**         | Message broker & result backend | `docker run -d --name redis -p 6379:6379 redis`        |
| **Celery Worker** | Executes background tasks       | `celery -A your_project_name worker --loglevel=info` |
| **Celery Beat**   | Handles scheduled tasks         | `celery -A your_project_name beat --loglevel=info`   |

