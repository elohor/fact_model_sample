from models.base_model import *
from peewee import CharField

class User(BaseModel):
    password = CharField(32)
    email = CharField(80, unique=True)
    first_name = CharField(80)
    last_name = CharField(80)

    class Meta:
        db_table = 'users'
