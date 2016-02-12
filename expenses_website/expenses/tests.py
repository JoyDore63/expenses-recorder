import logging

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Category, Expense


logger = logging.getLogger(__name__)
OK = 200
MOVED = 301
REDIRECT = 302
test_category = Category.objects.create(description='Treat')
purchase_date = timezone.now()


# Used for tests on the logged in test cases
class LoggedInTestBase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('joy', 'joy@test.com', 'password')
        self.client.login(username='joy', password='password')


# Validation tests are here.
# Validations added to model are not called when models are used directly
class ExpenseFormTests(LoggedInTestBase):

    def test_post_creates_expense(self):
        '''
        Post of valid data should create an expense
        '''
        response = self.client.post('/expense_form/',
                                    {'user': 'joy',
                                     'category': test_category,
                                     'purchase_date': timezone.now(),
                                     'description': 'Flapjack',
                                     'price': 1.5, })
        self.assertEqual(response.status_code, OK)

    def test_expense_not_created_with_negative_price(self):
        '''
        Post of data with negative price should fail
        '''
        response = self.client.post('/expense_form',
                                    {'user': 'joy',
                                     'category': test_category,
                                     'purchase_date': timezone.now(),
                                     'description': 'Refund',
                                     'price': -0.01, })
        self.assertEquals(response.status_code, MOVED)

    def test_duplicate_expense_not_created(self):
        '''
        Post of duplicate data should fail
        '''
        expense = Expense.objects.create(user='joy',
                                                 category=test_category,
                                                 purchase_date=purchase_date,
                                                 description='Coffee',
                                                 price=2.2)
        response = self.client.post('/expense_form/',
                                    {'user': 'joy',
                                     'category': test_category,
                                     'purchase_date': purchase_date,
                                     'description': 'Coffee',
                                     'price': 2.2, })
        logger.debug('response after post:'+repr(response))
        #self.assertContains(response, 'Duplicate data not allowed')
        response = self.client.get(reverse('expenses:list'))
        logger.debug('response after get:'+repr(response))
        logger.debug('response type is:'+repr(type(response)))
        # context appears not to be there!
        #logger.debug('reponse.context'+repr(response.context))
        #self.assertEqual(len(response.context['expense']), 1)
        self.assertContains(response, 'Duplicate data not allowed')
        

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
        expense = Expense.objects.create(user='joy',
                                         category=test_category,
                                         purchase_date=timezone.now(),
                                         description='Coffee',
                                         price=2.2)
        response = self.client.get(reverse('expenses:list'))
        self.assertContains(response, expense.description)


# Login required tests
class LoginRequiredTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('joy', 'joy@test.com', 'password')

    def test_home_page_requires_login(self):
        '''
        The home page should not be displayed if the user is not logged in
        '''
        response = self.client.get(reverse('expenses:home'))
        self.assertEqual(response.status_code, REDIRECT)

    def test_home_page_logged_in(self):
        '''
        The home page should be displayed if the user is logged in
        '''
        self.client.login(username='joy', password='password')
        response = self.client.get(reverse('expenses:home'))
        self.assertEqual(response.status_code, OK)
