from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.apps.api.views.generate import GenerateView, DownloadPDFAPIView


router = DefaultRouter()
router.register(r"generate", GenerateView, basename="generate")

urlpatterns = [
    path("", include(router.urls)),
    path("generate/<int:pk>/download/", DownloadPDFAPIView.as_view(), name="download")
]
