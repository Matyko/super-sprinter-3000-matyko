from connect import ConnectDatabase
from peewee import *


class Stories(Model):
    story_name = CharField()
    user_story = CharField()
    acceptance_criteria = CharField()
    business_value = IntegerField()
    estimation = FloatField()
    status = CharField(default='Planning')

    class Meta:
        database = ConnectDatabase.db