# Generated by Django 3.0.5 on 2020-10-27 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20201027_1207'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='question',
            field=models.CharField(blank=True, max_length=222, null=True, verbose_name='Question'),
        ),
    ]