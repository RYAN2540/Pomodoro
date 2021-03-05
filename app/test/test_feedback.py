import unittest
from app.models import Feedbacks, User

class TestFeedback(unittest.TestCase):
    '''
    Test class to class the behaviour of the Feedback class
    '''
    def setUp(self):
        self.user_John_Doe = User(username = 'John Doe', password = 'Iamjohndoe', email = 'johndoe@gmail.com', bio = 'I love coding',
        profile_pi_path = 'https://image.tmdb.org/t/p/w500/jdjdjdjn', pitch = 'talk is cheap show me the codes')
        self.new_feedback = Feedbacks(username = 'John Doe',feedback = 'I love Pomodoro Timer, helpful')

    def tearDown():
        Feedbacks.Clear_feedbacks()

    def tes_instance(self):
        self.assertTrue(isinstance(self.new_feedback, Feedbacks))

    def test_check_instance_variables(self):
        self.assertEquals(self.new_feedback.username, 'John Doe')
        self.assertEquals(self.new_feedback, 'I love Pomodoro Timer, helpful')

    def test_save_feedback(self):
        self.new_feedback.save_feedback()
        self.assertTrue(len(Feedbacks.query.all() > 0))