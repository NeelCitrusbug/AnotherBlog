# Generated by Django 3.0.5 on 2020-11-05 07:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_banner_created_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
    ]