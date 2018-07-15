from datetime import datetime

from mongoengine.queryset import CASCADE

from mongoengine import (
    Document,
    StringField,
    EmailField,
    BooleanField,
    ListField,
    ComplexDateTimeField,
    ReferenceField,
ObjectIdField
)

from lib.security import generate_password_hash, check_password_hash


class User(Document):
    username = StringField(required=True, min_length=4)
    email = EmailField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    password_hash = StringField(required=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Task(Document):
    owner = ReferenceField(User, reverse_delete_rule=CASCADE)
    title = StringField(max_length=120, required=True)
    body = StringField(max_length=256)
    timestamp = ComplexDateTimeField(default=datetime.utcnow)
    done = BooleanField(default=False)
    tags = ListField(StringField(max_length=30))
