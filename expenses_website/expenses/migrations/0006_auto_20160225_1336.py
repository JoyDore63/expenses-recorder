# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-25 13:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0005_auto_20160212_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]