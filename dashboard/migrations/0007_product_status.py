# Generated by Django 4.0.4 on 2022-06-04 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(default='available', max_length=200),
        ),
    ]
