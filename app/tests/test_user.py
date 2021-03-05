import unittest
from app.models import User


class TestUser(unittest.TestCase):
    '''
    Test class to test the behaviour of the User class
    '''
    def setUp(self):
        self.user_John_Doe = User(username = 'John Doe', password = 'Iamjohndoe', email = 'johndoe@gmail.com', bio = 'I love coding',
        profile_pi_path = 'https://image.tmdb.org/t/p/w500/jdjdjdjn', pitch = 'talk is cheap show me the codes')

        def tearDown(self):
            User.Clear_user()

        def test_check_instance_variables(self):
            self.assertEquals(self.new_John_Doe.id, 1)
            self.assertEquals(self.new_John_Doe.username, 'John Doe')
            self.assertEquals(self.new_John_Doe.password, 'Iamjohndoe')
            self.assertEquals(self.new_John_Doe.email, 'johndoe@gmail.com')
            self.assertEquals(self.new_John_Doe.bio, 'I love coding')
            self.assertEquals(self.new_John_Doe.profile_pic_path, 'https://image.tmdb.org/t/p/w500/jdjdjdjn')
            self.assertEquals(self.new_John_Doe.pitch, 'talk is cheap show me the codes')

        def test_password_setter(self):
            self.assertTrue(self.news_user.pass_secure is not None)

        def test_no_access_password(self):
            with self.assertRaises(AttributeError):
                self.new_user.password

        def test_password_verification(self):
            self.assertTrue(self.new_user.verify_password('Iamjohndoe'))