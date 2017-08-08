===================
PyBay Talk Proposal
===================

:Duration: 30 min

Title
=====

Time Zone Troubles: Dealing with Imaginary and Ambiguous Datetimes

Description
===========

Ambiguous datetimes occur when a time zone's UTC offset moves backwards (such as during a daylight saving time transition), leading to two datetimes with identical "wall time"; their complement, imaginary datetimes are "wall times" that do not exist in a given time zone, because they were skipped over when a time zone's UTC offset moved forward. Python 3.6 introduces a "fold" attribute to allow for disambiguation of local times (PEP495).

This talk will cover dealing with edge cases related to ambiguous and imaginary datetimes, the different approaches taken by pytz and dateutil, what changes with PEP 495, and some lessons learned from implementing backwards-compatible PEP495-compliant tzinfo classes in the dateutil library.


Audience
========

This talk will provide some useful information to developers about dealing with timezone-aware datetimes, with a particular deep dive into handling UTC offset transitions - a notoriously tricky subject. No prior experience will be required to understand this talk.

Outline
=======

(Note: Times at the highest level of the outline include times for the items on lower levels,
times preceeded by "T" are a running total)

- Introduction [6m]
  - Time zone transitions (DST, base offset changes) (2m 30s)
  - Ambiguous datetimes (1m)
  - Imaginary datetimes (30s)
  - Edge cases (2m)
- Python time zone model [7m, T: 13m]
  - tzinfo objects and implementation (3m)
    - Time zone details as a function of wall time
  - Disambiguation: property of datetime or tzinfo? (1m)
  - PEP 495 changes (3m)
    - Fold attribute
    - datetime comparisons
    - Default value for unspecified ambiguous times
- Handling transitions (pytz and dateutil.tz) [5m, T: 18m]
  - Constructing unambiguous datetimes (1m)
  - Detecting and handling imaginary times (1m)
  - Backwards compatibility (dateutil only): (2m)
    - Pre-PEP495: _DatetimeWithFold objects
    - "enfold" method
- General time-zone handling recommendations [7m 15s, T: 25m15s]
  - UTC (45s)
  - Fixed-offset zones (45s)
  - Local time [2m 15s]
    - General (1m 30s)
    - Windows  (45s)
  - Time zone strings (1m 30s)
  - Olson database zones (2m)
- Concluding remarks [45, T: 26m]

I have left in a buffer so that whatever seems interesting can be expanded on if necessary.

Some further details about the content
--------------------------------------
I gave a "lightning talk" version of this talk at PyCon 2017 in the morning session, [video here](https://youtu.be/SXl-pZnoaQ0?t=1225). I also gave a more general talk on using python-dateutil at Pygotham 2016, video is available
[here](http://pyvideo.org/pygotham-2016/python-dateutil-a-delightful-romp-in-the-never-confusing-world-of-dates-and-times.html)
(audio may be a bit messed up), [slides](https://pganssle.github.io/pygotham-2016-dateutil-talk), [slide repo with Jupyter notebook](https://github.com/pganssle/pygotham-2016-dateutil-talk).
