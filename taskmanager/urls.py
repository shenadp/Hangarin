from django.urls import path
from . import views

urlpatterns = [

    # ── Tasks ──
    path('',
         views.TaskListView.as_view(),
         name='task-list'),

    path('tasks/add/',
         views.TaskCreateView.as_view(),
         name='task-add'),

    path('tasks/<int:pk>/',
         views.TaskDetailView.as_view(),
         name='task-view'),

    path('tasks/<int:pk>/edit/',
         views.TaskUpdateView.as_view(),
         name='task-edit'),

    path('tasks/<int:pk>/delete/',
         views.TaskDeleteView.as_view(),
         name='task-delete'),

    # ── Sub Tasks ──
    path('subtasks/',
         views.SubTaskListView.as_view(),
         name='subtask-list'),

    path('subtasks/add/',
         views.SubTaskCreateView.as_view(),
         name='subtask-add'),

    path('subtasks/<int:pk>/edit/',       # ← ADDED
         views.SubTaskUpdateView.as_view(),
         name='subtask-edit'),

    path('subtasks/<int:pk>/delete/',
         views.SubTaskDeleteView.as_view(),
         name='subtask-delete'),

    # ── Notes ──
    path('notes/',
         views.NoteListView.as_view(),
         name='note-list'),

    path('notes/add/',
         views.NoteCreateView.as_view(),
         name='note-add'),

    path('notes/<int:pk>/edit/',          # ← ADDED
         views.NoteUpdateView.as_view(),
         name='note-edit'),

    path('notes/<int:pk>/delete/',
         views.NoteDeleteView.as_view(),
         name='note-delete'),

    # ── Categories ──
    path('categories/',
         views.CategoryListView.as_view(),
         name='category-list'),

    path('categories/add/',
         views.CategoryCreateView.as_view(),
         name='category-add'),

    path('categories/<int:pk>/edit/',     # ← ADDED
         views.CategoryUpdateView.as_view(),
         name='category-edit'),

    path('categories/<int:pk>/delete/',
         views.CategoryDeleteView.as_view(),
         name='category-delete'),

    # ── Priorities ──
    path('priorities/',
         views.PriorityListView.as_view(),
         name='priority-list'),

    path('priorities/add/',
         views.PriorityCreateView.as_view(),
         name='priority-add'),

    path('priorities/<int:pk>/edit/',     # ← ADDED
         views.PriorityUpdateView.as_view(),
         name='priority-edit'),

    path('priorities/<int:pk>/delete/',
         views.PriorityDeleteView.as_view(),
         name='priority-delete'),
]