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
        available_currencies = list(map(lambda item: item[0], CURRENCY_CHOICES))
        if self.currency not in available_currencies:
            raise ValidationError(f"Invalid currency. Choose one of the following: {available_currencies}")

        min_price = 0.50 * (USDRUB_rate if self.currency == 'RUB' else 1)
        max_price = 999999.99 * (USDRUB_rate if self.currency == 'RUB' else 1)

        if self.price < min_price or self.price > max_price:
            raise ValidationError(f"Price value should be not less than {min_price} and not greater than {max_price}")

        super(Item, self).clean()

    def save(self, **kwargs):
        self.clean()
        super(Item, self).save(**kwargs)

    def __str__(self):
        return f"{self.name} | {self.price} {self.currency}"
