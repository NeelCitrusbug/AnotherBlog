# Generated by Django 3.0.5 on 2020-10-26 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20201026_1355'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'User Profile', 'verbose_name_plural': 'User Profile'},
        ),
        migrations.AlterField(
            model_name='user',
            name='customer_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Customer Id'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_influencer',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Influencer'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='credit',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Credit'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='follwer',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Followers'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='is_popular',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Popular'),
        ),
    ]
