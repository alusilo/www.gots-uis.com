# Generated by Django 3.2 on 2021-05-28 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='school',
            field=models.CharField(default='', max_length=45),
            preserve_default=False,
        ),
    ]
