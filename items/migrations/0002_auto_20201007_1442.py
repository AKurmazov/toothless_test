# Generated by Django 3.1.2 on 2020-10-07 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='currency',
            field=models.CharField(choices=[('USD', 'USD'), ('RUB', 'RUB')], default='USD', max_length=3),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.FloatField(),
        ),
    ]
