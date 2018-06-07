import os
import time

from datetime import timedelta

from IPython.core.display import HTML, display


def print_tzinfo(dt, fmt_str='%Y-%m-%d %H:%M:%S%z'):
    s0 = '{}\n'.format(dt.strftime(fmt_str))
    s1 = '    tzname: {:>5};'.format(str(dt.tzname()))
    s1 += ' ' * max((1, 24 - len(s1)))

    utc_off = dt.utcoffset()
    if utc_off is not None:
        utc_off = utc_off / timedelta(hours=1)
        utc_off = '{: >6.2f}h'.format(utc_off)
    else:
        utc_off = '     None'

    s2 = 'UTC Offset: {};'.format(utc_off)
    s2 += ' ' * max((1, 28 - len(s2)))  

    dt_off = dt.dst()
    if dt_off is not None:
        dt_off = dt_off / timedelta(hours=1)
        dt_off = '{:>8}h'.format(dt_off)
    else:
        dt_off = '     None'

    s2 += 'DST: {}'.format(dt_off)

    print(s0 + s1 + s2)


def print_dt_eq(dt1, dt2, bold=False):
    out = "{} == {}: {}".format(dt1, dt2, dt1 == dt2)
    if bold:
        out = '<b>' + out + '</b>'
    display(HTML('<div style="font-family: monospace">{}</div>'.format(out)))


class TZContextBase(object):
    """
    Base class for a context manager which allows changing of time zones.

    Subclasses may define a guard variable to either block or or allow time
    zone changes by redefining ``_guard_var_name`` and ``_guard_allows_change``
    The default is that the guard variable must be affirmatively set.

    Subclasses must define ``get_current_tz`` and ``set_current_tz``.
    """
    _guard_var_name = "DATEUTIL_MAY_CHANGE_TZ"
    _guard_allows_change = True

    def __init__(self, tzval):
        self.tzval = tzval
        self._old_tz = None

    @classmethod
    def tz_change_allowed(cls):
        """
        Class method used to query whether or not this class allows time zone
        changes.
        """
        guard = bool(os.environ.get(cls._guard_var_name, False))

        # _guard_allows_change gives the "default" behavior - if True, the
        # guard is overcoming a block. If false, the guard is causing a block.
        # Whether tz_change is allowed is therefore the XNOR of the two.
        return guard == cls._guard_allows_change

    @classmethod
    def tz_change_disallowed_message(cls):
        """ Generate instructions on how to allow tz changes """
        msg = ('Changing time zone not allowed. Set {envar} to {gval} '
               'if you would like to allow this behavior')

        return msg.format(envar=cls._guard_var_name,
                          gval=cls._guard_allows_change)

    def __enter__(self):
        if not self.tz_change_allowed():
            raise ValueError(self.tz_change_disallowed_message())

        self._old_tz = self.get_current_tz()
        self.set_current_tz(self.tzval)

    def __exit__(self, type, value, traceback):
        if self._old_tz is not None:
            self.set_current_tz(self._old_tz)

        self._old_tz = None

    def get_current_tz(self):
        raise NotImplementedError

    def set_current_tz(self):
        raise NotImplementedError


class TZEnvContext(TZContextBase):
    """
    Context manager that temporarily sets the `TZ` variable (for use on
    *nix-like systems). Because the effect is local to the shell anyway, this
    will apply *unless* a guard is set.

    If you do not want the TZ environment variable set, you may set the
    ``DATEUTIL_MAY_NOT_CHANGE_TZ_VAR`` variable to a truthy value.
    """
    _guard_var_name = "DATEUTIL_MAY_NOT_CHANGE_TZ_VAR"
    _guard_allows_change = False

    def get_current_tz(self):
        return os.environ.get('TZ', UnsetTz)

    def set_current_tz(self, tzval):
        if tzval is UnsetTz and 'TZ' in os.environ:
            del os.environ['TZ']
        else:
            os.environ['TZ'] = tzval

        time.tzset()


class UnsetTzClass(object):
    """ Sentinel class for unset time zone variable """
    pass

UnsetTz = UnsetTzClass()
