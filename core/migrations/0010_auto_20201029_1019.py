# Generated by Django 3.0.5 on 2020-10-29 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_subscriptionplan_stripe_plan_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionorder',
            name='plan_status',
            field=models.CharField(blank=True, choices=[('active', 'Active'), ('cancel', 'Cancel')], max_length=222, null=True),
        ),
        migrations.AddField(
            model_name='subscriptionorder',
            name='stripe_subscription_id',
            field=models.CharField(blank=True, max_length=222, null=True),
        ),
    ]