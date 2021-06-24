from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase, override_settings

from allianceauth.notifications.models import Notification
from app_utils.allianceauth import (
    _ADMIN_NOTIFY_TIMEOUT_DEFAULT,
    create_fake_user,
    notify_admins,
    notify_admins_throttled,
)


class TestCreateFakeUser(TestCase):
    def test_should_create_fake_user(self):
        # when
        user = create_fake_user(1001, "Bruce Wayne")
        # then
        self.assertTrue(User.objects.filter(pk=user.pk).exists())
        self.assertEqual(user.username, "Bruce_Wayne")
        self.assertEqual(user.profile.main_character.character_id, 1001)
        self.assertEqual(user.profile.main_character.character_name, "Bruce Wayne")
        self.assertEqual(user.profile.main_character.corporation_id, 2001)
        self.assertEqual(user.profile.main_character.alliance_id, 3001)
        self.assertEqual(user.profile.main_character.alliance_name, "Wayne Enterprises")

    def test_should_create_fake_user_with_corporation(self):
        # when
        user = create_fake_user(
            1001,
            "Bruce Wayne",
            corporation_id=2002,
            corporation_name="Dummy corp",
            corporation_ticker="ABC",
        )
        # then
        self.assertEqual(user.profile.main_character.corporation_id, 2002)
        self.assertEqual(user.profile.main_character.corporation_name, "Dummy corp")
        self.assertEqual(user.profile.main_character.corporation_ticker, "ABC")
        self.assertIsNone(user.profile.main_character.alliance_id)

    def test_should_create_fake_user_with_permissions(self):
        # when
        user = create_fake_user(1001, "Bruce Wayne", permissions=["auth.add_group"])
        # then
        self.assertTrue(user.has_perm("auth.add_group"))


class TestNotifyAdmins(TestCase):
    def test_should_notify_users_with_logging_permissions_and_superusers_only(self):
        # given
        superuser = User.objects.create_superuser(username="super")
        user_admin = create_fake_user(
            1001, "Bruce Wayne", permissions=["auth.logging_notifications"]
        )
        user_regular = create_fake_user(1002, "Peter Parker")
        # when
        notify_admins("message", "title", "danger")
        # then
        self.assertEqual(Notification.objects.filter(user=superuser).count(), 1)
        self.assertEqual(Notification.objects.filter(user=user_admin).count(), 1)
        self.assertEqual(Notification.objects.filter(user=user_regular).count(), 0)
        notif = Notification.objects.filter(user=superuser).first()
        self.assertEqual(notif.message, "message")
        self.assertEqual(notif.title, "title")
        self.assertEqual(notif.level, "danger")


class TestNotifyAdminsThrottled(TestCase):
    def test_should_send_notification_when_new(self):
        # given
        user_admin = create_fake_user(
            1001, "Bruce Wayne", permissions=["auth.logging_notifications"]
        )
        cache.clear()
        # when
        notify_admins_throttled("message-id", "message", "title")
        # then
        self.assertEqual(Notification.objects.filter(user=user_admin).count(), 1)

    def test_should_discard_subsequent_notifications_while_throttled(self):
        # given
        user_admin = create_fake_user(
            1001, "Bruce Wayne", permissions=["auth.logging_notifications"]
        )
        cache.clear()
        # when
        notify_admins_throttled("message-id", "message", "title")
        notify_admins_throttled("message-id", "message", "title")
        # then
        self.assertEqual(Notification.objects.filter(user=user_admin).count(), 1)

    @patch("app_utils.allianceauth.cache.get_or_set", wraps=cache.get_or_set)
    def test_should_use_default_timeout_when_not_specified(self, spy_cache_get_or_set):
        # given
        create_fake_user(
            1001, "Bruce Wayne", permissions=["auth.logging_notifications"]
        )
        cache.clear()
        # when
        notify_admins_throttled("message-id", "message", "title")
        # then
        args, _ = spy_cache_get_or_set.call_args
        self.assertEqual(args[2], _ADMIN_NOTIFY_TIMEOUT_DEFAULT)

    @override_settings(APP_UTILS_ADMIN_NOTIFY_TIMEOUT=123)
    @patch("app_utils.allianceauth.cache.get_or_set", wraps=cache.get_or_set)
    def test_should_use_timeout_setting_when_defined(self, spy_cache_get_or_set):
        # given
        create_fake_user(
            1001, "Bruce Wayne", permissions=["auth.logging_notifications"]
        )
        cache.clear()
        # when
        notify_admins_throttled("message-id", "message", "title")
        # then
        args, _ = spy_cache_get_or_set.call_args
        self.assertEqual(args[2], 123)

    @override_settings(APP_UTILS_ADMIN_NOTIFY_TIMEOUT="invalid")
    @patch("app_utils.allianceauth.cache.get_or_set", wraps=cache.get_or_set)
    def test_should_use_default_timeout_when_setting_invalid_1(
        self, spy_cache_get_or_set
    ):
        # given
        create_fake_user(
            1001, "Bruce Wayne", permissions=["auth.logging_notifications"]
        )
        cache.clear()
        # when
        notify_admins_throttled("message-id", "message", "title")
        # then
        args, _ = spy_cache_get_or_set.call_args
        self.assertEqual(args[2], _ADMIN_NOTIFY_TIMEOUT_DEFAULT)

    @override_settings(APP_UTILS_ADMIN_NOTIFY_TIMEOUT=-1)
    @patch("app_utils.allianceauth.cache.get_or_set", wraps=cache.get_or_set)
    def test_should_use_default_timeout_when_setting_invalid_2(
        self, spy_cache_get_or_set
    ):
        # given
        create_fake_user(
            1001, "Bruce Wayne", permissions=["auth.logging_notifications"]
        )
        cache.clear()
        # when
        notify_admins_throttled("message-id", "message", "title")
        # then
        args, _ = spy_cache_get_or_set.call_args
        self.assertEqual(args[2], _ADMIN_NOTIFY_TIMEOUT_DEFAULT)
