from app.tasks.celery_app import celery_app

@celery_app.task
def test_task():
    print("Тестовая задача выполнена")
    return "Hello from Celery"

