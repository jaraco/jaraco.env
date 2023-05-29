import collections
import os


class Prefix(collections.abc.Mapping):
    """
    >>> setenv = getfixture('monkeypatch').setenv
    >>> setenv('JARACO_ENV_FOO', 'foo')
    >>> setenv('JARACO_ENV_BAR', 'bar')
    >>> env = Prefix('jaraco_env_')
    >>> dict(env)
    {'foo': 'foo', 'bar': 'bar'}
    >>> bool(env.check('foo', expect='foo'))
    True
    """

    def __init__(self, value):
        self.value = value.lower()

    def __iter__(self):
        return (
            val.lower().removeprefix(self.value)
            for val in os.environ
            if val.lower().startswith(self.value)
        )

    def __len__(self):
        return len(tuple(iter(self)))

    def __getitem__(self, key):
        return os.environ[self.value.upper() + key.upper()]

    def check(self, *args, **kwargs):
        return Check(*args, lookup=self, **kwargs)


class Check:
    """
    Check if an environment variable meets a certain expectation.

    >>> setenv = getfixture('monkeypatch').setenv
    >>> check = Check('SOME_VAR', expect='setting1')
    >>> bool(check)
    False
    >>> setenv('SOME_VAR', 'setting1')
    >>> bool(check)
    True
    >>> setenv('SOME_VAR', 'setting2')
    >>> bool(check)
    False

    >>> check = Check('OTHER_VAR', expect='setting1', default='setting1')
    >>> bool(check)
    True
    >>> setenv('OTHER_VAR', 'setting2')
    >>> bool(check)
    False
    """

    def __init__(self, key, expect, *, default=None, _lookup=os.environ):
        self.key = key
        self.expect = expect
        self.default = default
        self.lookup = _lookup

    def __bool__(self):
        return self.lookup.get(self.key, self.default) == self.expect
