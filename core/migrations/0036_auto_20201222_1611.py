# Generated by Django 3.0.5 on 2020-12-22 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_event_is_transfer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventscript',
            name='title',
            field=models.TextField(blank=True, null=True, verbose_name='Title'),
        ),
    ]