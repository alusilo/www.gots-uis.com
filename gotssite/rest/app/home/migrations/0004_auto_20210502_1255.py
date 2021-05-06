# Generated by Django 3.2 on 2021-05-02 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_remove_configuration_total_items_carousel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.menu')),
            ],
        ),
        migrations.AlterField(
            model_name='configuration',
            name='group_logo',
            field=models.ImageField(default='static/img/logo.png', upload_to='static'),
        ),
        migrations.CreateModel(
            name='MenuItemElement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.menuitem')),
            ],
        ),
    ]