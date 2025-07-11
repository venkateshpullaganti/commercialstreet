# Generated by Django 5.0.6 on 2025-07-08 17:15

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]
