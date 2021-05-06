from unittest.mock import patch

from django.test import TestCase, override_settings

from app_utils.urls import reverse_absolute, site_absolute_url

MODULE_PATH = "app_utils.urls"
TEST_SITE_URL = "https://auth.example.com"


@override_settings(ESI_SSO_CALLBACK_URL=f"{TEST_SITE_URL}/sso/callback")
class TestReverseAbsolute(TestCase):
    def test_should_return_absolute_url_for_view(self):
        # when
        result = reverse_absolute("admin:index")
        # then
        self.assertEqual(result, f"{TEST_SITE_URL}/admin/")

    def test_should_return_absolute_url_for_view_with_args(self):
        # when
        result = reverse_absolute("admin:app_list", args=["authentication"])
        # then
        self.assertEqual(result, f"{TEST_SITE_URL}/admin/authentication/")


@patch(MODULE_PATH + ".settings")
class TestSiteAbsoluteUrl(TestCase):
    def test_should_return_absolute_url_for_view(self, mock_settings):
        # given
        mock_settings.ESI_SSO_CALLBACK_URL = f"{TEST_SITE_URL}/sso/callback"
        # when
        result = site_absolute_url()
        # then
        self.assertEqual(result, TEST_SITE_URL)

    def test_should_return_empty_string_1(self, mock_settings):
        # given
        mock_settings.ESI_SSO_CALLBACK_URL = TEST_SITE_URL
        # when
        result = site_absolute_url()
        # then
        self.assertEqual(result, "")

    def test_should_return_empty_string_2(self, mock_settings):
        # given
        mock_settings.ESI_SSO_CALLBACK_URL = ""
        # when
        result = site_absolute_url()
        # then
        self.assertEqual(result, "")
