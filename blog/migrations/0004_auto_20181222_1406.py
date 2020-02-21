# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-12-22 14:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='modified_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]