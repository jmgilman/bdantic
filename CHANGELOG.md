# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.2] - 2022-02-09

### Added

- `query` and `realize` methods for querying and realize a `BeancountFile`

## [0.2.1] - 2022-02-08

### Added

- `id` field to all directive types to uniquely identify them
- `by_id` and `by_ids` methods to `Directives` for fetching directives by ID
- `by_account` method to `Directives` for fetching directives by account name
- `by_type` method to `Directives` and `TxnPostings` for fetching entries by
   type
- `accounts` field to `BeancountFile` for holding all `Account` instances parsed
   from the file
- `compress` and `decompress` methods to `BeancountFile` for compressing and
  decompressing a whole `BeancountFile` instance.

### Changed

- `Account` no longer holds copies of the directives associated with the account

### Fixed

- Added missing imports from `models/__init__.py`

## [0.2.0] - 2022-02-04

### Added

- `filter` and `select` functions for manipulating models
- `BaseList` and `BaseDict` for models which wrap lists and dictionaries
- `TxnPostings` model for holding txn_postings field of a `RealAccount`
- Documentation using mkdocs

### Changed

- `Account` model can now be parsed from a beancount `RealAccount`
- `Entries` renamed to `Directives`
- The `parse` and `export` methods were moved to the base class
- General code cleanup
- Improved most docstrings

## [0.1.3] - 2022-02-02

### Added

- `parse_query` function for parsing query results

### Changed

- `QueryColumn` changed to a model
- The `type` field for `QueryColumn` has been changed from a `Type` to a `str`

# [0.1.2] - 2022-02-01

### Added

- Account model for representing data about a single beancount account

### Changed

- Added export for `parse_realize`
- Bumped `beancount-stubs` to v0.1.3

## [0.1.1] - 2022-02-01

### Added

- Support for parsing responses from realize() operations

### Changed

- Improves consistency across test data generation

## [0.1.0] - 2022-02-01

### Added

- Initial release

[unreleased]: https://github.com/jmgilman/bdantic/compare/v0.2.2...HEAD
[0.2.1]: https://github.com/jmgilman/bdantics/releases/tag/v0.2.2
[0.2.1]: https://github.com/jmgilman/bdantics/releases/tag/v0.2.1
[0.2.0]: https://github.com/jmgilman/bdantics/releases/tag/v0.2.0
[0.1.3]: https://github.com/jmgilman/bdantics/releases/tag/v0.1.3
[0.1.2]: https://github.com/jmgilman/bdantics/releases/tag/v0.1.2
[0.1.1]: https://github.com/jmgilman/bdantics/releases/tag/v0.1.1
[0.1.0]: https://github.com/jmgilman/bdantics/releases/tag/v0.1.0
