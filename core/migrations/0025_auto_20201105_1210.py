# Generated by Django 3.0.5 on 2020-11-05 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_contactus_email'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='offer',
            options={'ordering': ['-created_at'], 'verbose_name': 'Offer', 'verbose_name_plural': 'Offers'},
        ),
        migrations.AlterModelOptions(
            name='subscriptionplan',
            options={'ordering': ['-price'], 'verbose_name': 'Subscription Plan', 'verbose_name_plural': 'Subscription Plan'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-created_at'], 'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
        migrations.AddField(
            model_name='offer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
