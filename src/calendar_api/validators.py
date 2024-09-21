from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from re import match 
from datetime import date, timedelta

STATES = [
    'AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 
    'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 
    'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO'
]
DAYS_OF_WEEK = ['2a', '3a', '4a', '5a', '6a', 'sab', 'dom']
REGISTERS = ['CRM', 'CRBM', 'CRO', 'COREN', 'CRF', 'CRN'] 

def validate_cpf(cpf: str) -> str:
    """Efetua a validação do CPF, tanto formatação quando dígito verificadores.

    Parâmetros:
        cpf (str): CPF a ser validado

    Retorno:
        bool:
            - Falso, quando o CPF não possuir o formato 99999999999;
            - Falso, quando o CPF não possuir 11 caracteres numéricos;
            - Falso, quando os dígitos verificadores forem inválidos;
            - Verdadeiro, caso contrário.
    """

    if match(r"\d{3}\.\d{3}\.\d{3}-\d{2}", cpf):
        return ValidationError("CPF Inválido.")

    numbers = [int(digit) for digit in cpf if digit.isdigit()]

    if len(numbers) != 11 or len(set(numbers)) == 1:
        return ValidationError("CPF Inválido.")

    sum_of_products = sum(a * b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:
        return ValidationError("CPF Inválido.")

    sum_of_products = sum(a * b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        return ValidationError("CPF Inválido.")

    return cpf


def validate_cep(value) -> str:
    if not match(r'^\d{8}$', value):
        raise ValidationError(
            _('%(value)s nao esta no formato numero 12345678'),
            params={'value': value},
        )
    return str(value)


def validate_rg(value) -> str:
    if not match(r'^\d{1,9}$', value):
        raise ValidationError(
            _('%(value)s nao esta no formato numerico 123456789'),
            params={'value': value},
        )
    return str(value)


def validate_phone(value) -> str:
    if not match(r'^\d{11}$', value):
        raise ValidationError(
            _('%(value)s nao esta no formato numerico ddd+numero'),
            params={'value': value},
        )
    return str(value)
    

def validade_char_lower_than_16(value: str) -> str:
    if len(value) > 16:
        raise ValidationError(
            _('%(value)s tem mais de 16 caracteres'),
            params={'value': value},
        )
    return str(value)


def validade_char_lower_than_32(value: str) -> str:
    if len(value) > 32:
        raise ValidationError(
            _('%(value)s tem mais de 32 caracteres'),
            params={'value': value},
        )
    return str(value)


def validade_char_lower_than_64(value: str) -> str:
    if len(value) > 32:
        raise ValidationError(
            _('%(value)s tem mais de 64 caracteres'),
            params={'value': value},
        )
    return str(value)
    

def validate_integer(value) -> int:
    if not float(value).is_integer():
        raise ValidationError(
            _('%(value)s não é um número inteiro.'),
            params={'value': value},
        )
    return int(value)


def validate_have_max_6_digits(value) -> int:
    if value >= 999999:
        raise ValidationError(
            _('%(value)s o valor deve possuir no maximo 6 digitos'),
            params={'value': value},
        )
    return int(value)


def validate_grater_than_1(value) -> int:
    if value <= 0:
        raise ValidationError(
            _('%(value)s o valor deve possuir no maximo 6 digitos'),
            params={'value': value},
        )
    return int(value)


def validate_state(value) -> str:
    if value not in STATES:
        raise ValidationError(
            _('%(value)s não é um estado válido.'),
            params={'value': value},
        )
    return str(value)


def validate_days_of_week(value) -> str:
    if value not in DAYS_OF_WEEK:
        raise ValidationError(
            _('%(value)s não é um dia da semana válido.'),
            params={'value': value},
        )
    return str(value)


def validate_registers(value) -> str:
    if value not in REGISTERS:
        raise ValidationError(
            _('%(value)s não é um registro válido.'),
            params={'value': value},
        )
    return str(value)


def validate_date_not_newer_than_today(value):
    if value > date.today():
        raise ValidationError("Data nao pode ser mais recente que hoje.")  
    return value


def validate_date_not_130_years_later(value):
    if value < date.today() - timedelta(days=365*130):
        raise ValidationError(
            _('%(value)s Data nao pode ser maior de 130 anos de hoje.'),
            params={'value': value},
        )
    return value


def validate_date_not_older_than_today(value):
    if value < date.today():
        raise ValidationError(
            _('%(value)s Data nao pode ser mais antiga que hoje.'), 
            params={'value': value},
            )  
    return value


def validate_date_not_5_years_newer(value): 
    if value > date.today() + timedelta(days=365*5):
        raise ValidationError(
            _('Data nao pode ser maior de 10 anos de hoje.'), 
            params={'value': value}
        )
    return value
