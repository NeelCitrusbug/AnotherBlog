# Generated by Django 3.0.5 on 2020-11-03 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_eventorder_transaction_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
