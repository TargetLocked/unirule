# Copyright (C) 2024 TargetLocked
#
# This file is part of unirule.
#
# unirule is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# unirule is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with unirule.  If not, see <https://www.gnu.org/licenses/>.


from typing import Callable, Optional


class Registry:
    """Registry for dispatching key to the corresponding hook function."""

    NOMATCH = "__nomatch__"

    # TODO: custom error handler for more friendly error msgs

    def __init__(self) -> None:
        self._data = {}
        self._nomatch_value: Optional[Callable] = None

    def set(self, key: str, value: Callable) -> None:
        if key is self.NOMATCH:
            self._nomatch_value = value
        elif key in self._data:
            raise ValueError(f"duplicate key in Registry: {key}")
        self._data[key] = value

    def get(self, key: str) -> Callable:
        try:
            return self._data[key]
        except KeyError:
            if self._nomatch_value is not None:
                return self._nomatch_value
            raise ValueError(f"unsupported key: {key}") from None

    def key_handler(self, key: str) -> Callable:
        """Set the decorated function as a hook.

        Arguments:
            key -- key to use

        Returns:
            A decorator.
        """

        def _decorator(func: Callable) -> Callable:
            self.set(key, func)
            return func

        return _decorator
