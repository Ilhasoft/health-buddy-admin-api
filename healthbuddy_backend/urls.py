from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include("healthbuddy_backend.dashboard.urls")),
    path("users/", include("healthbuddy_backend.users.urls")),
    path("publications/", include("healthbuddy_backend.publications.urls")),
    path("videos/", include("healthbuddy_backend.videos.urls")),
    path("api/", include("healthbuddy_backend.api.urls")),
]
