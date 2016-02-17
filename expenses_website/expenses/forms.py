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
    category_choices = forms.MultipleChoiceField(required=True, 
                                                widget=None, 
                                                label=None, 
                                                initial=None, 
                                                help_text='')