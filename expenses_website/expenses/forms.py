from django import forms
from django.utils import timezone

from .models import Category


class CreateExpenseForm(forms.Form):
    category = forms.ModelChoiceField(Category.objects.all())
    purchase_date = forms.DateField(widget=forms.SelectDateWidget,
                                    initial=timezone.now)
    description = forms.CharField(max_length=120)
    price = forms.DecimalField(widget=forms.TextInput,
                               max_digits=4,
                               min_value=0.01,
                               decimal_places=2)


class FilterListForm(forms.Form):
    # Create a list of tuples as MultipleChoiceField is not happy with
    # list of objects from Category.objects.all()
    choice_list = []
    for category in Category.objects.all():
        choice_list.append((category.pk, category.description))
    # Get just the pks for initial values => all checkboxes will be ticked
    initial_values = [pk for pk, description in choice_list]
    category_choices = forms.MultipleChoiceField(
        choice_list,
        widget=forms.CheckboxSelectMultiple,
        initial=initial_values
    )
