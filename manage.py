from app import create_app, db
from flask_script import Manager,Server
from flask_migrate import Migrate, MigrateCommand
from app.models import User

# Creating app instance
app = create_app('development')

manager = Manager(app)
manager.add_command('server',Server)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)  

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)

#shell is used to test features in our app and for debugging
@manager.shell 
def make_shell_context():
    return dict(app = app, db = db, User = User)

if __name__ == '__main__':
    manager.run()