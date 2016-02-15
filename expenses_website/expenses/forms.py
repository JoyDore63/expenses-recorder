from django.forms import Form, ChoiceField, DateField, CharField, DecimalField

from .models import Category


class CreateExpenseForm(Form):
    category = ChoiceField(Category.objects.all())
    purchase_date = DateField()
    description = CharField(max_length=120)
    price = DecimalField(max_digits=4, min_value=0.01, decimal_places=2)
