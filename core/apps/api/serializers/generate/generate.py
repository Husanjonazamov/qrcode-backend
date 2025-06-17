from rest_framework import serializers
from django.core.files.base import ContentFile
from core.apps.api.models import GenerateModel
from core.apps.api.views.qrcode import add_qr_to_each_page


class BaseGenerateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenerateModel
        fields = [
            "id",
            "owner",
            "client",
            "purpose",
            "valuation_amount",
            "status",
            "input_pdf",
            "result_pdf"
        ]


class ListGenerateSerializer(BaseGenerateSerializer):
    class Meta(BaseGenerateSerializer.Meta):
        pass


class RetrieveGenerateSerializer(BaseGenerateSerializer):
    class Meta(BaseGenerateSerializer.Meta):
        pass


class CreateGenerateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenerateModel
        fields = [
            'owner',
            'client',
            'purpose',
            'valuation_amount',
            'input_pdf',
        ]
    def create(self, validated_data):
        instance = super().create(validated_data)

        item_id = f"{instance.id}"
        output_buffer = add_qr_to_each_page(instance.input_pdf.path, item_id)

        instance.result_pdf.save(
            f'processed_{instance.id}.pdf',
            ContentFile(output_buffer.read())
        )
        return instance


