import re


class Validator:
    def __init__(self):
        self.input_string = ''

    @staticmethod
    def length_validation(input_string: str, max_len: int):
        string_len = len(input_string)
        if string_len > max_len:
            raise ValidationException(f'Maximum length {max_len} is exceeded!')

    @staticmethod
    def word_validation(input_string: str):
        for char in input_string:
            if not (char.isalpha() or char.isdigit()):
                raise ValidationException(f'Not a valid string {input_string}! Please use only word characters.')

    def date_validation(self, input_string: str):
        self.length_validation(input_string, max_len=11)
        date_list = input_string.split('.')
        if len(date_list) != 3 or list(filter(lambda x: not x.isdigit(), date_list)):
            raise ValidationException('Not a valid string. DD.MM.YYYY is valid format.')

    @staticmethod
    def email_validation(input_string: str):
        reg = re.compile('^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9.-]+$')
        email = reg.match(input_string)
        if not email:
            raise ValidationException('Not a valid email. xxx@xxx.xxx is a valid format.')


class ValidationException(Exception):
    def __init__(self, message):
        super().__init__(f'Validation error: {message}')
