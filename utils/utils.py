import re
from handlers.errors import ValidationError


def normalize_phone(phone_number: str):
    if not bool(phone_number.strip()):
        raise ValidationError("phone", "Phone number is empty")

    number_pattern = r"\d"
    phone_numbers_list = re.findall(number_pattern, phone_number.replace(" ", ""))
    cleaned_phone_number = "".join(phone_numbers_list)

    if len(phone_numbers_list) and phone_numbers_list[0] == "3":
        return f"{cleaned_phone_number}"
    else:
        return f"38{cleaned_phone_number}"


def parse_user_input_data(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args
