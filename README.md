# python-jsr303

A Python validator based on [JSR 303](https://beanvalidation.org/1.0/spec/), [Hibernate Validator](http://hibernate.org/validator/), and [Symfony Validator](https://symfony.com/doc/current/components/validator.html).


## Introduction

```python
from jsr303 import validation

validator = validation.create_validator()
violations = validator.validate('Brussels', [Length(min=10), NotBlank()])

if violations:
    for violation in violations:
        print(violation.message)
```

## Custom Validation Constraint

```python
from jsr303 import Constraint, ConstraintValidator, validate

class ContainsAlphanumeric(Constraint):

    message = "The string {string} contains an illegal character: it can only contain letters or numbers."


import re


class ContainsAlphanumericValidator(ConstraintValidator):

    def validate(value: str, constraint: Constraint) -> None:
        """
        :raises UnexpectedTypeException
        """
        if value is None or value == "":
            return;
        if type(value) != str:
            raise UnexpectedTypeException(value, 'str')
        if not re.match('^[a-zA-Z0-9]+$', value):
            self.context.buildViolation(constraint.message).
                parameter(string=value).
                add_violation()


class FooClass(object):

    def __init__(self, value=None):
        self._value = value

    @validate(validators=[NotNone, Blank, ContainsAlphanumeric])
    @property
    def do_something(self):
        return self._value
```