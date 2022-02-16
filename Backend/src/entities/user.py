
# coding=utf-8

from marshmallow import Schema, fields

from sqlalchemy import Column, String

from .entity import Entity, Base






class User(Entity , Base):
    """User account."""

    __tablename__ = "user"

    id = Column(fields.Int, primary_key=True, autoincrement="auto")
    username = Column(fields.Str(255), unique=True, nullable=False)
    password = Column(fields.Str, nullable=False)
    email = Column(fields.Str(255), unique=True, nullable=False)
    first_name = Column(fields.Str(255))
    last_name = Column(fields.Str(255))

    def __init__(self, id, username, password,email,first_name,last_name):
        Entity.__init__(self)
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    
    class UserSchema(Schema):
        id = fields.Number()
        username = fields.Str(255)
        password =fields.Str
        email = fields.Str
        first_name = fields.Str
        last_name = fields.Str
        created_at = fields.DateTime()
        updated_at = fields.DateTime()
        last_updated_by = fields.Str()