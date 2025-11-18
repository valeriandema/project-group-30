from handlers.errors import ValidationError
from models.field import Field
from utils.utils import normalize_phone


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, phone: str):
        formatted_phone = normalize_phone(phone)

        if not formatted_phone.isdigit():
            raise ValidationError("phone", "Expected only digits")

        if len(formatted_phone) != 12:
            raise ValidationError("phone", "Invalid phone number. Format: 380XXXXXXXXX")

        self._value = phone
