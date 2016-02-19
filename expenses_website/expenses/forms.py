import logging

from django import forms
from django.utils import timezone

from .models import Category

logger = logging.getLogger(__name__)


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

    category_choices = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, **kwargs):
        super(FilterListForm, self).__init__(**kwargs)
        # Create a list of tuples as MultipleChoiceField is not happy with
        # list of objects from Category.objects.all()
        all_choices = Category.objects.all()
        self.fields['category_choices'].choices = all_choices.values_list(
            'id',
            'description'
        )
        # Get just the pks for initial values => all checkboxes will be ticked
        self.fields['category_choices'].initial = all_choices.values_list(
            'id',
            flat=True
        )
