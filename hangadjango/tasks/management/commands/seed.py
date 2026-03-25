from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone
import random
from tasks.models import Task, SubTask, Note, Priority, Category

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        fake = Faker()

        # Add fixed priorities & categories

        priorities = ['High', 'Medium', 'Low', 'Critical', 'Optional']
        categories = ['Work', 'School', 'Personal', 'Finance', 'Projects']

        for p in priorities:
            Priority.objects.get_or_creare(name=p)
        for c in categories:
            Category.objects.get_or_create(name=c)

        # Generate tasks

        for _ in range(10):
            task = Task.objects.create(
                title=fake.sentence.(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                status=fake.random_element(elements=['Pending', 'In Progress', 'Completed']),
                priority=random.choice(Priority.objects.all()),
                category=random.choice(Category.objects.all()),
            )
        
        # Subtasks

        for _ in range(3):
            SubTask.objects.create(
                title=fake.sentence(nb_words=3),
                status=fake.random_element(elements=['Pending', 'In Progress', 'Completed']),
                parent_task=task,
            )

        # Notes

        Note.objects.create(task=task, content=fake.paragraph(nb_sentences=2))