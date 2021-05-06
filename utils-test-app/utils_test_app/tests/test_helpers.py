from app_utils.helpers import humanize_number
from django.test import TestCase


class TestFormatisk(TestCase):
    def test_should_return_formatted_string_from_number_1(self):
        # when
        result = humanize_number(1260000000)
        # then
        self.assertEqual(result, "1.3b")

    def test_should_return_formatted_string_from_number_2(self):
        # when
        result = humanize_number(123456789)
        # then
        self.assertEqual(result, "123.5m")

    def test_should_return_formatted_string_from_string(self):
        # when
        result = humanize_number("1234567890")
        # then
        self.assertEqual(result, "1.2b")

    def test_should_raise_value_error_when_type_invalid(self):
        # when/then
        with self.assertRaises(ValueError):
            humanize_number("invalid")

    def test_should_use_custom_magnitude(self):
        # when
        result = humanize_number(123456789, "b")
        # then
        self.assertEqual(result, "0.1b")

    def test_should_format_with_custom_precision(self):
        # when
        result = humanize_number("1234567890", precision=3)
        # then
        self.assertEqual(result, "1.235b")
