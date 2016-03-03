import logging

from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.template import RequestContext
from django.contrib import messages

from .models import Expense, Category
from .forms import CreateExpenseForm, FilterListForm, CreateCategoryForm

logger = logging.getLogger(__name__)


def logout_view(request):
    logout(request)
    return redirect(reverse('expenses:logged_out'))


class LoggedOutView(TemplateView):
    template_name = 'expenses/logged_out.html'


class ExpenseListView(LoginRequiredMixin, FormView):
    model = Expense
    template_name = 'expenses/list.html'
    form_class = FilterListForm

    def get_context_data(self, select_data=True, **kwargs):
        context = super(ExpenseListView, self).get_context_data(**kwargs)
        if select_data:
            expense_list = Expense.objects.order_by('-category',
                                                    '-purchase_date')
            context['recent_expenses_list'] = expense_list
        return context

    def form_valid(self, form, **kwargs):
        category_choices = form.cleaned_data['category_choices']
        new_list = Expense.objects.filter(category__in=category_choices)
        context = self.get_context_data(select_data=False, **kwargs)
        context['recent_expenses_list'] = new_list
        # Need a RequestContext to handle the csrf token, context is a dict
        return render(
            self.request,
            self.template_name,
            context=context,
            context_instance=RequestContext(self.request))


class CategoryCreate(LoginRequiredMixin, FormView):
    model = Category
    template_name = 'expenses/category_form.html'
    form_class = CreateCategoryForm

    def form_valid(self, form):
        category = Category(description=form.cleaned_data['description'])
        try:
            category.save()
        except IntegrityError:
            form.add_error(None, "Duplicate data not allowed")
            return self.form_invalid(form)
        self.success_url = reverse('expenses:category', args=(category.pk,))
        return HttpResponseRedirect(self.success_url)


class ExpenseCreate(LoginRequiredMixin, FormView):
    model = Expense
    template_name = 'expenses/expense_form.html'
    form_class = CreateExpenseForm

    def form_valid(self, form):
        # Create new Expense object
        expense = get_expense_from_form(self.request.user, form)
        try:
            expense.save()
        except IntegrityError:
            logger.debug('caught integrity error')
            form.add_error(None, 'Duplicate data not allowed')
            return self.form_invalid(form)
        messages.success(
            self.request,
            "Expense: " + expense.description + ", was created sucessfully"
        )
        return HttpResponseRedirect(reverse('expenses:list'))

#  Super call amended by Dave, from    get(self, request)
#    def get(self, request):
#        super(ExpenseCreate, self).get(request)

#    def post(self, request):
#        super(ExpenseCreate, self).post(request)


class ResultView(LoginRequiredMixin, DetailView):
    model = Expense
    template_name = 'expenses/result.html'


class CategoryView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'expenses/category.html'


def get_expense_from_form(user, form):
    category = form.cleaned_data['category']
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
