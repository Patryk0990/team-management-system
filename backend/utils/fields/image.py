from django.db import models
from .widgets.image import ImageWidget


class ImageField(models.ImageField):
    def formfield(self, **kwargs):
        defaults = {'widget': ImageWidget}
        defaults.update(kwargs)
        return super().formfield(**defaults)
