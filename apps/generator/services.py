import secrets
import string


class PasswordGeneratorService:
    DICEWARE_WORDS = [
        'alpha', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf', 'hotel',
        'india', 'juliet', 'kilo', 'lima', 'mike', 'november', 'oscar', 'papa',
        'quebec', 'romeo', 'sierra', 'tango', 'uniform', 'victor', 'whiskey',
        'xray', 'yankee', 'zulu'
    ]

    @staticmethod
    def generate(length=16, use_uppercase=True, use_lowercase=True, use_numbers=True, use_symbols=True, use_diceware=False):
        if use_diceware:
            return PasswordGeneratorService._build_diceware_phrase(length)

        charset = ''
        if use_uppercase:
            charset += string.ascii_uppercase
        if use_lowercase:
            charset += string.ascii_lowercase
        if use_numbers:
            charset += string.digits
        if use_symbols:
            charset += '!@#$%^&*()-_=+[]{}|;:,.<>?'

        if not charset:
            raise ValueError('Debe seleccionar al menos un tipo de carácter.')

        return ''.join(secrets.choice(charset) for _ in range(length))

    @staticmethod
    def _build_diceware_phrase(num_words=5):
        words = [secrets.choice(PasswordGeneratorService.DICEWARE_WORDS) for _ in range(num_words)]
        return ' '.join(words)

    @staticmethod
    def calculate_strength(password: str, diceware=False) -> int:
        if diceware:
            score = min(len(password.split()) * 15, 100)
            return score

        score = 0
        if any(c.islower() for c in password):
            score += 1
        if any(c.isupper() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(c in '!@#$%^&*()-_=+[]{}|;:,.<>?' for c in password):
            score += 1
        if len(password) >= 12:
            score += 1
        return min(score * 20, 100)
