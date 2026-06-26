"""Unit tests for shared validators."""

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from core.validators import validate_non_negative_decimal, validate_positive_decimal


class ValidatorTests(SimpleTestCase):
    def test_validate_positive_decimal_rejects_zero(self):
        with self.assertRaises(ValidationError):
            validate_positive_decimal(Decimal("0"))

    def test_validate_positive_decimal_accepts_positive(self):
        validate_positive_decimal(Decimal("1"))

    def test_validate_non_negative_decimal_rejects_negative(self):
        with self.assertRaises(ValidationError):
            validate_non_negative_decimal(Decimal("-1"))

    def test_validate_non_negative_decimal_accepts_zero(self):
        validate_non_negative_decimal(Decimal("0"))
