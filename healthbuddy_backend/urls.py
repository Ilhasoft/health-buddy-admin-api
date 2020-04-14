from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include("healthbuddy_backend.dashboard.urls")),
    path("users/", include("healthbuddy_backend.users.urls")),
    path("publications/", include("healthbuddy_backend.publications.urls")),
    path("videos/", include("healthbuddy_backend.videos.urls")),
    path("api/", include("healthbuddy_backend.api.urls")),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
