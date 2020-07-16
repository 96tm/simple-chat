from app import create_app, database, socket_io
from app.models import add_test_users as add_users
from app.models import UserChatTable, Chat, RemovedChat
from app.models import User, Role, Contact, Message
from config import ProductionConfig


app = create_app(ProductionConfig.name)


@app.cli.command('add_test_users')
def add_test_users():
    add_users()


@app.cli.command('test')
def test_all():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.shell_context_processor
def make_shell_context():
    return {'database': database,
            'UserChatTable': UserChatTable,
            'Chat': Chat,
            'User': User,
            'Role': Role,
            'RemovedChat': RemovedChat,
            'Contact': Contact, 
            'Message': Message,
            'add_test_users': add_users}


if __name__ == '__main__':
    socket_io.run(app, debug=True)
