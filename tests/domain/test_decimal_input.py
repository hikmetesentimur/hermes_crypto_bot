from decimal import Decimal

import pytest

from hermes_crypto_bot.domain.decimal_input import DecimalInputError, parse_decimal


def test_parse_decimal_accepts_dot_separator() -> None:
    assert parse_decimal("10.25") == Decimal("10.25")


def test_parse_decimal_accepts_comma_separator() -> None:
    assert parse_decimal("10,25") == Decimal("10.25")


@pytest.mark.parametrize(
    ("value", "expected"),
    [("+12", Decimal("12")), ("-.5", Decimal("-0.5")), ("5.", Decimal("5"))],
)
def test_parse_decimal_accepts_fixed_point_grammar(value: str, expected: Decimal) -> None:
    assert parse_decimal(value) == expected


@pytest.mark.parametrize("value", ["1,234.56", "1.234,56"])
def test_parse_decimal_rejects_mixed_separators(value: str) -> None:
    with pytest.raises(DecimalInputError, match="belirsiz"):
        parse_decimal(value)


def test_parse_decimal_rejects_binary_float_input() -> None:
    with pytest.raises(TypeError, match="metin"):
        parse_decimal(0.1)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "value",
    [
        "",
        " ",
        " 1",
        "1 ",
        "+",
        "-",
        ".",
        ",",
        "abc",
        "1_000",
        "1e3",
        "1E-3",
        "NaN",
        "Infinity",
        "-Infinity",
        "1.2.3",
    ],
)
def test_parse_decimal_rejects_invalid_or_non_finite_values(value: str) -> None:
    with pytest.raises(DecimalInputError, match="geçerli ve sonlu"):
        parse_decimal(value)


def test_parse_decimal_rejects_overlong_input() -> None:
    with pytest.raises(DecimalInputError, match="çok uzun"):
        parse_decimal("+" + ("0" * 256))


def test_parse_decimal_rejects_too_many_digits() -> None:
    value = ("0" * 128) + ".1"

    with pytest.raises(DecimalInputError, match="basamak"):
        parse_decimal(value)
