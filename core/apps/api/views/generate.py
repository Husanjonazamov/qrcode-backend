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

from django.http import FileResponse
import os
from django.http import FileResponse, Http404
from rest_framework.permissions import AllowAny

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"detail": "Muvaffaqiyatli o'chirildi"},
            status=status.HTTP_200_OK  
        )




class DownloadPDFAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            obj = GenerateModel.objects.get(pk=pk)
            file_path = obj.result_pdf.path  
            if not os.path.exists(file_path):
                raise Http404("Fayl topilmadi")
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
        except GenerateModel.DoesNotExist:
            raise Http404("Obyekt topilmadi")
