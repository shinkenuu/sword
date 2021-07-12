from datetime import date

from django.test import TestCase

from apps.tasks.validations import validate_past_or_present


class IsPastOrPresentTestCase(TestCase):
    def test_raises_value_error_when_is_date_is_in_the_future(self):
        # ARRANGE
        future_date = date(9999, 12, 31)

        # ACT / ASSERT
        with self.assertRaises(ValueError):
            validate_past_or_present(future_date)

    def test_past_date_is_valid(self):
        # ARRANGE
        past_date = date(2000, 1, 1)

        # ACT / ASSERT
        validate_past_or_present(past_date)

    def test_preset_date_is_valid(self):
        # ARRANGE
        present_date = date.today()

        # ACT / ASSERT
        validate_past_or_present(present_date)
