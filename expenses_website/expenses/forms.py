from django import forms


class AddExpenseForm(forms.Form):
    category = forms.CharField(label='Category', max_length=30)
    purchase_date = forms.DateField(label='Date purchased')
    description = forms.CharField(label='Description', max_length=120)
    price = forms.DecimalField(label='Price',
                               min_value=0.01,
                               max_digits=5,
                               decimal_places=2)
