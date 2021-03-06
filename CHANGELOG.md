# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased] - yyyy-mm-dd

## [1.8.0] - 2021-07-14

### Added

- `esi.retry_task_if_esi_is_down`: Retry current celery task if ESI is not online or error threshold is exceeded.
- `views.JSONResponseMixin`: A mixin that can be used to render a JSON response for a class based view.

### Changed

- Deprecated: `allianceauth.create_fake_user`. Use `testing.create_fake_user` instead.
- Deprecated: `testing.BravadoOperationStub`. Use `esi_testing.BravadoOperationStub` instead.
- Deprecated: `testing.BravadoResponseStub`. Use `esi_testing.BravadoResponseStub` instead.

## [1.7.1] - 2021-07-01

### Changed

- Renamed `APP_UTILS_ADMIN_NOTIFY_TIMEOUT` to `APP_UTILS_NOTIFY_THROTTLED_TIMEOUT`

## [1.7.0] - 2021-07-01

### Added

- `helpers.throttle`: Allows calling any function throttled, e.g. to once per day
- `allianceauth.notify_throttled`: Send notification throttled, e.g. to once a day only

## [1.6.0] - 2021-06-29

### Changed

- esi.fetch_esi_status() will not report ESI as down during the daily downtime by default
- messages.messages_plus: Disabled icon feature, since it is not provided by Auth core. Icons will still be rendered, but are now created by Auth (with allianceauth>=2.8.5).

## [1.5.0] - 2021-06-26

### Added

- New section esi containing helpers for working with ESI

### Changed

- Improved documentation with a short summary for each section.
- Logging from this package will now include it's full verbose name

## [1.4.0] - 2021-06-24

### Added

- allianceauth.create_fake_user
- allianceauth.notify_admins_throttled
- views.HttpResponseNoContent

### Changed

- Improved documentation layout

## [1.3.0] - 2021-05-06

### Added

- helpers.humanize_number

## [1.2.0] - 2021-04-16

### Added

- helpers.AttrDict: Access dict like an object
- views.BootstrapStyle
- views.fontawesome_modal_button_html

### Changed

- Performance improvement for django.users_with_permission

### Fixed

- Create TZ aware timestamps in fake ESI response

## [1.1.0] - 2021-03-19

### Added

- testing.create_user_from_evecharacter
- esi_testing module with tools for testing with django-esi
- testing: response_text, json_response_to_python, json_response_to_dict, multi_assert_in, multi_assert_not_in


## [1.0.2] - 2021-03-13

### Changed

- urls.reverse_absolute now also accepts args

## [1.0.1] - 2021-02-27

### Changed

- Improved API documentation
- Restructured test modules

### Fixed

- testing.add_character_to_user_2 not returning EveCharacter

## [1.0.0] - 2021-02-20

### Added

- API documentation on readthedocs

## [1.0.0a7] - 2021-02-18

### Added

- allianceauth.is_night_mode
- django.admin_boolean_icon_html

## [1.0.0a6] - 2021-02-14

### Added

- datetime.ldap_time_2_datetime
- datetime.ldap_timedelta_2_timedelta

## [1.0.0a5] - 2021-02-14

### Added

- allianceauth.notify_admins
- urls.reverse_absolute
- urls.static_file_absolute_url

### Changed

- datetime.timeuntil_str: added show_seconds argument

## [1.0.0a4] - 2021-02-11

### Fixed

- bootstrap labels are spans

## [1.0.0a3] - 2021-02-10

### Changed

- `django.users_with_permission` now also returns superusers by default

## [1.0.0a1] - 2021-02-09

### Added

- Initial
