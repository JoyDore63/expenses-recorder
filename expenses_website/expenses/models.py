from __future__ import unicode_literals

from django.db import models


"""
The User can create an Expense which will be in a category.
For example,
   User: Tony
   Category: Treats
   Expense: Coffee
"""


class User(models.Model):
    name = models.CharField(max_length=6)


class Category(models.Model):
    description = models.CharField(max_length=30)
