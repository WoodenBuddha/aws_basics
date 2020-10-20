import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import blueprint
from app.main import create_app
from app.main import db

app = create_app(os.getenv('ENV') or 'dev')
app.register_blueprint(blueprint)
app.app_context().push()

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run(host="0.0.0.0", port=80)


@manager.command
def rundev():
    app.run()


if __name__ == '__main__':
    manager.run()