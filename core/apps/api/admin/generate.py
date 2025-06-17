from django.contrib import admin
from unfold.admin import ModelAdmin

from core.apps.api.models import GenerateModel


@admin.register(GenerateModel)
class GenerateAdmin(ModelAdmin):
    list_display = (
        "id",
        "owner",
        "client",
        "purpose",
        "status",
        "valuation_amount"
    )
