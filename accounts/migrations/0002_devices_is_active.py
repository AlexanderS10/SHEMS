# Generated by Django 4.0.10 on 2023-12-11 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='devices',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
