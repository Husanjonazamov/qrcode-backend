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
            "id",
            'owner',
            'client',
            'purpose',
            'valuation_amount',
            'input_pdf',
        ]
    def create(self, validated_data):
        instance = super().create(validated_data)

        try:
            item_id = str(instance.id)
            original_pdf_path = instance.input_pdf.path

            output_buffer = add_qr_to_each_page(original_pdf_path, item_id)

            instance.result_pdf.save(
                f"processed_{instance.id}.pdf",
                ContentFile(output_buffer.read())
            )

        except Exception as e:
            raise serializers.ValidationError(f"Error: \n\n{e}\n\n")

        return instance


