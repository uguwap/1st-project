from app.tasks.celery_app import celery

@celery.task(queue="reminders")  # ⬅️ добавить queue
def test_task():
    print("Тестовая задача выполнена")
    return "Hello from Celery"
