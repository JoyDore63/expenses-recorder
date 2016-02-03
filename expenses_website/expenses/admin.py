from django.contrib import admin

from .models import User, Category, Expense

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Expense)
