from modeltranslation.translator import TranslationOptions, register

from core.apps.api.models import GenerateModel


@register(GenerateModel)
class GenerateTranslation(TranslationOptions):
    fields = []
