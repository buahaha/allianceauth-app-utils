# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased] - yyyy-mm-dd

## [0.4.0] - 2021-01-01

### Added

- New method `clear()` removes all messages form a queue
- pre-commit with Black, Flake8, EOFs

### Changes

- Removed support for Python 3.5

## [0.3.1] - 2020-08-04

### Fixes

- enqueue() does not return new size of queue

## [0.3.0] - 2020-07-23

### Changes

- Rename to redis-simple-mq / SimpleMQ
- Moved to GitLab
- Added missing tests
- Removed `base_name` from `SimpleMQ()`
- Changed `name` in `SimpleMQ()` to optional

## [0.2.0] - 2020-07-19

### Changes

- changed `size` from property to method

## [0.1.0] - 2019-12-23

### Added

- Initial
