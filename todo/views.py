from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Todo
from django.db.models import Q


class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = 'todo/todo_list.html'
    context_object_name = 'todos'

    def get_queryset(self):
        return Todo.objects.filter(Q(created_by=self.request.user) | Q(assigned_to=self.request.user)).distinct()


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    fields = ['title', 'description', 'assigned_to']
    template_name = 'todo/todo_form.html'
    success_url = reverse_lazy('todo:todo_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TodoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Todo
    fields = ['title', 'description', 'assigned_to']
    template_name = 'todo/todo_form.html'
    success_url = reverse_lazy('todo:todo_list')

    def test_func(self):
        todo = self.get_object()
        return self.request.user == todo.created_by


class TodoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Todo
    template_name = 'todo/todo_confirm_delete.html'
    success_url = reverse_lazy('todo:todo_list')

    def test_func(self):
        todo = self.get_object()
        return self.request.user == todo.created_by