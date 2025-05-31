# Django + Celery: Introduction, Installation & Configuration

## What Is Celery?

**Celery** is a powerful, production-ready asynchronous task queue. It's used for running time-consuming tasks like sending emails, processing images, or background calculations outside the main request/response cycle.

> Think of it as a way to **run Python functions in the background**.

---

## 🚀 Why Use Celery with Django?

* Offload slow tasks from the main app
* Schedule recurring jobs (with **Celery Beat**)
* Retry failed tasks automatically
* Scales well with message brokers like Redis or RabbitMQ

---

## 📦 Installation

Install Celery and a broker (we’ll use Redis):

```bash
pip install celery redis
```

If you want to use **Celery Beat** (for periodic tasks):

```bash
pip install django-celery-beat
```

---

## 🛠️ Configuring Celery in Django

### 1. Create `celery.py` in your main Django project folder (same as `settings.py`)

```python
# your_project/celery.py

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

app = Celery('your_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

### 2. Modify `__init__.py` (same folder as `settings.py`)

```python
# your_project/__init__.py

from .celery import app as celery_app

__all__ = ['celery_app']
```

---

## 🔧 Django Settings Configuration

```python
# settings.py

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
```

---

## 🗂️ Creating a Celery Task

In your Django app (e.g. `myapp/tasks.py`):

```python
from celery import shared_task

@shared_task
def send_email_task(email):
    print(f"Sending email to {email}")
```

---

## ▶️ Running Celery Worker

Start the Redis server:

```bash
redis-server
```

Start the Celery worker:

```bash
celery -A your_project worker --loglevel=info
```

---

## 🕒 Using Celery Beat (Scheduled Tasks)

1. Add `'django_celery_beat'` to `INSTALLED_APPS`
2. Run migrations:

```bash
python manage.py migrate
```

3. Add to `settings.py`:

```python
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
```

4. Start beat:

```bash
celery -A your_project beat --loglevel=info
```

Now you can define periodic tasks in the Django admin via `django-celery-beat`.
