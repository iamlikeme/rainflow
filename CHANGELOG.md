# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [3.0.0] - 2020-04-20

### Changed
- (#35) By default, the first and the last points in the time series
  are treated as reversals.
- (#37) Function `reversals` now yields index and value of each reversal,
  instead of value only.
- (#38) Function `extract_cycles` now yields range, mean, count, start index and
  end index for each cycle instead of low, high and count.
- (#43) Arguments `binsize` and `nbins` to `count_cycles` produce bins which
  include the right edge and exclude the left edge.

### Removed
- (#35) Removed optional arguments `left` and `right` to functions
  `reversals`, `extract_cycles` and `count_cycles`. The new behaviour
  correspods to `left=True` and `right=True`.

## [2.2.0] - 2019-10-23

### Added
- (#22) Function `count_cycles` now accepts optional arguments `binsize` and `nbins`
  for binning cycle ranges. Contributed by [gsokoll](https://github.com/gsokoll).

## [2.1.2] - 2018-06-14

### Changed
- (#18) Function `extract_cycles` yields trailing half-cycles in the same order
  as these cycles start. Contributed by [oysteoh](https://github.com/oysteoh).
- Licence changed to MIT (previously GPL v3)

## [2.1.1] - 2018-04-17

### Changed
- Long description based on `README.md` is now included in the distribution package.

## [2.1.0] - 2018-04-17

### Added
- (#10) Added optional arguments `left` and `right` to functions
  `reversals`, `extract_cycles` and `count_cycles`. The arguments
  tell whether the first and the last point in the time series
  should be treated as a reversal (both `False` by default).

## [2.0.0] - 2018-02-25

### Changed
- (#7) Function `extract_cycles` is now a generator and yields low, high and count
  for each cycle. Previously the function returned ranges only.

## [1.0.2] - 2016-12-06
