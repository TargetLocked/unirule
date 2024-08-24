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

import argparse
import io
import sys

from unirule.exporter.dlc import DlcExporter
from unirule.exporter.metadomain import MetaDomainTextExporter, MetaDomainYamlExporter
from unirule.exporter.singbox import SingboxExporter
from unirule.importer.dlc import DlcImporter
from unirule.importer.metadomain import MetaDomainTextImporter, MetaDomainYamlImporter
from unirule.importer.singbox import SingboxImporter
from unirule.util import uglobal

INPUT_TYPES = {
    "singbox": SingboxImporter,
    "dlc": DlcImporter,
    "meta-domain-yaml": MetaDomainYamlImporter,
    "meta-domain-text": MetaDomainTextImporter,
}

OUTPUT_TYPES = {
    "singbox": SingboxExporter,
    "dlc": DlcExporter,
    "meta-domain-yaml": MetaDomainYamlExporter,
    "meta-domain-text": MetaDomainTextExporter,
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help='"stdin" or path to the input file')
    parser.add_argument("output_path", help='"stdout" or path to the output file')
    parser.add_argument(
        "-i",
        "--input-type",
        help="type of the input file",
        required=True,
        choices=INPUT_TYPES.keys(),
    )
    parser.add_argument(
        "-o",
        "--output-type",
        help="type of the output file",
        required=True,
        choices=OUTPUT_TYPES.keys(),
    )
    parser.add_argument(
        "-p", "--pedantic", help="mark all warnings as errors", action="store_true"
    )

    args = parser.parse_args()

    uglobal.pedantic = args.pedantic

    # create stream object
    istream = sys.stdin
    if args.input_path != "stdin":
        buffered_file = io.BufferedReader(io.FileIO(args.input_path, mode="r"))
        istream = io.TextIOWrapper(buffered_file, encoding="utf-8")
    ostream = sys.stdout
    if args.output_path != "stdout":
        buffered_file = io.BufferedWriter(io.FileIO(args.output_path, mode="w"))
        ostream = io.TextIOWrapper(buffered_file, encoding="utf-8", newline="\n")

    # find importer and exporter
    importer = INPUT_TYPES[args.input_type]()
    exporter = OUTPUT_TYPES[args.output_type]()

    importer.import_(istream)
    exporter.set_ir(importer.get_ir())
    exporter.export(ostream)

    return 0
