from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
import datetime
from peewee import *

# DATABASE
DATABASE = SqliteDatabase('database.db')


# MODEL FOR USER
class User(UserMixin, Model):
    # DATA FIELDS FOR USER
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    email = CharField(max_length=100, unique=True)
    username = CharField(max_length=100, unique=True)
    password = CharField(max_length=100)
    miles = IntegerField(default=0)

    # LINK DATABASE TO USER
    class Meta:
        database = DATABASE

    # FUNCTION TO GET ALL FLIGHTS FROM USER
    def get_flights(self):
        return Flight.select().where(Flight.user == self)

    # FUNCTION TO CREATE USER
    @classmethod
    def create_user(cls, first_name, last_name, email, username, password):
        try:
            with DATABASE.transaction():
                cls.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=username,
                    password=generate_password_hash(password),
                    miles=0
                )
        # expects that an error could occur if user exists
        except IntegrityError:
            raise ValueError("User already exists")


# MODEL FOR FLIGHT
class Flight(Model):
    # DATA FIELDS FOR USER
    timestamp = DateTimeField(default=datetime.datetime.now)
    seat_number = TextField()
    flight_number = TextField()
    origin = TextField()
    destination = TextField()
    departure_time = TextField()
    arrival_time = TextField()
    airplane_model = TextField()
    date = TextField()

    # ADDS FLIGHT TO USER REQUESTING IT
    user = ForeignKeyField(
        model=User,
        related_name='flight'
    )

    # SORTS FLIGHTS BY TIME ADDED
    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)


# INITIALIZE MODEL
def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Flight], safe=True)
    DATABASE.close()
