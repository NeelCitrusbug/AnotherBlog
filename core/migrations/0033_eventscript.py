# Generated by Django 3.0.5 on 2020-12-10 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_user_earned_money'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventScript',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='Title')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='evnt_script', to='core.Event')),
            ],
            options={
                'verbose_name': 'Event Script',
                'verbose_name_plural': 'Event Script',
            },
        ),
    ]