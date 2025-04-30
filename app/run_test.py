from app.tasks.test import test_task

test_task.delay()
print("Задача отправлена")

