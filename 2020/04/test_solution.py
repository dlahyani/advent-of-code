from unittest import TestCase

import solution


class VerifyBirthYearTests(TestCase):
    def test_not_a_number(self):
        with self.assertRaises(ValueError):
            solution.verify_birth_year("not-a-number")

    def test_not_a_number_suffix(self):
        with self.assertRaises(ValueError):
            solution.verify_birth_year("1990g")

    def test_not_a_number_prefix(self):
        with self.assertRaises(ValueError):
            solution.verify_birth_year("x1990")

    def test_too_many_digits(self):
        with self.assertRaises(ValueError):
            solution.verify_birth_year("01990")

    def test_too_low(self):
        with self.assertRaises(ValueError):
            solution.verify_birth_year("1919")

    def test_too_high(self):
        with self.assertRaises(ValueError):
            solution.verify_birth_year("2003")

    def test_min(self):
        self.assertEqual(solution.verify_birth_year("1920"), 1920)

    def test_max(self):
        self.assertEqual(solution.verify_birth_year("2002"), 2002)

    def test_mid_range(self):
        self.assertEqual(solution.verify_birth_year("1990"), 1990)


class VerifyIssueYearTests(TestCase):
    def test_not_a_number(self):
        with self.assertRaises(ValueError):
            solution.verify_issue_year("not-a-number")

    def test_not_a_number_2(self):
        with self.assertRaises(ValueError):
            solution.verify_issue_year("2015g")

    def test_not_a_number_3(self):
        with self.assertRaises(ValueError):
            solution.verify_issue_year("x2015")

    def test_too_many_digits(self):
        with self.assertRaises(ValueError):
            solution.verify_birth_year("02015")

    def test_too_low(self):
        with self.assertRaises(ValueError):
            solution.verify_issue_year("2009")

    def test_too_high(self):
        with self.assertRaises(ValueError):
            solution.verify_issue_year("2021")

    def test_min(self):
        self.assertEqual(solution.verify_issue_year("2010"), 2010)

    def test_max(self):
        self.assertEqual(solution.verify_issue_year("2020"), 2020)

    def test_mid_range(self):
        self.assertEqual(solution.verify_issue_year("2015"), 2015)


class VerifyExpirationYearTests(TestCase):
    def test_not_a_number(self):
        with self.assertRaises(ValueError):
            solution.verify_expiration_year("not-a-number")

    def test_not_a_number_2(self):
        with self.assertRaises(ValueError):
            solution.verify_expiration_year("2025g")

    def test_not_a_number_3(self):
        with self.assertRaises(ValueError):
            solution.verify_expiration_year("x2025")

    def test_too_many_digits(self):
        with self.assertRaises(ValueError):
            solution.verify_birth_year("02025")

    def test_too_low(self):
        with self.assertRaises(ValueError):
            solution.verify_expiration_year("2019")

    def test_too_high(self):
        with self.assertRaises(ValueError):
            solution.verify_expiration_year("2031")

    def test_min(self):
        self.assertEqual(solution.verify_expiration_year("2020"), 2020)

    def test_max(self):
        self.assertEqual(solution.verify_expiration_year("2030"), 2030)

    def test_mid_range(self):
        self.assertEqual(solution.verify_expiration_year("2025"), 2025)


class VerifyHeightTests(TestCase):
    def test_invalid_format(self):
        with self.assertRaises(ValueError):
            solution.verify_height("what's-that")

    def test_invalid_format_number(self):
        with self.assertRaises(ValueError):
            solution.verify_height("x160cm")

    def test_invalid_format_unit(self):
        with self.assertRaises(ValueError):
            solution.verify_height("160kcm")

    def test_height_cm_too_low(self):
        with self.assertRaises(ValueError):
            solution.verify_height("149cm")

    def test_height_cm_too_high(self):
        with self.assertRaises(ValueError):
            solution.verify_height("194cm")

    def test_height_in_too_low(self):
        with self.assertRaises(ValueError):
            solution.verify_height("58in")

    def test_height_in_too_high(self):
        with self.assertRaises(ValueError):
            solution.verify_height("77in")

    def test_height_cm_min(self):
        self.assertEqual(solution.verify_height("150cm"), (150, "cm"))

    def test_height_cm_max(self):
        self.assertEqual(solution.verify_height("193cm"), (193, "cm"))

    def test_height_cm_mid(self):
        self.assertEqual(solution.verify_height("170cm"), (170, "cm"))

    def test_height_in_min(self):
        self.assertEqual(solution.verify_height("59in"), (59, "in"))

    def test_height_cm_max(self):
        self.assertEqual(solution.verify_height("76in"), (76, "in"))

    def test_height_cm_mid(self):
        self.assertEqual(solution.verify_height("60in"), (60, "in"))


class TestVerifyHairColor(TestCase):
    def test_missing_sharp_prefix(self):
        with self.assertRaises(ValueError):
            solution.verify_hair_color("88bb33")

    def test_invalid_digit(self):
        with self.assertRaises(ValueError):
            solution.verify_hair_color("#88gb33")

    def test_not_enough_digits(self):
        with self.assertRaises(ValueError):
            solution.verify_hair_color("#88bb3")

    def test_not_invalid_prefix(self):
        with self.assertRaises(ValueError):
            solution.verify_hair_color("xxx#88bb33")

    def test_not_invalid_suffix(self):
        with self.assertRaises(ValueError):
            solution.verify_hair_color("#88bb33xxx")

    def test_valid_color(self):
        self.assertEqual(solution.verify_hair_color("#090a88"), "#090a88")
