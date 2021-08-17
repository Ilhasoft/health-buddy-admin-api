from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

from .fake_news.views import FakeNewsViewSet
from .posts.views import ImageCreateView
from .users.views import UserViewSet
from .articles.views import ArticleViewSet
from .rapidpro.views import FlowViewSet
from .videos.views import VideoViewSet
from .polls.views import PollViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Healthbuddy API",
        default_version="v1",
        description="An API to manage the contents of the website https://healthbuddy.info/",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# trailing_slash=False: should not contain "/" at the end of the url
router = routers.DefaultRouter(trailing_slash=False)
router.register(r"users", UserViewSet)
router.register(r"articles", ArticleViewSet)
router.register(r"fake-news", FakeNewsViewSet)
router.register(r"videos", VideoViewSet)
router.register(r"flows", FlowViewSet)
router.register(r"polls", PollViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("api/", include(router.urls)),
    path("api/password_reset/", include("django_rest_passwordreset.urls", namespace="password_reset")),
    path("upload/", ImageCreateView.as_view(), name="upload_image_post"),
    path("rapidpro/", include("healthbuddy_backend.rapidpro.urls"), name="rapidpro"),
    path("google_analytics/", include("healthbuddy_backend.google_analytics.urls"), name="google_analytics"),
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
