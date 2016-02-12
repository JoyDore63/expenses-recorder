import logging

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Category, Expense


logger = logging.getLogger(__name__)


def get_category():
    return Category.objects.create(description='Treat')


# TODO Valid data tests
# TODO Price is within valid range
class ModelValidationTests(TestCase):

    def test_price_negative_validation(self):
        '''
        If the price is negative shouldn't be able to create an expense
        '''
        with self.assertRaises(ValidationError):
            e = Expense(
                user='joy',
                category=get_category(),
                purchase_date=timezone.now(),
                description='Coffee',
                price=-0.1
            )
            logger.debug('expense created '+e.description)
            # Expense.objects.create(
                #user='joy',
                # category=get_category(),
                # purchase_date=timezone.now(),
                # description='Coffee',
                # price=-0.1
                #)


# List view tests
class ListViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('joy', 'joy@test.com', 'password')
        self.client.login(username='joy', password='password')

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
                                         category=get_category(),
                                         purchase_date=timezone.now(),
                                         description='Coffee',
                                         price=2.2)
        response = self.client.get(reverse('expenses:list'))
        logger.debug('boo!')
        self.assertContains(response, expense.description)


# Login required tests
class LoginRequiredTests(TestCase):

    REDIRECT = 302
    OK = 200

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('joy', 'joy@test.com', 'password')

    def test_home_page_requires_login(self):
        '''
        The home page should not be displayed if the user is not logged in
        '''
        response = self.client.get(reverse('expenses:home'))
        self.assertEqual(response.status_code, self.REDIRECT)

    def test_home_page_logged_in(self):
        '''
        The home page should be displayed if the user is logged in
        '''
        self.client.login(username='joy', password='password')
        response = self.client.get(reverse('expenses:home'))
        self.assertEqual(response.status_code, self.OK)
