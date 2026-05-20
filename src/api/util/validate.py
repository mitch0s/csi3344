import re

from api.object.base.errors import RequestValidationError


def validate_first_name(value: str) -> None:
    """
    Raises RequestValidationError if value argument fails validation
    for first name
    """

    if type(value) is not str:
        raise RequestValidationError('First name must be string type')

    value = value.strip()

    if len(value) < 1:
        raise RequestValidationError('First name cannot be empty')

    if len(value) > 64:
        raise RequestValidationError('First name too long')

    if not re.fullmatch(r"[A-Za-z \-']+", value):
        raise RequestValidationError('First name contains invalid characters')


def validate_last_name(value: str) -> None:
    """
    Raises RequestValidationError if value argument fails validation
    for last name
    """

    if type(value) is not str:
        raise RequestValidationError('Last name must be string type')

    value = value.strip()

    if len(value) < 1:
        raise RequestValidationError('Last name cannot be empty')

    if len(value) > 64:
        raise RequestValidationError('Last name too long')

    if not re.fullmatch(r"[A-Za-z \-']+", value):
        raise RequestValidationError('Last name contains invalid characters')


def validate_email_address(value: str) -> None:
    """
    Raises RequestValidationError if value argument fails validation
    for email address
    """

    if type(value) is not str:
        raise RequestValidationError('Email address must be string type')

    value = value.strip().lower()

    if len(value) < 3:
        raise RequestValidationError('Email address too short')

    if len(value) > 254:
        raise RequestValidationError('Email address too long')

    pattern = r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$"

    if not re.fullmatch(pattern, value):
        raise RequestValidationError('Invalid email address')


def validate_password(value: str) -> None:
    """
    Raises RequestValidationError if value argument fails validation
    for password
    """

    if type(value) is not str:
        raise RequestValidationError('Password must be string type')

    if len(value) < 8:
        raise RequestValidationError('Password must be at least 8 characters')

    if len(value) > 128:
        raise RequestValidationError('Password too long')

    if not re.search(r'[A-Z]', value):
        raise RequestValidationError('Password must contain uppercase character')

    if not re.search(r'[a-z]', value):
        raise RequestValidationError('Password must contain lowercase character')

    if not re.search(r'[0-9]', value):
        raise RequestValidationError('Password must contain numeric character')

    if not re.search(r'[^A-Za-z0-9]', value):
        raise RequestValidationError('Password must contain special character')