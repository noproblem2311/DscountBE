# Generated by Django 4.2.9 on 2024-02-06 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='videotranscription',
            name='note',
            field=models.TextField(blank=True, null=True, verbose_name='Note'),
        ),
    ]