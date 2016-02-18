import logging

from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError

from .models import Expense, Category
from .forms import CreateExpenseForm, FilterListForm

logger = logging.getLogger(__name__)


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'expenses/home.html'


class ExpenseListView(LoginRequiredMixin, FormView):
    model = Expense
    template_name = 'expenses/list.html'
    form_class = FilterListForm
    success_url = '/expense/list/'

    def get_context_data(self, **kwargs):
        context = super(ExpenseListView, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['recent_expenses_list'] = Expense.objects.order_by('-purchase_date')[:20]
        return context

    def form_valid(self, form):
        category_choices = form.cleaned_data['category_choices']
        logger.error("choices:"+repr(category_choices))
        return HttpResponseRedirect(self.fish)

    def form_invalid(self, form):
        logger.error("FORM INVALID")
        return super(ExpenseListView)


class ExpenseCreate(LoginRequiredMixin, FormView):
    model = Expense
    template_name = 'expenses/expense_form.html'
    form_class = CreateExpenseForm

    # TODO create separate get_success_url method - overriding std one

    def form_valid(self, form):
        expense = get_expense_from_form(self.request.user.username, form)
        try:
            expense.save()
        except IntegrityError:
            logger.debug('caught integrity error')
            form.add_error(None, 'Duplicate data not allowed')
            return self.form_invalid(form)
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


def get_expense_from_form(user, form):
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
