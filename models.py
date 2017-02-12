from connect import ConnectDatabase
from peewee import *


class Stories(Model):
    story_name = TextField()
    user_story = TextField()
    acceptance_criteria = TextField()
    business_value = IntegerField()
    estimation = FloatField()
    status = CharField(default='Planning')

    class Meta:
        database = ConnectDatabase.db