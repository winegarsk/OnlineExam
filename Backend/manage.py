from flask.cli import FlaskGroup

from src.app import app
from src.models import User, Session, engine, Base

cli = FlaskGroup(app)

# if needed, generate database schema
session = Session()

@cli.command("create_db")
def create_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

@cli.command("seed_db")
def seed_db():
    session.add(User(email="asearle@g.clemson.edu",first_name="Adrian",last_name="Searles",username="asearle",password="Pspgame12"))
    session.commit()


if __name__ == "__main__":
    cli()