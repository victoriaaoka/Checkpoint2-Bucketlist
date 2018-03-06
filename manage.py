import os
from flask_script import Manager
import unittest
from flask_migrate import Migrate, MigrateCommand
from my_app import models
from my_app.app import db, create_app


app = create_app(config_name=os.getenv('APP_SETTINGS'))
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def runtests():
    """Runs the unit tests automatically."""
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=1).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@manager.command
def initdb():
        db.create_all()
        print('All tables created.')

@manager.command
def dropdb():
        db.drop_all()
        print('All tables deleted.')

if __name__ == '__main__':
    manager.run()
