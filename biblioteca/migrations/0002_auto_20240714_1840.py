# Generated by Django 2.2.9 on 2024-07-14 21:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuario',
            old_name='senha',
            new_name='password',
        ),
    ]
