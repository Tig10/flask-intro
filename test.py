from app import app
import unittest

class FlaskTestCase(unittest.TestCase):
    
    # Ensure that Flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that the login page loads correctly
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertTrue(b'Please login' in response.data)

    # Ensure login behaves correctly given the correct credentials
    def test_correct_login(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(username='admin', password='admin'),
        follow_redirects=True)
        self.assertIn(b'You were just logged in!', response.data)

    # Ensure login behaves correctly given the wrong credentials
    def test_incorrect_login(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(username='wrongusername', password='wrongpassword'),
        follow_redirects=True)
        self.assertIn(b'Invalid credentials. Please try again.', response.data)

    # Ensure logout behaves correctly
    def test_logout(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(username='admin', password='admin'),
        follow_redirects=True)
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn(b'You were just logged out!', response.data)

    # Ensure the main page requires a login
    def test_main_route_requires_login(self):
        tester = app.test_client(self)
        response = tester.get('/', follow_redirects=True)
        self.assertTrue(b'You need to login first.' in response.data)

    # Ensure that posts show up on the main page
    def test_post_show_up(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(username='admin', password='admin'), follow_redirects=True)
        self.assertTrue(b'Hello from the shell', response.data)


if __name__ == '__main__':
    unittest.main()