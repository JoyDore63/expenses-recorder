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

    class Meta:
        verbose_name_plural = 'Categories'  # Shows in admin site


class Expense(models.Model):
    description = models.CharField(max_length=120)
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    # Include 'human-readable' name for purchase date
    purchase_date = models.DateTimeField('date of purchase')
