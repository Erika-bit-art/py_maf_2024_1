# Generated by Django 2.2.9 on 2024-08-04 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registros', '0004_registro_foto_base64'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
