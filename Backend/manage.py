from flask.cli import FlaskGroup

from src.app import app, database


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    database.drop_all()
    database.create_all()
    database.session.commit()

if __name__ == "__main__":
    cli()