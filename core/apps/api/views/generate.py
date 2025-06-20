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

import base64
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from datetime import timedelta
from rest_framework.decorators import action




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
    queryset = GenerateModel.objects.order_by("-created_at") 

    @action(detail=False, methods=["get"], url_path="stats", permission_classes=[AllowAny])
    def stats(self, request):
        today = now().date()
        start_of_week = today - timedelta(days=6)
        start_of_month = today.replace(day=1)

        daily_count = GenerateModel.objects.filter(created_at__date=today).count()
        weekly_count = GenerateModel.objects.filter(created_at__date__gte=start_of_week).count()
        monthly_count = GenerateModel.objects.filter(created_at__date__gte=start_of_month).count()
        total_count = GenerateModel.objects.count()

        return Response({
            "daily": daily_count,
            "weekly": weekly_count,
            "monthly": monthly_count,
            "total": total_count
        })
    
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




class QRDecodeView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, encoded_id):
        try:
            padded = encoded_id + "=" * (-len(encoded_id) % 4)
            decoded_bytes = base64.urlsafe_b64decode(padded)
            decoded_str = decoded_bytes.decode()

            item_id = decoded_str.split("-")[-1]
            obj = get_object_or_404(GenerateModel, id=item_id)

            return Response({
                "pdf_url": obj.result_pdf.url,
                "owner": obj.owner,
                "client": obj.client,
                "purpose": obj.purpose,
                "valuation_amount": obj.valuation_amount,
            })

        except Exception as e:
            return Response({"error": str(e)}, status=400)
