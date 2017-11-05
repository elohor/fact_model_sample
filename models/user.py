from models.base_model import *
from peewee import CharField

class User(BaseModel):
    username = CharField(20)
    password = CharField(20)
    email = CharField(80, unique=True)
    name = CharField(80)

    class Meta:
        db_table = 'users'
