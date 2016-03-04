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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Expense, Category
from .forms import CreateExpenseForm, FilterListForm, CreateCategoryForm

logger = logging.getLogger(__name__)
LIST_PAGE_SIZE = 6


def logout_view(request):
    logout(request)
    return redirect(reverse('expenses:logged_out'))


class LoggedOutView(TemplateView):
    template_name = 'expenses/logged_out.html'


class ExpenseListView(LoginRequiredMixin, FormView):
    model = Expense
    template_name = 'expenses/list.html'
    form_class = FilterListForm

    def __init__(self):
        self.expense_list = Expense.objects.order_by('-category',
                                                     '-purchase_date')

    # Provides data for the Form __init__ method
    def get_initial(self):
        initial = super(ExpenseListView, self).get_initial()
        # Enables the correct sub-set of categories to be ticked on the page
        # after the user has made a selection
        if 'form_data'in self.request.session.keys():
            # Use the categories selected by the user
            initial['categories'] = self.request.session.__getitem__(
                'form_data')['category_choices']
        else:
            # Nothing saved so must be first time in, select all categories
            initial['categories'] = Category.objects.all().values_list(
                'id',
                flat=True
            )
        return initial

    def get_context_data(self, **kwargs):
        context = super(ExpenseListView, self).get_context_data(**kwargs)
        # Look in the session for saved form data
        #  to get the currently selected categories
        # Otherwise next/prev resets to include all the categories
        if 'form_data' in self.request.session.keys():
            # Get the categories selected by the user
            current_categories = self.request.session.__getitem__(
                'form_data')['category_choices']
            # Filter the list with selected categories
            self.expense_list = Expense.objects.filter(
                category__in=current_categories
            ).order_by('-category',
                       '-purchase_date'
                       )
        context['expenses_list'] = get_page_list(self,
                                                 self.expense_list,
                                                 LIST_PAGE_SIZE)
        return context

    def form_valid(self, form, **kwargs):
        # Get categories just chosen by the user and use to filter list
        category_choices = form.cleaned_data['category_choices']
        filtered_list = Expense.objects.filter(category__in=category_choices
                                               ).order_by('-category',
                                                          '-purchase_date')
        # Save filtered list in context to send back to page
        context = self.get_context_data(**kwargs)
        context['expenses_list'] = get_page_list(self,
                                                 filtered_list,
                                                 LIST_PAGE_SIZE)
        # Save the data so we can get it back later,
        #   eg when getting next/prev page
        self.request.session['form_data'] = form.cleaned_data
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


def get_page_list(self, full_list, page_size):
    paginator = Paginator(full_list, page_size)
    page = self.request.GET.get('page')
    try:
        page_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        page_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        page_list = paginator.page(paginator.num_pages)
    return page_list
