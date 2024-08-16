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

from typing import TextIO, final, override

import yaml

from unirule.exception import BadIrError, IncapableOutputError
from unirule.exporter import BaseExporter
from unirule.util import Registry

# for key
_reg = Registry()


@_reg.key_handler("domain")
def _trans_domain(value: list[str]) -> list[str]:
    return value


@_reg.key_handler("domain_suffix")
def _trans_domain_suffix(value: list[str]) -> list[str]:
    result = []
    for item in value:
        if item.startswith("."):
            # special domain suffix
            result.append(item)
        else:
            # general domain suffix
            result.append(f"+.{item}")
    return result


# TODO: add support for "domain_regex" produced by MetaDomain*Importer


# 1 rule item -> N rule lines
def _export_metadomain(rule: dict) -> list[str]:
    match tp := rule.get("type"):
        case None:
            results = []
            for key, value in rule.items():
                if len(value) == 0:
                    continue
                # translate all fields
                trans_func = _reg.get(key)
                results.extend(trans_func(value))
            return results
        case "logical":
            raise IncapableOutputError("logical rule is not supported")
        case _:
            raise BadIrError(f"unexpected rule type: {tp}")


@final
class MetaDomainYamlExporter(BaseExporter):
    @override
    def export(self, stream: TextIO) -> None:
        rules = []
        for item in self.ir:
            rules.extend(_export_metadomain(item))
        # format: { payload: [] }
        yaml.dump({"payload": rules}, stream)


@final
class MetaDomainTextExporter(BaseExporter):
    @override
    def export(self, stream: TextIO) -> None:
        rules = []
        for item in self.ir:
            rules.extend(_export_metadomain(item))
        stream.write("\n".join(rules))
