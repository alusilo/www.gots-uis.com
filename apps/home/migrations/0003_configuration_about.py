# Generated by Django 3.2 on 2021-05-28 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20210528_0112'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='about',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
