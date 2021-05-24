from flask_sqlalchemy import SQLAlchemy
import pusher

db = SQLAlchemy()
pusher_client = pusher.Pusher(
    app_id=u'1208443',
    key=u'e62bffe8a9303c6d8215',
    secret=u'80c7f81c0f8de69f45ea',
    cluster=u'eu'
)


def init_db(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()

