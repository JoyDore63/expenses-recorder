# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-03 16:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_expense'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterField(
            model_name='expense',
            name='purchase_date',
            field=models.DateField(verbose_name='date of purchase'),
        ),
    ]
