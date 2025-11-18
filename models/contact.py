from models.name import Name
from models.phone import Phone
from models.birthday import Birthday
from models.email import Email
from models.address import Address


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.address = None
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_email(self, email):
        self.emails.append(Email(email))

    def set_address(self, address):
        self.address = Address(address)

    def set_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def find_phone(self, phone: str):
        """Find a phone by value"""
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def edit_phone(self, old_phone: str, new_phone: str):
        """Edit an existing phone number"""
        phone_obj = self.find_phone(old_phone)
        if phone_obj:
            phone_obj.value = new_phone
        else:
            raise ValueError(f"Phone {old_phone} not found.")

    def remove_phone(self, phone: str):
        """Remove a phone number"""
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)
        else:
            raise ValueError(f"Phone {phone} not found.")

    def find_email(self, email: str):
        """Find an email by value"""
        for e in self.emails:
            if e.value == email:
                return e
        return None

    def edit_email(self, old_email: str, new_email: str):
        """Edit an existing email address"""
        email_obj = self.find_email(old_email)
        if email_obj:
            email_obj.value = new_email
        else:
            raise ValueError(f"Email {old_email} not found.")

    def __str__(self):
        result = f"Contact name: {self.name.value}"
        if self.phones:
            result += f", phones: {'; '.join(p.value for p in self.phones)}"
        if self.emails:
            result += f", emails: {'; '.join(e.value for e in self.emails)}"
        if self.address:
            result += f", address: {self.address.value}"
        if self.birthday:
            result += f", birthday: {self.birthday}"
        return result
