# tests/test_users.py

import unittest

from flask import request
from flask_login import current_user

from base import BaseTestCase
from project import bcrypt
from project.models import User

class TestUser(BaseTestCase):
    
    def test_user_registration(self):
        '''Ensure user can register'''
        with self.client:
            response = self.client.post('/register', data=dict(username='Tigere', email='tigere@tigere.dev', password='password123', confirm='password123'),
            follow_redirects=True)
            self.assertIn(b'Welcome to Flask', response.data)
            self.assertTrue(current_user.name == 'Tigere')
            self.assertTrue(current_user.is_active)
            user = User.query.filter_by(email='admin@admin.com').first()
            self.assertTrue(str(user) == '<name - admin>')

    def test_incorrect_user_registration(self):
        '''Ensure errors are thrown during an incorrect user registration'''
        with self.client:
            response = self.client.post('/register', data=dict(
                username='Tigere', email='tigere',
                password='python', confirm='python'
            ), follow_redirects=True)
            self.assertIn(b'Invalid email address.', response.data)
            self.assertIn('/register', request.url)

    def test_get_by_id(self):
        '''Ensure id is correct for the current/logged in user'''
        with self.client:
            self.client.post('/login', data=dict(
                username='admin', password='admin'
            ), follow_redirects=True)
            self.assertTrue(current_user.id == 1)
            self.assertFalse(current_user.id == 20)
    
    def test_check_password(self):
        '''Ensure given password is correct after unhashing'''
        user = User.query.filter_by(email='admin@admin.com').first()
        self.assertTrue(bcrypt.check_password_hash(user.password, 'admin'))
        self.assertFalse(bcrypt.check_password_hash(user.password, 'foobar'))



class UsersViewsTests(BaseTestCase):
        # Ensure that the login page loads correctly
    def test_login_page_loads(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertTrue(b'Please login' in response.data)

    # Ensure login behaves correctly given the correct credentials
    def test_correct_login(self):
        with self.client:
            response = self.client.post('/login', data=dict(username='admin', password='admin'),
            follow_redirects=True)
            self.assertIn(b'You were logged in.', response.data)
            self.assertTrue(current_user.name == 'admin')
            self.assertTrue(current_user.is_active())

    # Ensure login behaves correctly given the wrong credentials
    def test_incorrect_login(self):
        response = self.client.post('/login', data=dict(username='wrongusername', password='wrongpassword'),
        follow_redirects=True)
        self.assertIn(b'Invalid Credentials. Please try again.', response.data)

    # Ensure logout behaves correctly
    def test_logout(self):
        with self.client:
            response = self.client.post('/login', data=dict(username='admin', password='admin'),
            follow_redirects=True)
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn(b'You were logged out.', response.data)
            self.assertFalse(current_user.is_active)

    # Ensure that logout page requires user login
    def test_logout_route_requires_login(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertIn(b'Please log in to access this page.', response.data)



if __name__ == '__main__':
    unittest.main()