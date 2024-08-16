from django.test import TestCase
from django.test import Client

class UserTests(TestCase):
    
    def test_users(self):
        c = Client()
        user_data = {
            'first_name': "Alice",
            'last_name': "Allison",
            'username': "alice007",
            'password': "pass_good",
            'email': "alice@example.com"
        }
        
        response = c.post('/api/v0/accounts/', user_data, 'application/json')
        self.assertEqual(response.status_code, 201)

        response = c.post('/api/v0/accounts/login', {
            'username': user_data['username'],
            'password': user_data['password']
        }, 'application/json')
        self.assertEqual(response.status_code, 200)
        pair_token = response.json()
        
        auth = {'Authorization': f"Bearer {pair_token['access']}"}
        response = c.get('/api/v0/expenses/', headers=auth)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])