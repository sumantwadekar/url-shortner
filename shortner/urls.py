from django.urls import path, include
from rest_framework.routers import DefaultRouter
import debug_toolbar

from .views import URLViews, RedirectToLongURLView

router = DefaultRouter()
router.register(
    prefix="shortner",
    viewset=URLViews,
    basename="shortner",
)

urlpatterns = [
    path("", URLViews.as_view({"get": "home"}), name="home"),
    path("api/", include(router.urls)),  # Move API under /api/
    path(
        "<str:short_code>/", RedirectToLongURLView.as_view(), name="redirect view"
    ),  # Short URL redirect
    path("__debug__/", include(debug_toolbar.urls)),
]
