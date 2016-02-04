from django.views import generic
from django.http import HttpResponse
from expenses_website.expenses.forms import AddExpenseForm

from .models import Expense


class IndexView(generic.ListView):
    template_name = 'expenses/index.html'
    context_object_name = 'recent_expenses_list'

    def get_queryset(self):
        '''Return the last 20 expenses'''
        return Expense.objects.order_by('-purchase_date')[:20]


class AddView(generic.View):
    template_name = 'expenses/add.html'
    form_class =  AddExpenseForm

    def get(self, request):
        # TODO
        return HttpResponse('add result')