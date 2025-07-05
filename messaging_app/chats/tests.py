from django.test import TestCase
from .models import users

class UserTestCase(TestCase):
    def test_create_user(self):
        """Test that a user can be created"""
        user = users.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='password123',
            first_name='Test',
            last_name='User'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
