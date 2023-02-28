from peewee import *
import sqlite3

# set database
db = SqliteDatabase("data.db")


# створення базового класу з якого будуть наслідуватися інші
class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order_by = "id"


class User(BaseModel):

    login = CharField()
    first_name = CharField(max_length=50)
    last_name = CharField()
    phone_number = CharField()
    mail = CharField()
    vacantion = CharField()
    photo_id = CharField()

    class Meta:
        db_table = "Users"


class Job(BaseModel):
    # стоврення зовнішнього ключа на таблицю
    user = ForeignKeyField(User, backref="Jobs", on_delete='CASCADE', constraint_name='user')
    position = CharField()
    years = CharField()
    description = CharField()

    class Meta:
        db_table = "Jobs"

    def to_dict(self):
        result = {"position": self.position, "years": self.years, "description": self.description}
        return result


class Education(BaseModel):

    # стоврення зовнішнього ключа на таблицю
    # каскадне видалення on_delete='CASCADE'
    user = ForeignKeyField(User, backref="Educations", on_delete='CASCADE')
    place = CharField()
    name = CharField()
    grade = CharField()

    class Meta:
        db_table = "Educations"

    def to_dict(self):
        result = {"place": self.place, "name": self.name, "grade": self.grade}
        return result
