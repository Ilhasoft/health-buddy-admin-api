from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm


class UserListView(LoginRequiredMixin, ListView):
    model = User
    paginate_by = 10
    template_name = "users/list_user.html"
    context_object_name = "users"


class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = CustomUserCreationForm
    permission_required = ("auth.add_user",)
    template_name = "users/form_user.html"
    success_url = reverse_lazy("list_user")


class UserDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    http_method_names = ['post']
    model = User
    permission_required = ("auth.delete_user",)
    success_url = reverse_lazy("list_user")


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/detail_user.html"
    context_object_name = "user"


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    permission_required = ("auth.change_user",)
    fields = ["username", "first_name", "last_name", "email"]
    template_name = "users/form_user.html"
    success_url = reverse_lazy("list_user")
    #mandar no contexto o formulário de alterar senha


class UserPasswordChangeView(PasswordChangeView):
    http_method_names = ['post']
    #form_class = PasswordChangeForm
    permission_required = ("auth.change_user",)

    def get_success_url(self):
        return reverse_lazy("update_user", kwargs={'pk': self.kwargs['pk']})
