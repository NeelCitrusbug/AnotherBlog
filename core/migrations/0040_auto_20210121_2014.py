# Generated by Django 3.0.5 on 2021-01-21 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_auto_20201223_1346'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contactus',
            options={'verbose_name': 'Mailing list', 'verbose_name_plural': 'Mailing list'},
        ),
        migrations.AddField(
            model_name='influenceroffer',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='evnt_offer', to='core.Event'),
        ),
    ]
