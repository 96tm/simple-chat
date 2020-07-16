from app import create_app, database
from app.models import User, Role, Chat
import unittest
        

class ClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        database.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

        self.bob = User(username='bob', password='bob', email='bob@bob.bob', confirmed=True)
        self.arthur = User(username='arthur', password='arthur', email='arthur@arthur.arthur', confirmed=True)
        self.clair = User(username='clair', password='clair', email='clair@clair.clair', confirmed=True)
        self.chat_bob_arthur = Chat()
        self.chat_bob_arthur.add_users([self.bob, self.arthur])
        database.session.add_all([self.bob, self.arthur, self.clair, self.chat_bob_arthur])
        database.session.commit()
    
    def test_index(self):
        response = self.client.post('/auth/login', data={
            'email': 'bob@bob.bob',
            'password': 'bob'
        }, follow_redirects=True)
        self.assertIn('Simple Messenger - bob',
                      response.get_data(as_text=True))

    def test_register_and_login(self):
        response = self.client.post('/auth/signup', data={
            'email': 'no_such_email@gmail.com',
            'username': 'user',
            'password': 'pass',
            'password_confirmation': 'pass'
        })
        self.assertEqual(response.status_code, 302)

        user = User.query.filter_by(username='user').first()

        response = self.client.post('/auth/login', data={
            'email': 'user@user.user',
            'password': 'pass'
        }, follow_redirects=True)
        self.assertIn('Invalid', response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/auth/login', data={
            'email': 'no_such_email@gmail.com',
            'password': 'pass'
        }, follow_redirects=True)
        self.assertIn('Hello', response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)

        user = User(username='confirmed_user', password ='pass',
                email='confirmed@confirmed.confirmed', confirmed=True)
        database.session.add(user)
        database.session.commit()

        response = self.client.post('/auth/login', data={
            'email': 'confirmed@confirmed.confirmed',
            'password': 'pass'
        }, follow_redirects=True)
        self.assertIn(f'Simple Messenger - {user.username}',
                      response.get_data(as_text=True))

    def tearDown(self):
        database.session.remove()
        database.drop_all()
        self.app_context.pop()
