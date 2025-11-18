import re
from handlers.errors import ValidationError
from models.field import Field


class Email(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, email: str):
        email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

        if (not email) or not bool(email.strip()):
            raise ValidationError("email", "Please enter email")

        if not re.match(email_pattern, email):
            raise ValidationError("email", "Email is not valid")

        self._value = email
