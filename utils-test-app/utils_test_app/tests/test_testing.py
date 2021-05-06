import requests

from django.contrib.auth.models import User
from django.test import TestCase

from allianceauth.authentication.models import EveCharacter
from app_utils.testing import (
    NoSocketsTestCase,
    SocketAccessError,
    create_user_from_evecharacter,
    generate_invalid_pk,
)


class TestNoSocketsTestCase(NoSocketsTestCase):
    def test_raises_exception_on_attempted_network_access(self):

        with self.assertRaises(SocketAccessError):
            requests.get("https://www.google.com")


class TestGenerateInvalidPk(TestCase):
    def test_normal(self):
        User.objects.all().delete()
        User.objects.create(username="John Doe", password="dummy")
        invalid_pk = generate_invalid_pk(User)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=invalid_pk)


class TestCreateUserFromEveCharacter(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.character = EveCharacter.objects.create(
            character_id=1001,
            character_name="Bruce Wayne",
            corporation_id=2001,
            corporation_name="Wayne Tech",
            corporation_ticker="WYT",
        )

    def test_should_create_basic_user(self):
        # when
        user, character_ownership = create_user_from_evecharacter(1001)
        # then
        self.assertEqual(user.username, "Bruce_Wayne")
        self.assertEqual(character_ownership.character, self.character)
        self.assertEqual(character_ownership.user, user)

    def test_should_create_user_with_given_scope(self):
        # when
        user, character_ownership = create_user_from_evecharacter(
            1001, scopes=["dummy_scope"]
        )
        # then
        self.assertEqual(user.username, "Bruce_Wayne")
        self.assertEqual(character_ownership.character, self.character)
        self.assertEqual(character_ownership.user, user)
        self.assertTrue(user.token_set.filter(scopes__name="dummy_scope").exists())
