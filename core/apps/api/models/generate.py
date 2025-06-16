from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel


class GenerateModel(AbstractBaseModel):
    name = models.CharField(verbose_name=_("Nomi"), max_length=255)
    year = models.CharField(verbose_name=_("Yili"), max_length=255, blank=True, null=True)
    color = models.CharField(verbose_name=_("Rangi"), max_length=50, blank=True, null=True)
    owner = models.CharField(verbose_name=_("Egasi"), max_length=50, blank=True, null=True)
    other_info = models.TextField(verbose_name=_("Tavsif"), blank=True, null=True)
    pdf_file = models.FileField(upload_to='pdfs/')
    processed_pdf = models.FileField(upload_to='processed_pdfs/', null=True, blank=True)

    
    
    def __str__(self):
        return self.name
    
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
