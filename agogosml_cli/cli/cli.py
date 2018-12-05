# -*- coding: utf-8 -*-

"""Console script for agogosml_cli."""
import sys
import click

import cli.init as init
import cli.generate as generate


@click.group()
def main() -> None:
    """CLI and scaffold generation tool for agogosml"""


main.add_command(init.init)
main.add_command(generate.generate)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
