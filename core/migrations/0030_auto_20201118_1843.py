# Generated by Django 3.0.5 on 2020-11-18 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_auto_20201109_1459'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventpracticeaudienceqa',
            options={'verbose_name': 'Practice Audience Q.A.', 'verbose_name_plural': 'Practice Audience Q.A.'},
        ),
        migrations.AlterModelOptions(
            name='subscriptionorder',
            options={'verbose_name': 'User Subscriptions', 'verbose_name_plural': 'User Subscriptions'},
        ),
        migrations.AlterField(
            model_name='event',
            name='session_lenght',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Session length'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='follower',
            field=models.CharField(blank=True, default=0, max_length=222, null=True, verbose_name='Followers'),
        ),
    ]
