"""Kullanıcı ondalık sayı girdisini kayıpsız ayrıştırma."""

import re
from decimal import Decimal

MAX_DECIMAL_INPUT_LENGTH = 256
MAX_DECIMAL_DIGITS = 128
_DECIMAL_PATTERN = re.compile(r"[+-]?(?:[0-9]+(?:[.,][0-9]*)?|[.,][0-9]+)")


class DecimalInputError(ValueError):
    """Kullanıcı ondalık girdisi güvenle ayrıştırılamadığında oluşur."""


def parse_decimal(value: str) -> Decimal:
    """Ondalık metni ikili kayan nokta kullanmadan ayrıştır."""
    if not isinstance(value, str):
        raise TypeError("Ondalık değer metin olarak verilmelidir.")
    if len(value) > MAX_DECIMAL_INPUT_LENGTH:
        raise DecimalInputError("Ondalık değer çok uzun; en fazla 256 karakter kullanın.")
    if "," in value and "." in value:
        raise DecimalInputError("Ondalık sayı biçimi belirsiz; tek ayırıcı kullanın.")
    if _DECIMAL_PATTERN.fullmatch(value) is None:
        raise DecimalInputError("Ondalık değer geçerli ve sonlu bir sayı olmalıdır.")
    if sum(character.isdigit() for character in value) > MAX_DECIMAL_DIGITS:
        raise DecimalInputError("Ondalık değer en fazla 128 basamak içermelidir.")
    return Decimal(value.replace(",", "."))
