import unittest
from app.models import Todos, User


class TestTodo():
    '''
    Test class to test the behaviour of the Todo Class
    '''
    def setUp(self):
        self.user_John_Doe = User(username = 'John Doe', password = 'qwerty900', email = 'johndoe@gmail.com', bio = 'I love coding',
        profile_pi_path = 'https://image.tmdb.org/t/p/w500/jdjdjdjn', pitch = 'talk is cheap show me the codes')
        self.new_todo = Todos(username = 'John Doe', category = 'Personal', description = 'Creating a navbar', completed = 'Pending',
        create_date = '02,02,2021')

    def tearDown():
        Todos.Clear_todo()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_todo, Todos))

    def test_check_instance_variables(self):
        self.assertEquals(self.new_todo.username, 'John Doe')
        self.assertEquals(self.new_todo.category, 'Personal')
        self.assertEquals(self.new_todo.completed, 'Pending')
        self.assertEquals(self.new_todo.create_date, '02,02,20201')

    def test_save_todo(self):
        self.new_todo.save_todo()
        self.assertTrue(len(Todos.query.all() > 0))
    