__all__ = (
    "ValidatorException",
    "NoPairProvidedError",
    "NoNameProvidedError",
    "NoValueProvidedError",
    "PairAmbiguousError",
    "BadNamingError",
    "RepeatingNameError"
)


class ValidatorException(Exception):
    """ Some error occurs during validation process. """


class NoPairProvidedError(ValidatorException):
    """ `=` statement missing. You need provide key and value organized by such template `name=value` """


class NoNameProvidedError(ValidatorException):
    """ Key missing. You need provide key organized by such template `name=value` """


class NoValueProvidedError(ValidatorException):
    """ Value missing. You need provide value organized by such template `name=value` """


class PairAmbiguousError(ValidatorException):
    """ Some pair 'name=value' ambiguous. Possible due to few `=` statements. """


class BadNamingError(ValidatorException):
    """ Name must be a camel case. """


class RepeatingNameError(ValidatorException):
    """ Names must be unique """
