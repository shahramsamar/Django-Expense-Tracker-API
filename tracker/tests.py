from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import ExpenseIncome
from django.urls import reverse

class AuthenticationTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
    
    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('access' in response.data)
    
    def test_user_login(self):
        # First register
        self.client.post(self.register_url, self.user_data)
        # Then login
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)

class ExpenseIncomeTests(APITestCase):
    def setUp(self):
        self.expense_list_url = reverse('expenses-list')
        
        self.user1 = User.objects.create_user(username='user1', password='pass1')
        self.user2 = User.objects.create_user(username='user2', password='pass2')
        self.admin = User.objects.create_superuser(username='admin', password='adminpass')
        
        # Create test records
        ExpenseIncome.objects.create(
            user=self.user1,
            title='User1 Expense',
            amount=100.00,
            transaction_type='debit',
            tax=10.00,
            tax_type='flat'
        )
        ExpenseIncome.objects.create(
            user=self.user2,
            title='User2 Expense',
            amount=200.00,
            transaction_type='credit',
            tax=5.00,
            tax_type='percentage'
        )
        
        # Get tokens
        self.user1_token = self.get_token('user1', 'pass1')
        self.user2_token = self.get_token('user2', 'pass2')
        self.admin_token = self.get_token('admin', 'adminpass')
    
    def get_token(self, username, password):
        response = self.client.post(reverse('login'), {
            'username': username,
            'password': password
        })
        return response.data['access']
    
    def test_create_expense(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user1_token}')
        data = {
            'title': 'New Expense',
            'amount': 50.00,
            'transaction_type': 'debit',
            'tax': 5.00,
            'tax_type': 'flat'
        }
        response = self.client.post(self.expense_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data['total']), 55.00)
    
    def test_user_can_only_see_own_records(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user1_token}')
        response = self.client.get(self.expense_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'User1 Expense')
    
    def test_admin_can_see_all_records(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(self.expense_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_tax_calculations(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user1_token}')
        
        # Test flat tax
        data = {
            'title': 'Flat Tax Test',
            'amount': 100.00,
            'transaction_type': 'debit',
            'tax': 10.00,
            'tax_type': 'flat'
        }
        response = self.client.post(self.expense_list_url, data)
        self.assertEqual(float(response.data['total']), 110.00)
        
        # Test percentage tax
        data = {
            'title': 'Percentage Tax Test',
            'amount': 100.00,
            'transaction_type': 'debit',
            'tax': 10.00,
            'tax_type': 'percentage'
        }
        response = self.client.post(self.expense_list_url, data)
        self.assertEqual(float(response.data['total']), 110.00)
        
        # Test zero tax
        data = {
            'title': 'Zero Tax Test',
            'amount': 100.00,
            'transaction_type': 'debit',
            'tax': 0.00,
            'tax_type': 'flat'
        }
        response = self.client.post(self.expense_list_url, data)
        self.assertEqual(float(response.data['total']), 100.00)