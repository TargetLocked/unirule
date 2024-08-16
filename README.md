# unirule

Rule converter for proxy platforms.

unirule supports rules in text formats only. For binary formats, we recommend [MetaCubeX/geo](https://github.com/MetaCubeX/geo).

## Install

unirule requires Python >= 3.10 .

```bash
pip install unirule
```

## Usage

```bash
unirule -h
```

```plain
usage: unirule [-h] -i {singbox,dlc,meta-domain-yaml,meta-domain-text} -o {singbox,dlc,meta-domain-yaml,meta-domain-text} input_path output_path

positional arguments:
  input_path            "stdin" or path to the input file
  output_path           "stdout" or path to the output file

options:
  -h, --help            show this help message and exit
  -i {singbox,dlc,meta-domain-yaml,meta-domain-text}, --input-type {singbox,dlc,meta-domain-yaml,meta-domain-text}
                        type of the input file
  -o {singbox,dlc,meta-domain-yaml,meta-domain-text}, --output-type {singbox,dlc,meta-domain-yaml,meta-domain-text}
                        type of the output file
```

## Develop

This project uses [Rye](https://rye.astral.sh/).

```bash
git clone https://github.com/TargetLocked/unirule.git
cd unirule
rye sync
```

For more information, please refer to the manual of Rye.
