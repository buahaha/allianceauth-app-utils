===============
API
===============

allianceauth
============

Utilities related to Alliance Auth.

.. automodule:: app_utils.allianceauth
    :members:

caching
=======

Utilities for caching objects and querysets.

.. automodule:: app_utils.caching
    :members:

datetime
========

Utilities related to date and time.

.. automodule:: app_utils.datetime
    :members:

django
========

Extending the Django utilities.

.. automodule:: app_utils.django
    :members:

esi
========

Helpers for working with ESI.

.. autoclass:: app_utils.esi.EsiStatusException
.. autoclass:: app_utils.esi.EsiOffline
.. autoclass:: app_utils.esi.EsiErrorLimitExceeded
    :members: retry_in
.. autoclass:: app_utils.esi.EsiStatus
    :members: is_online, error_limit_remain, error_limit_reset, is_error_limit_exceeded, error_limit_reset_w_jitter, raise_for_status
.. autofunction:: app_utils.esi.fetch_esi_status

esi_testing
===========

Utilities for testing features using django-esi.

.. automodule:: app_utils.esi_testing
    :members:

helpers
=======

General purpose helpers.

.. automodule:: app_utils.helpers
    :members:

json
========

JSON related utilities.

.. autoclass:: app_utils.json.JSONDateTimeDecoder

.. autoclass:: app_utils.json.JSONDateTimeEncoder

logging
========

Utilities for enhancing logging.

.. autoclass:: app_utils.logging.LoggerAddTag
.. autofunction:: app_utils.logging.make_logger_prefix

messages
========

Improvement of the Django message class.

.. automodule:: app_utils.messages
    :members:

testing
========

Utilities for making it easier to write tests.

.. autofunction:: app_utils.testing.add_character_to_user
.. autofunction:: app_utils.testing.add_character_to_user_2
.. autofunction:: app_utils.testing.add_new_token
.. autoclass:: app_utils.testing.BravadoOperationStub
.. autoclass:: app_utils.testing.BravadoResponseStub
.. autofunction:: app_utils.testing.generate_invalid_pk
.. autoclass:: app_utils.testing.NoSocketsTestCase
.. autofunction:: app_utils.testing.queryset_pks
.. autofunction:: app_utils.testing.set_test_logger

urls
========

Utilities related to URLs.

.. automodule:: app_utils.urls
    :members:

views
========

Utilities for supporting Django views.

.. automodule:: app_utils.views
    :members:
