from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from core.apps.api.models import GenerateModel
from core.apps.api.serializers.generate import (
    CreateGenerateSerializer,
    ListGenerateSerializer,
    RetrieveGenerateSerializer,
)


@extend_schema(tags=["generate"])
class GenerateView(BaseViewSetMixin, ModelViewSet):
    queryset = GenerateModel.objects.all()
    serializer_class = ListGenerateSerializer
    permission_classes = [AllowAny]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListGenerateSerializer,
        "retrieve": RetrieveGenerateSerializer,
        "create": CreateGenerateSerializer,
    }
