from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
import json

from .models import Task, SubTask, Note, Category, Priority




class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()

        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q)
            )

        status = self.request.GET.get('status', '')
        if status:
            qs = qs.filter(status=status)

        category = self.request.GET.get('category', '')
        if category:
            qs = qs.filter(category__id=category)

        priority = self.request.GET.get('priority', '')
        if priority:
            qs = qs.filter(priority__id=priority)

        sort = self.request.GET.get('sort', '')
        allowed_sorts = ['deadline', '-deadline',
                         'title', '-title',
                         'status', 'priority']
        if sort in allowed_sorts:
            qs = qs.order_by(sort)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        today      = timezone.now().date()
        week_start = today - timezone.timedelta(days=today.weekday())
        week_end   = week_start + timezone.timedelta(days=6)

        ctx['total_tasks']     = Task.objects.count()
        ctx['tasks_today']     = Task.objects.filter(
                                     deadline__date=today
                                 ).count()
        ctx['tasks_this_week'] = Task.objects.filter(
                                     deadline__date__range=[week_start, week_end]
                                 ).count()
        ctx['completed_tasks'] = Task.objects.filter(
                                     status='Completed'
                                 ).count()
        ctx['categories']      = Category.objects.all()
        ctx['priorities']      = Priority.objects.all()

        # ── Chart data: tasks per day for last 7 days ──
        labels         = []
        pending_data   = []
        progress_data  = []
        completed_data = []

        for i in range(6, -1, -1):
            day = today - timezone.timedelta(days=i)
            labels.append(day.strftime('%b %d'))
            pending_data.append(
                Task.objects.filter(deadline__date=day, status='Pending').count()
            )
            progress_data.append(
                Task.objects.filter(deadline__date=day, status='In Progress').count()
            )
            completed_data.append(
                Task.objects.filter(deadline__date=day, status='Completed').count()
            )

        ctx['chart_labels']    = json.dumps(labels)
        ctx['chart_pending']   = json.dumps(pending_data)
        ctx['chart_progress']  = json.dumps(progress_data)
        ctx['chart_completed'] = json.dumps(completed_data)

        return ctx


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'task_form.html'
    fields = ['title', 'description', 'deadline', 'status', 'category', 'priority']
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        messages.success(self.request, 'Task created successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please fix the errors below.')
        return super().form_invalid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'task_form.html'
    fields = ['title', 'description', 'deadline', 'status', 'category', 'priority']
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        messages.success(self.request, 'Task updated successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please fix the errors below.')
        return super().form_invalid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        messages.success(self.request, 'Task deleted successfully.')
        return super().form_valid(form)


# ═══════════════════════════════════════════════════
# SUBTASK VIEWS
# ══════════════════════════════════════════════════

class SubTaskListView(LoginRequiredMixin, ListView):
    model = SubTask
    template_name = 'subtask_list.html'
    context_object_name = 'subtasks'
    paginate_by = 10

    def get_queryset(self):
        return SubTask.objects.filter(
            task__isnull=False
        ).select_related('task')


class SubTaskCreateView(LoginRequiredMixin, CreateView):
    model = SubTask
    template_name = 'task_form.html'
    fields = ['task', 'title', 'status']
    success_url = reverse_lazy('subtask-list')

    def get_initial(self):
        initial = super().get_initial()
        task_id = self.request.GET.get('task')
        if task_id:
            initial['task'] = task_id
        return initial

    def form_valid(self, form):
        messages.success(self.request, 'Subtask created successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please fix the errors below.')
        return super().form_invalid(form)


class SubTaskUpdateView(LoginRequiredMixin, UpdateView):
    model = SubTask
    template_name = 'task_form.html'
    fields = ['task', 'title', 'status']
    success_url = reverse_lazy('subtask-list')

    def form_valid(self, form):
        messages.success(self.request, 'Subtask updated successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please fix the errors below.')
        return super().form_invalid(form)


class SubTaskDeleteView(LoginRequiredMixin, DeleteView):
    model = SubTask
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('subtask-list')

    def form_valid(self, form):
        messages.success(self.request, 'Subtask deleted successfully.')
        return super().form_valid(form)


# ═══════════════════════════════════════════════════
# NOTE VIEWS
# ═══════════════════════════════════════════════════

class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'note_list.html'
    context_object_name = 'notes'
    paginate_by = 12


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    template_name = 'task_form.html'
    fields = ['task', 'content']
    success_url = reverse_lazy('note-list')

    def get_initial(self):
        initial = super().get_initial()
        task_id = self.request.GET.get('task')
        if task_id:
            initial['task'] = task_id
        return initial

    def form_valid(self, form):
        messages.success(self.request, 'Note added successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please fix the errors below.')
        return super().form_invalid(form)


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    template_name = 'task_form.html'
    fields = ['task', 'content']
    success_url = reverse_lazy('note-list')

    def form_valid(self, form):
        messages.success(self.request, 'Note updated successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please fix the errors below.')
        return super().form_invalid(form)


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('note-list')

    def form_valid(self, form):
        messages.success(self.request, 'Note deleted successfully.')
        return super().form_valid(form)


# ═══════════════════════════════════════════════════
# CATEGORY VIEWS
# ═══════════════════════════════════════════════════

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'task_form.html'
    fields = ['name']
    success_url = reverse_lazy('category-list')

    def form_valid(self, form):
        messages.success(self.request, 'Category added successfully!')
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = 'task_form.html'
    fields = ['name']
    success_url = reverse_lazy('category-list')

    def form_valid(self, form):
        messages.success(self.request, 'Category updated successfully!')
        return super().form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('category-list')

    def form_valid(self, form):
        messages.success(self.request, 'Category deleted successfully.')
        return super().form_valid(form)


# ═══════════════════════════════════════════════════
# PRIORITY VIEWS
# ═══════════════════════════════════════════════════

class PriorityListView(LoginRequiredMixin, ListView):
    model = Priority
    template_name = 'priority_list.html'
    context_object_name = 'priorities'


class PriorityCreateView(LoginRequiredMixin, CreateView):
    model = Priority
    template_name = 'task_form.html'
    fields = ['name']
    success_url = reverse_lazy('priority-list')

    def form_valid(self, form):
        messages.success(self.request, 'Priority added successfully!')
        return super().form_valid(form)


class PriorityUpdateView(LoginRequiredMixin, UpdateView):
    model = Priority
    template_name = 'task_form.html'
    fields = ['name']
    success_url = reverse_lazy('priority-list')

    def form_valid(self, form):
        messages.success(self.request, 'Priority updated successfully!')
        return super().form_valid(form)


class PriorityDeleteView(LoginRequiredMixin, DeleteView):
    model = Priority
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('priority-list')

    def form_valid(self, form):
        messages.success(self.request, 'Priority deleted successfully.')
        return super().form_valid(form)