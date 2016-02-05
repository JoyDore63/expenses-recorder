from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from .models import Expense, User, Category
from .forms import AddExpenseForm


class IndexView(ListView):
    model = Expense
    template_name = 'expenses/index.html'
    context_object_name = 'recent_expenses_list'

    def get_queryset(self):
        '''Return the last 20 expenses'''
        return Expense.objects.order_by('-purchase_date')[:20]


class ExpenseCreate(CreateView):
    model = Expense
    fields = ['user', 'category', 'purchase_date', 'description',  'price']
    

class ResultView(DetailView):
    model = Expense
    template_name = 'expenses/result.html'


def add_expense(request):
    if request.method == 'POST':
        form = AddExpenseForm(request.POST)
        if form.is_valid():
            user = User.objects.get(name=form.cleaned_data['user'])
            category = Category.objects.get(
                description=form.cleaned_data['category']
            )
            purchase_date = form.cleaned_data['purchase_date']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            expense = Expense(
                user=user,
                category=category,
                purchase_date=purchase_date,
                description=description,
                price=price
            )
            expense.save()
            return HttpResponseRedirect(
                reverse('expenses:result', args=(expense.pk,))
            )
    else:
        form = AddExpenseForm()

    return render(request, 'expenses/add_expense.html', {'form': form})
