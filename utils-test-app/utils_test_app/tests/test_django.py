from unittest.mock import Mock, patch

from allianceauth.tests.auth_utils import AuthUtils
from app_utils.django import app_labels, clean_setting, users_with_permission
from django.contrib.auth.models import Group, User
from django.test import TestCase

MODULE_PATH = "app_utils"


class TestAppLabel(TestCase):
    def test_returns_set_of_app_labels(self):
        labels = app_labels()
        for label in ["authentication", "groupmanagement", "eveonline"]:
            self.assertIn(label, labels)


class TestCleanSetting(TestCase):
    @patch(MODULE_PATH + ".django.settings")
    def test_default_if_not_set(self, mock_settings):
        mock_settings.TEST_SETTING_DUMMY = Mock(spec=None)
        result = clean_setting(
            "TEST_SETTING_DUMMY",
            False,
        )
        self.assertEqual(result, False)

    @patch(MODULE_PATH + ".django.settings")
    def test_default_if_not_set_for_none(self, mock_settings):
        mock_settings.TEST_SETTING_DUMMY = Mock(spec=None)
        result = clean_setting("TEST_SETTING_DUMMY", None, required_type=int)
        self.assertEqual(result, None)

    @patch(MODULE_PATH + ".django.settings")
    def test_true_stays_true(self, mock_settings):
        mock_settings.TEST_SETTING_DUMMY = True
        result = clean_setting(
            "TEST_SETTING_DUMMY",
            False,
        )
        self.assertEqual(result, True)

    @patch(MODULE_PATH + ".django.settings")
    def test_false_stays_false(self, mock_settings):
        mock_settings.TEST_SETTING_DUMMY = False
        result = clean_setting("TEST_SETTING_DUMMY", False)
        self.assertEqual(result, False)

    @patch(MODULE_PATH + ".django.settings")
    def test_default_for_invalid_type_bool(self, mock_settings):
        mock_settings.TEST_SETTING_DUMMY = "invalid type"
        result = clean_setting("TEST_SETTING_DUMMY", False)
        self.assertEqual(result, False)

    @patch(MODULE_PATH + ".django.settings")
    def test_default_for_invalid_type_int(self, mock_settings):
        mock_settings.TEST_SETTING_DUMMY = "invalid type"
        result = clean_setting("TEST_SETTING_DUMMY", 50)
        self.assertEqual(result, 50)

    @patch(MODULE_PATH + ".django.settings")
    def test_none_allowed_for_type_int(self, mock_settings):
        mock_settings.TEST_SETTING_DUMMY = None
        result = clean_setting("TEST_SETTING_DUMMY", 50)
        self.assertIsNone(result)

    @patch(MODULE_PATH + ".django.settings")
    def test_default_if_below_minimum_1(self, mock_settings):
        """when setting is below minimum and default is > minium, then use minimum"""
        mock_settings.TEST_SETTING_DUMMY = -5
        result = clean_setting("TEST_SETTING_DUMMY", default_value=50)
        self.assertEqual(result, 0)

    @patch(MODULE_PATH + ".django.settings")
    def test_default_if_below_minimum_2(self, mock_settings):
        """when setting is below minimum, then use minimum"""
        mock_settings.TEST_SETTING_DUMMY = -50
        result = clean_setting("TEST_SETTING_DUMMY", default_value=50, min_value=-10)
        self.assertEqual(result, -10)

    @patch(MODULE_PATH + ".django.settings")
    def test_default_if_below_minimum_3(self, mock_settings):
        """when default is None and setting is below minimum, then use minimum"""
        mock_settings.TEST_SETTING_DUMMY = 10
        result = clean_setting(
            "TEST_SETTING_DUMMY", default_value=None, required_type=int, min_value=30
        )
        self.assertEqual(result, 30)

    @patch(MODULE_PATH + ".django.settings")
    def test_setting_if_above_maximum(self, mock_settings):
        """when setting is above maximum, then use maximum"""
        mock_settings.TEST_SETTING_DUMMY = 100
        result = clean_setting("TEST_SETTING_DUMMY", default_value=10, max_value=50)
        self.assertEqual(result, 50)

    @patch(MODULE_PATH + ".django.settings")
    def test_default_below_minimum(self, mock_settings):
        """when default is below minimum, then raise exception"""
        mock_settings.TEST_SETTING_DUMMY = 10
        with self.assertRaises(ValueError):
            clean_setting("TEST_SETTING_DUMMY", default_value=10, min_value=50)

    @patch(MODULE_PATH + ".django.settings")
    def test_default_above_maximum(self, mock_settings):
        """when default is below minimum, then raise exception"""
        mock_settings.TEST_SETTING_DUMMY = 10
        with self.assertRaises(ValueError):
            clean_setting("TEST_SETTING_DUMMY", default_value=100, max_value=50)

    @patch(MODULE_PATH + ".django.settings")
    def test_default_is_none_needs_required_type(self, mock_settings):
        mock_settings.TEST_SETTING_DUMMY = "invalid type"
        with self.assertRaises(ValueError):
            clean_setting("TEST_SETTING_DUMMY", default_value=None)

    @patch(MODULE_PATH + ".django.settings")
    def test_when_value_in_choices_return_it(self, mock_settings):
        mock_settings.TEST_SETTING_DUMMY = "bravo"
        result = clean_setting(
            "TEST_SETTING_DUMMY", default_value="alpha", choices=["alpha", "bravo"]
        )
        self.assertEqual(result, "bravo")

    @patch(MODULE_PATH + ".django.settings")
    def test_when_value_not_in_choices_return_default(self, mock_settings):
        mock_settings.TEST_SETTING_DUMMY = "charlie"
        result = clean_setting(
            "TEST_SETTING_DUMMY", default_value="alpha", choices=["alpha", "bravo"]
        )
        self.assertEqual(result, "alpha")


