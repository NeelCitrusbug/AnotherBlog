# Generated by Django 3.0.5 on 2020-10-31 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20201030_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionplan',
            name='stripe_product_id',
            field=models.CharField(blank=True, max_length=222, null=True),
        ),
    ]
