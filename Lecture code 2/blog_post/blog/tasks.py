from celery import shared_task

from blog.models import BlogPost


@shared_task
def send_email_task(email):
    print(f"Sending email to {email}")


@shared_task
def delete_inactive_blog_posts():
    blog_posts_count = BlogPost.objects.filter(is_active=False).count()
    BlogPost.objects.filter(is_active=False).update(deleted=True)

    print(f"Deleted {blog_posts_count} blog posts")


@shared_task
def reorder_blog_posts(sort_field: str, asc_des: str):
    if asc_des == 'des':
        sort_field = f'-{sort_field}'
    blog_posts = BlogPost.objects.order_by(sort_field)

    for index, blog_post in enumerate(blog_posts, start=1):
        blog_post.order = index
        blog_post.save(update_fields=['order'])

    print(f"reordered {blog_posts.count()} blog posts")
