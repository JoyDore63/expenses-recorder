from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Expense, Category
from .forms import AddExpenseForm


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'expenses/home.html'


class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'expenses/list.html'
    context_object_name = 'recent_expenses_list'

    def get_queryset(self):
        '''Return the last 20 expenses'''
        return Expense.objects.order_by('-purchase_date')[:20]


class ExpenseCreate(LoginRequiredMixin, CreateView):
    model = Expense
    fields = ['category', 'purchase_date', 'description', 'price']

    # TODO create separate get_success_url method - overriding std one

    def form_valid(self, form):
        expense = get_expense_from_form(self.request.user.username, form)
        expense.save()
        self.success_url = reverse('expenses:result', args=(expense.pk,))
        return HttpResponseRedirect(self.success_url)

#  Super call amended by Dave, from    get(self, request)
#    def get(self, request):
#        super(ExpenseCreate, self).get(request)

#    def post(self, request):
#        super(ExpenseCreate, self).get(request)


class ResultView(LoginRequiredMixin, DetailView):
    model = Expense
    template_name = 'expenses/result.html'


def add_expense(request):
    if request.method == 'POST':
        form = AddExpenseForm(request.POST)
        if form.is_valid():
            expense = get_expense_from_form(request.user.username, form)
            expense.save()
            return HttpResponseRedirect(
                reverse('expenses:result', args=(expense.pk,))
            )
    else:
        form = AddExpenseForm()

    return render(request, 'expenses/add_expense.html', {'form': form})


def get_expense_from_form(user, form):
    user = user
    category = Category.objects.get(
        description=form.cleaned_data['category']
    )
    purchase_date = form.cleaned_data['purchase_date']
    description = form.cleaned_data['description']
    price = form.cleaned_data['price']
    return Expense(
        user=user,
        category=category,
        purchase_date=purchase_date,
        description=description,
        price=price
    )
