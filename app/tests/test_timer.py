import unittest

from flask_login.mixins import UserMixin
from app.models import Timer, User

class TestTimer(unittest.TestCase):
    '''
    Test class to test the behaviour of the Timer Class
    '''
    def setUp(self):
        self.user_John_Doe = User(username = 'John Doe', password = 'qwerty900', email = 'johndoe@gmail.com', bio = 'I love coding',
        profile_pi_path = 'https://image.tmdb.org/t/p/w500/jdjdjdjn', pitch = 'talk is cheap show me the codes')
        self.new_timer = Timer(username = 'John Doe', pomodoro_interval = '1hr', break_interval = '5min')

    def tearDown(self):
        Timer.Clear_timer()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_timer, Timer))

    def test_check_instance_variables(self):
        self.asserEquals(self.new_timer.username, 'John Doe')
        self.assertEquals(self.new_timer.pomodoro_interval, '1hr')
        self.assertEquals(self.new_timer.break_interval, '5min')

    def test_save_timer(self):
        self.new_timer.save_timer()
        self.assertTrue(len(Timer.query.all() > 0))