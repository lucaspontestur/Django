# Generated by Django 5.0.6 on 2024-05-31 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meu_app', '0004_nota'),
    ]

    operations = [
        migrations.AddField(
            model_name='nota',
            name='titulo',
            field=models.CharField(default='Nota', max_length=255),
        ),
    ]
