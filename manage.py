import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from my_app import db, create_app
from my_app import models


app = create_app(config_name=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
