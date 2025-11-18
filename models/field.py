class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
