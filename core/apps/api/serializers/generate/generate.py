from rest_framework import serializers

from core.apps.api.models import GenerateModel
from django.core.files.base import ContentFile
from core.apps.api.views.qrcode import add_qr_to_pdf
import os


class BaseGenerateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenerateModel
        fields = [
            "id",
            "name",
            "year",
            "color",
            "owner",
            "other_info",
            "processed_pdf"
        ]


class ListGenerateSerializer(BaseGenerateSerializer):
    class Meta(BaseGenerateSerializer.Meta): ...


class RetrieveGenerateSerializer(BaseGenerateSerializer):
    class Meta(BaseGenerateSerializer.Meta): ...



        
class CreateGenerateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenerateModel
        fields = [
            'name',
            'year',
            'color',
            'owner',
            'other_info',
            'pdf_file'
        ]

    def create(self, validated_data):
        instance = super().create(validated_data)

        input_pdf_file = instance.pdf_file  
        
        output_path = f"media/processed_pdfs/processed_{instance.id}.pdf"

        output_buffer = add_qr_to_pdf(input_pdf_file, output_path, instance)

        instance.processed_pdf.save(
            f'processed_{instance.id}.pdf',
            ContentFile(output_buffer.read())
        )

        return instance

