# Generated by Django 3.2 on 2021-05-13 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_user_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='date_of_birth',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]