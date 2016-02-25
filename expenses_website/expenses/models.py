# coding=utf8
from __future__ import unicode_literals

from django.db import models
from django.core.validators import DecimalValidator, MinValueValidator


'''
The User can create an Expense which will be in a category.
For example,
   User: Tony (from login)
   Category: Treats
   Expense: Coffee
'''


class Category(models.Model):
    description = models.CharField(max_length=30, unique=True)

    # Helper for testing and debugging, as recommended by Alex2
    # This is also used on the auto-generated expense_form
    def __unicode__(self):
        return u'{}'.format(self.description)

    class Meta:
        verbose_name_plural = 'Categories'  # Shows in admin site
        ordering = ['description']


class Expense(models.Model):
    description = models.CharField(max_length=120)
    user = models.CharField(max_length=10)
    category = models.ForeignKey(Category)
    price = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[DecimalValidator(4, 2),
                    MinValueValidator(limit_value=0.01)]
    )
    # Include 'human-readable' name for purchase date
    purchase_date = models.DateField('date of purchase')

    # Helper for testing and debugging, as recommended by Alex2
    def __unicode__(self):
        #  \xa puts a pound sign in front of the price
        return u'{} - {} - {} - {} - £{}'.format(
            self.user,
            self.purchase_date,
            self.category,
            self.description,
            self.price
        )

    class Meta:
        ordering = ['purchase_date', 'description']
        unique_together = ('user',
                           'category',
                           'purchase_date',
                           'description',
                           'price')
