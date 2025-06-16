from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.apps.api.views.generate import GenerateView


router = DefaultRouter()
router.register(r"generate", GenerateView, basename="generate")

urlpatterns = [
    path("", include(router.urls)),
]
