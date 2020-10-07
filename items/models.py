from django.db import models
from django.core.validators import MinValueValidator


class Item(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True, default='')
    price = models.FloatField(validators=[MinValueValidator(0.50)])

    def __str__(self):
        return f"{self.name} | {self.price}$"
