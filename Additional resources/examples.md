## Step 1: Sample Django Model

### `models.py`

```python
from django.db import models

class Order(models.Model):
    customer_email = models.EmailField()
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

Run migrations after creating the model:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Task Example 1: Send Email Notification

### `tasks.py`

```python
from celery import shared_task
from django.core.mail import send_mail
from .models import Order

@shared_task
def send_order_confirmation_email(order_id):
    try:
        order = Order.objects.get(id=order_id)
        send_mail(
            subject="Order Confirmation",
            message=f"Your order with ID {order.id} has been received!",
            from_email="no-reply@example.com",
            recipient_list=[order.customer_email],
        )
        return f"Email sent to {order.customer_email}"
    except Order.DoesNotExist:
        return f"Order with ID {order_id} not found."
```

---

## Task Example 2: Auto-Close Old Orders

```python
from datetime import timedelta
from django.utils import timezone

@shared_task
def auto_close_old_orders():
    threshold = timezone.now() - timedelta(days=3)
    old_orders = Order.objects.filter(status='pending', created_at__lt=threshold)
    updated_count = old_orders.update(status='closed')
    return f"{updated_count} old orders marked as closed."
```

---

## How to Trigger

### Manually (in Django shell or view):

```python
send_order_confirmation_email.delay(order_id=1)
auto_close_old_orders.delay()
```

### Automatically (via Celery Beat):

You can schedule `auto_close_old_orders` to run daily.
