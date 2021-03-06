# Generated by Django 3.0.5 on 2020-11-09 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_event_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='credit_required',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Credit required'),
        ),
        migrations.AlterField(
            model_name='event',
            name='number_of_participants',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Number of participants'),
        ),
        migrations.AlterField(
            model_name='event',
            name='remianing_spots',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Remianing spots'),
        ),
    ]
