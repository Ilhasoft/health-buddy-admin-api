from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .forms import CustomUserCreationForm


class UserListView(LoginRequiredMixin, ListView):
    model = User
    paginate_by = 10
    template_name = "users/list_user.html"
    context_object_name = "users"


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/detail_user.html"
    context_object_name = "user"


class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = CustomUserCreationForm
    permission_required = ("auth.add_user",)
    template_name = "users/form_user.html"
    success_url = reverse_lazy("list_user")


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    fields = ["username", "first_name", "last_name", "email"]
    permission_required = ("auth.change_user",)
    template_name = "users/form_user.html"
    success_url = reverse_lazy("list_user")


class UserDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    http_method_names = ["post"]
    model = User
    permission_required = ("auth.delete_user",)
    success_url = reverse_lazy("list_user")


class UserAccessManagementView(UserDeleteView):
    def _revert_user_status(self):
        user = self.get_object()
        current_status = user.is_active
        user.is_active = not current_status
        user.save()

    def delete(self, request, *args, **kwargs):
        self._revert_user_status()
        return HttpResponseRedirect(self.success_url)
