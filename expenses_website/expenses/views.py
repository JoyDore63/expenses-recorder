from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Expense, User, Category
from .forms import AddExpenseForm


class HomeView(TemplateView):
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
    fields = ['user', 'category', 'purchase_date', 'description', 'price']

    # TODO create separate get_success_url method - overriding std one

    def form_valid(self, form):
        expense = get_expense_from_form(form)
        expense.save()
        self.success_url = reverse('expenses:result', args=(expense.pk,))
        return super(ExpenseCreate, self).form_valid(form)

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
            expense = get_expense_from_form(form)
            expense.save()
            return HttpResponseRedirect(
                reverse('expenses:result', args=(expense.pk,))
            )
    else:
        form = AddExpenseForm()

    return render(request, 'expenses/add_expense.html', {'form': form})


def get_expense_from_form(form):
    user = User.objects.get(name=form.cleaned_data['user'])
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
