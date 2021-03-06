# Generated by Django 2.0.3 on 2018-05-04 12:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='cretae_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Create Date'),
        ),
        migrations.AddField(
            model_name='projects',
            name='modify_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Modify Date'),
        ),
        migrations.AddField(
            model_name='projects',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='projects',
            name='projectDescription',
            field=models.TextField(blank=True, null=True, verbose_name='DESCRIPTION'),
        ),
        migrations.AddField(
            model_name='projects',
            name='projectName',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='projects',
            name='projectTag',
            field=models.TextField(blank=True, null=True, verbose_name='PROJECT TAG'),
        ),
    ]
