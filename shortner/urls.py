from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import URLViews, RedirectToLongURLView

router = DefaultRouter()
router.register(
    prefix="shortner",
    viewset=URLViews,
    basename="shortner",
)

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path(
        "<str:short_code>/",
        RedirectToLongURLView.as_view(),
        name="redirect view",
    ),
]
