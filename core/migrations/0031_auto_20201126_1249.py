# Generated by Django 3.0.5 on 2020-11-26 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_auto_20201118_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='influencer_stripe_account_id',
            field=models.CharField(blank=True, max_length=222, null=True, verbose_name='Influencer stripe id'),
        ),
        migrations.DeleteModel(
            name='Charge',
        ),
    ]
