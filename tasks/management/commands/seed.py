from django.core.management.base import BaseCommand
from tasks.models import Task, SubTask, Note, Priority, Category
from faker import Faker
from django.utils import timezone
import random

class Command(BaseCommand):
    help = "Seed database with fake data"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # ===========================
        # Create default priorities if empty
        # ===========================
        if not Priority.objects.exists():
            for name in ["High", "Medium", "Low", "Critical", "Optional"]:
                Priority.objects.create(name=name)

        # ===========================
        # Create default categories if empty
        # ===========================
        if not Category.objects.exists():
            for name in ["Work", "School", "Personal", "Finance", "Projects"]:
                Category.objects.create(name=name)

        # ===========================
        # Get lists of all priorities and categories
        # ===========================
        priorities = list(Priority.objects.all())
        categories = list(Category.objects.all())

        # ===========================
        # Create 20 tasks with subtasks and notes
        # ===========================
        for _ in range(20):
            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                priority=random.choice(priorities),
                category=random.choice(categories)
            )

            # 3 subtasks per task
            for _ in range(3):
                SubTask.objects.create(
                    title=fake.sentence(nb_words=4),
                    status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                    task=task
                )

            # 2 notes per task
            for _ in range(2):
                Note.objects.create(
                    task=task,
                    content=fake.paragraph(nb_sentences=2)
                )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
