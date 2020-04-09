from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include("dashboard.urls")),
    path("users/", include("users.urls")),
    path("publications/", include("publications.urls")),
    path("videos/", include("videos.urls")),
    path("api/", include("api.urls")),
]
