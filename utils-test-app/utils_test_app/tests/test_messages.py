from unittest.mock import Mock, patch

from django.http import HttpRequest
from django.test import TestCase

from app_utils.messages import messages_plus

MODULE_PATH = "app_utils"


class TestMessagePlus(TestCase):
    @patch(MODULE_PATH + ".messages.messages", spec=True)
    def test_valid_call(self, mock_messages):
        messages_plus.debug(Mock(spec=HttpRequest), "Test Message")
        self.assertTrue(mock_messages.debug.called)
        call_args_list = mock_messages.debug.call_args_list
        args, kwargs = call_args_list[0]
        self.assertEqual(
            args[1],
            '<span class="glyphicon glyphicon-eye-open" '
            'aria-hidden="true"></span>&nbsp;&nbsp;'
            "Test Message",
        )

    def test_invalid_level(self):
        with self.assertRaises(ValueError):
            messages_plus._add_messages_icon(987, "Test Message")

    @patch(MODULE_PATH + ".messages.messages")
    def test_all_levels(self, mock_messages):
        text = "Test Message"
        messages_plus.error(Mock(spec=HttpRequest), text)
        self.assertTrue(mock_messages.error.called)

        messages_plus.debug(Mock(spec=HttpRequest), text)
        self.assertTrue(mock_messages.debug.called)

        messages_plus.info(Mock(spec=HttpRequest), text)
        self.assertTrue(mock_messages.info.called)

        messages_plus.success(Mock(spec=HttpRequest), text)
        self.assertTrue(mock_messages.success.called)

        messages_plus.warning(Mock(spec=HttpRequest), text)
        self.assertTrue(mock_messages.warning.called)
