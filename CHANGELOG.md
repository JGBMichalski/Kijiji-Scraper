# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2022-08-02

### Fixed
- Fixed `smtplib` implementation to work with Outlook since GMail is no longer supported due to Google updates (more information can be found on the [Google Account Help Page](https://support.google.com/accounts/answer/6010255?hl=en)).

## [1.0.2] - 2022-02-17

### Fixed
- Docker container now contains the `VERSION` file.

## [1.0.1] - 2022-02-17

### Added
- Added version docker tagging to Github Actions.

### Changed
- Version information is now stored in `VERSION` found in the root directory.

## [1.0.0] - 2022-02-16

### Added
- Initial Release