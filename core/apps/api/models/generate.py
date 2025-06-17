from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel



class StatusChoice(models.TextChoices):
    DOWNLOAD = 'downloaded', 'Yuklab olingan'
    PENDING = 'pending', 'Kutilmoqda'
    ERROR = 'error', 'Xatolik'

    


class GenerateModel(AbstractBaseModel):
    owner = models.CharField(max_length=255, verbose_name="Mulk egasi")
    client = models.CharField(max_length=255, verbose_name="Buyurtmachi")
    purpose = models.CharField(max_length=255, verbose_name="Baholash maqsadi")
    valuation_amount = models.CharField(
        verbose_name="Baholangan narx",
        max_length=200,
        blank=True, null=True
    )
    input_pdf = models.FileField(upload_to='uploads/original_pdfs/', verbose_name="Asl PDF fayl")
    result_pdf = models.FileField(upload_to='uploads/processed_pdfs/', blank=True, null=True, verbose_name="Tayyorlangan PDF")
    status = models.CharField(
        verbose_name=_("Status"),
        choices=StatusChoice.choices,
        max_length=100,
        default=StatusChoice.PENDING
        )

    
    def __str__(self):
        return self.owner
    
    def get_absolute_url(self):
        return f"/car-info/{self.id}/"

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="mock",
        )

    class Meta:
        db_table = "generate"
        verbose_name = _("GenerateModel")
        verbose_name_plural = _("GenerateModels")
