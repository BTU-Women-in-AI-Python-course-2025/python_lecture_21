# Celery Tasks in Django: Defining Tasks & Using Arguments

## What Is a Celery Task?

A **Celery task** is simply a **Python function** you decorate with `@shared_task` or `@app.task`. Once defined, it can run **asynchronously** in the background.

---

## Basic Task Example

Create a `tasks.py` file inside your Django app (e.g. `myapp/tasks.py`):

```python
from celery import shared_task

@shared_task
def say_hello():
    print("Hello from Celery!")
```

To trigger it:

```python
say_hello.delay()
```

---

## 🧾 Task with Arguments

You can pass any number of arguments to a task using `.delay()` or `.apply_async()`.

```python
@shared_task
def greet_user(name):
    print(f"Hello, {name}!")
```

Usage:

```python
greet_user.delay("Mariam")
```

---

## 📦 Realistic Example

```python
@shared_task
def add_numbers(a, b):
    return a + b
```

Usage:

```python
add_numbers.delay(3, 7)  # Will return 10 asynchronously
```

---

## 🎯 Keyword Arguments

Celery also supports keyword arguments:

```python
@shared_task
def send_email(to, subject, body=None):
    print(f"To: {to}, Subject: {subject}, Body: {body}")
```

Usage:

```python
send_email.delay(to="user@example.com", subject="Welcome", body="Thanks for joining!")
```

---

## 🧰 Task Metadata

You can customize tasks with parameters:

```python
@shared_task(bind=True, max_retries=3)
def process_file(self, file_id):
    try:
        # your logic here
        pass
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)  # retry after 60 seconds
```
