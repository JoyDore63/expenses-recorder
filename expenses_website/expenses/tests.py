import logging

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import IntegrityError

from .models import Category, Expense


logger = logging.getLogger(__name__)
OK = 200
MOVED = 301
REDIRECT = 302
purchase_date = timezone.now()


# Used for tests on the logged in test cases
class LoggedInTestBase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('joy', 'joy@test.com', 'password')
        self.client.login(username='joy', password='password')


class CategoryFormTests(LoggedInTestBase):

    def test_post_creates_category(self):
        '''
        Post of valid data should create a category
        '''
        response = self.client.post('/category_form/',
                                    description='Car Park')
        self.assertEqual(response.status_code, OK)

    def test_duplicate_category_not_created(self):
        '''
        Post of duplicate data should fail
        '''
        Category.objects.create(description='Treat')
        with self.assertRaises(IntegrityError):
            Category.objects.create(description='Treat')


# Validation tests are here.
# Validations added to model are not called when models are used directly
class ExpenseFormTests(LoggedInTestBase):

    def test_post_creates_expense(self):
        '''
        Post of valid data should create an expense
        '''
        test_category = Category.objects.create(description='Treat')
        response = self.client.post('/expense_form/',
                                    {'user': self.user,
                                     'category': test_category,
                                     'purchase_date': purchase_date,
                                     'description': 'Flapjack',
                                     'price': 1.5, })
        self.assertEqual(response.status_code, OK)

    def test_expense_not_created_with_negative_price(self):
        '''
        Post of data with negative price should fail
        '''
        test_category = Category.objects.create(description='Treat')
        response = self.client.post('/expense_form',
                                    {'user': self.user,
                                     'category': test_category,
                                     'purchase_date': purchase_date,
                                     'description': 'Refund',
                                     'price': -0.01, })
        self.assertEquals(response.status_code, MOVED)

    def test_expense_not_created_with_too_large_price(self):
        '''
        Post of data with too large price should fail
        '''
        test_category = Category.objects.create(description='Treat')
        response = self.client.post('/expense_form',
                                    {'user': self.user,
                                     'category': test_category,
                                     'purchase_date': purchase_date,
                                     'description': 'Expensive item',
                                     'price': 100})
        self.assertEquals(response.status_code, MOVED)

    def test_expense_not_created_with_too_many_decimal_places_in_price(self):
        '''
        Post of data with price having too many decimal places should fail
        '''
        test_category = Category.objects.create(description='Treat')
        response = self.client.post('/expense_form',
                                    {'user': self.user,
                                     'category': test_category,
                                     'purchase_date': purchase_date,
                                     'description': 'Expensive item',
                                     'price': 1.123})
        self.assertEquals(response.status_code, MOVED)

    def test_duplicate_expense_not_created(self):
        '''
        Post of duplicate data should fail
        '''
        test_category = Category.objects.create(description='Treat')
        Expense.objects.create(user=self.user,
                               category=test_category,
                               purchase_date=purchase_date,
                               description='Coffee',
                               price=2.2)
        with self.assertRaises(IntegrityError):
            Expense.objects.create(user=self.user,
                                   category=test_category,
                                   purchase_date=purchase_date,
                                   description='Coffee',
                                   price=2.2)


# List view tests
class ListViewTests(LoggedInTestBase):

    def test_list_view_with_no_expenses(self):
        '''
        If no expenses exist an appropriate message should be displayed
        '''
        response = self.client.get(reverse('expenses:list'))
        self.assertContains(response, 'No expenses are available')

    def test_list_view_contains_expense(self):
        '''
        If an expense exists it should be displayed
        '''
        category = Category.objects.create(description='Treat')
        expense = Expense.objects.create(user=self.user,
                                         category=category,
                                         purchase_date=timezone.now(),
                                         description='Coffee',
                                         price=2.2)
        response = self.client.get(reverse('expenses:list'))
        self.assertContains(response, expense.description)

        def test_category_filter(self):
            '''
            Only the expenses in the chosen category should be displayed
            '''
            category1 = Category.objects.create(description='Treat')
            category2 = Category.objects.create(description="Lunch")
            expense1 = Expense.objects.create(user=self.user,
                                              category=category1,
                                              purchase_date=timezone.now(),
                                              description='Coffee',
                                              price=2.9)
            expense2 = Expense.objects.create(user=self.user,
                                              category=category2,
                                              purchase_date=timezone.now(),
                                              description='salad',
                                              price=3.0)
            category_choices = [category1]
            response = self.client.get(reverse('expenses:list'),
                                       category_choices)
            self.assertContains(response, expense1.description)
            self.assertNotContains(response, expense2.description)


class ResultViewTests(LoggedInTestBase):

    def test_result_view_contains_expense(self):
            '''
            If an expense exists it should be displayed
            '''
            category = Category.objects.create(description='Treat')
            expense = Expense.objects.create(user=self.user,
                                             category=category,
                                             purchase_date=timezone.now(),
                                             description='Coffee',
                                             price=2.2)
            response = self.client.get(reverse('expenses:result',
                                       args=(expense.id,)))
            self.assertContains(response, expense.description)


# Login required tests
class LoginRequiredTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('joy', 'joy@test.com', 'password')

    def test_list_page_requires_login(self):
        '''
        The list page should not be displayed if the user is not logged in
        '''
        response = self.client.get(reverse('expenses:list'))
        self.assertEqual(response.status_code, REDIRECT)

    def test_list_page_logged_in(self):
        '''
        The list page should be displayed if the user is logged in
        '''
        self.client.login(username='joy', password='password')
        response = self.client.get(reverse('expenses:list'))
        self.assertEqual(response.status_code, OK)
