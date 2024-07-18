import os
from src import create_app
from src import db
# from src.extensions import db
from flask_migrate import Migrate

# from src.models.post import post

app = create_app('development')
migrate = Migrate(app, db)

# @app.shell_context_processor
# def make_shell_context():
#     return dict(db=db)
if __name__=='__main__':
    app.run(port=os.getenv("PORT", 5000), debug=os.getenv("DEBUG", True))