# Generated by Django 3.2 on 2021-05-28 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0002_auto_20210528_0810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='image',
            field=models.ImageField(upload_to='research/publications/img'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='research/publications/pdf'),
        ),
        migrations.AlterField(
            model_name='researcharea',
            name='image',
            field=models.ImageField(upload_to='research/img'),
        ),
    ]
