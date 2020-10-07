from django.db import models
from django.core.exceptions import ValidationError


CURRENCY_CHOICES = (
    ('USD', 'USD'),
    ('RUB', 'RUB')
)
USDRUB_rate = 80  # Hard-coded


class Item(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True, default='')
    price = models.FloatField()
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')

    def clean(self):
        min_price = 0.50 * (USDRUB_rate if self.currency == 'RUB' else 1)
        max_price = 999999.99 * (USDRUB_rate if self.currency == 'RUB' else 1)

        if self.price < min_price or self.price > max_price:
            raise ValidationError(f"Price value should be not less than {min_price} and not greater than {max_price}")

        super().clean()

    def __str__(self):
        return f"{self.name} | {self.price} {self.currency}"
