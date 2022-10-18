from enum import Enum


class BustType(str, Enum):
    """
    Тип бюста.
    """

    NATURAL = "Natural"
    IMPLANTS = "Implants"
