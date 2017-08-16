# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-13 01:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0009_auto_20170809_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personal',
            name='usuario',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]