# Generated by Django 5.1.6 on 2025-03-11 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pending_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(null=True)),
                ('failed_at', models.DateTimeField(null=True)),
                ('type', models.CharField(choices=[('common', 'Most Common'), ('level', 'Highest Level')], max_length=20)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', max_length=20)),
                ('data', models.JSONField(null=True)),
            ],
            options={
                'ordering': ['-pending_at'],
            },
        ),
    ]
