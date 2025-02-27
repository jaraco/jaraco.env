from __future__ import annotations

import os
from collections.abc import Mapping


class Check:
    """
    Check if an environment variable meets a certain expectation.

    See https://github.com/jaraco/pip-run/blob/7688eae0f6e2437ad233eafcf6c807923065bf18/pip_run/commands.py#L79
    for example usage.

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

    def __init__(
        self,
        key: str,
        expect: str,
        *,
        default: str | None = None,
        _lookup: Mapping[str, str] = os.environ,
    ) -> None:
        self.key = key
        self.expect = expect
        self.default = default
        self.lookup = _lookup

    def __bool__(self) -> bool:
        return self.lookup.get(self.key, self.default) == self.expect