class TestUsersWithPermissionQS(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.permission = AuthUtils.get_permission_by_name("auth.timer_management")
        cls.group, _ = Group.objects.get_or_create(name="Test Group")
        AuthUtils.add_permissions_to_groups([cls.permission], [cls.group])
        cls.state = AuthUtils.create_state(name="Test State", priority=75)
        cls.state.permissions.add(cls.permission)

    def setUp(self) -> None:
        self.user_1 = AuthUtils.create_user("Bruce Wayne")
        self.user_2 = AuthUtils.create_user("Lex Luther")
        self.user_3 = User.objects.create_superuser("Spiderman")

    @classmethod
    def user_with_permission_pks(cls, include_superusers=True) -> set:
        return set(
            users_with_permission(
                cls.permission, include_superusers=include_superusers
            ).values_list("pk", flat=True)
        )

    def test_should_return_users_with_user_permission(self):
        # given
        AuthUtils.add_permissions_to_user([self.permission], self.user_1)
        # when
        result = self.user_with_permission_pks()
        # then
        self.assertSetEqual(result, {self.user_1.pk, self.user_3.pk})

    def test_should_return_users_with_user_permission_excluding_superusers(self):
        # given
        AuthUtils.add_permissions_to_user([self.permission], self.user_1)
        # when
        result = self.user_with_permission_pks(include_superusers=False)
        # then
        self.assertSetEqual(result, {self.user_1.pk})

    def test_group_permission(self):
        """group permissions"""
        self.user_1.groups.add(self.group)
        self.assertSetEqual(
            self.user_with_permission_pks(), {self.user_1.pk, self.user_3.pk}
        )

    def test_state_permission(self):
        """state permissions"""
        AuthUtils.assign_state(self.user_1, self.state, disconnect_signals=True)
        self.assertSetEqual(
            self.user_with_permission_pks(), {self.user_1.pk, self.user_3.pk}
        )

    def test_distinct_qs(self):
        """only return one user object, despite multiple matches"""
        # given
        AuthUtils.add_permissions_to_user([self.permission], self.user_1)
        self.user_1.groups.add(self.group)
        AuthUtils.assign_state(self.user_1, self.state, disconnect_signals=True)
        # when
        result = self.user_with_permission_pks()
        # then
        self.assertSetEqual(result, {self.user_1.pk, self.user_3.pk})
