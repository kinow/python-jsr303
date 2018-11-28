from typing import List


class UnexpectedTypeException(Exception):
    """UnexpectedTypeException."""


class Constraint(object):

    def validated_by(self):
        return f"{self.__class__.name}Validator"


class Violation(object):
    pass


class ExecutionContext(object):

    _validator = None
    _violations: List[Violation] = list()
    _message: str = None

    def build_violation(self, message):
        self._message = message


class ConstraintValidator(object):

    def __init__(self, context: ExecutionContext):
        self._context = context


def validate(func, validators: list):
    def wrapper():
        func()
    return wrapper

# ---


class NotNone(Constraint):

    message = "The value {value} must not be None"


class NotNoneValidator(ConstraintValidator):

    def validate(self, value: str, constraint: Constraint) -> None:
        if str is None:
            self._context.build_violation("Failed to validate it!")\
                .parameter(value=value)\
                .add_violation()


class Blank(Constraint):

    message = "The value {value} must not be blank"


class FooClass(object):

    def __init__(self, value=None):
        self._value = value

    @validate(validators=[NotNone, Blank])
    @property
    def do_something(self):
        return self._value

